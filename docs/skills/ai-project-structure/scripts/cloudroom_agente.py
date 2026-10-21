#!/usr/bin/env python3
"""Adaptador que faz um filho do Cloudroom se comportar como CLI headless.

Uso no loop (o prompt e sempre o ultimo argumento, como em `claude -p`):

    loop.sh --tarefa T-042 --agente "python3 scripts/cloudroom_agente.py --provider claude-code --model claude-sonnet-5-5"

Abre um filho com `room-cli thread spawn --shared-sandbox --prompt-file`, espera
ate ele terminar, imprime a resposta integral no stdout e sai com o codigo certo.
O filho aparece na barra de threads do Cloudroom, com log, estado e custo.

Somente biblioteca padrao; roda em Linux, macOS e Windows (Git Bash).
Spec: docs/specs/0008-adaptador-cloudroom.md.
"""

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True

ESTADOS_DE_FALHA = {"failed", "error", "stopped", "cancelled", "canceled", "archived"}
CONSULTAS_RUINS_SEGUIDAS = 3
TEMPO_SPAWN = 120
TEMPO_CONSULTA = 60
TEMPO_STOP = 3

EPILOGO = """\
O prompt e o ultimo argumento. O adaptador aceita so as opcoes acima; qualquer
outra, inclusive --top-level, --prompt e --prompt-file, e recusada (exit 1).

Chama `room-cli thread spawn --shared-sandbox --prompt-file ARQUIVO` e consulta
`room-cli thread output ID --all` a cada --intervalo segundos ate o filho
terminar. Nao tem tempo limite proprio: quem limita e o --tempo-maximo do loop.
O id do filho sai no stderr como `thread=<id>` desde o spawn.

Codigos de saida:
  0    resposta integral do filho no stdout, mais uma quebra de linha
  1    uso invalido, room-cli ausente do PATH ou spawn recusado pela CLI
  2    filho falhou, foi parado ou terminou sem resposta (erro no stderr)
  143  SIGTERM ou SIGINT recebido: `room-cli thread stop ID` e saida em ate 5 s
"""


class Interrompido(Exception):
    pass


class Falha(Exception):
    def __init__(self, codigo, mensagem):
        Exception.__init__(self, mensagem)
        self.codigo = codigo
        self.mensagem = mensagem


_sinais = {"protegido": False, "recebido": None}


def _tratar_sinal(numero, quadro):
    _sinais["recebido"] = numero
    if not _sinais["protegido"]:
        raise Interrompido()


def log(texto):
    print(texto, file=sys.stderr, flush=True)


class Parser(argparse.ArgumentParser):
    def error(self, mensagem):
        raise Falha(1, mensagem)


def montar_parser():
    p = Parser(prog="cloudroom_agente.py", allow_abbrev=False, add_help=False,
               formatter_class=argparse.RawDescriptionHelpFormatter,
               usage="cloudroom_agente.py --provider PROVIDER [opcoes] PROMPT",
               description=__doc__.split("\n\n")[0], epilog=EPILOGO)
    p.add_argument("--provider", required=True,
                   help="codex, claude-code, pi, opencode, hermes, devin, fx ou openclaw (obrigatorio)")
    p.add_argument("--model", help="modelo do filho")
    p.add_argument("--reasoning-level", dest="reasoning_level", help="nivel de raciocinio do filho")
    p.add_argument("--service-tier", dest="service_tier", help="default ou fast")
    p.add_argument("--titulo", help="titulo da thread; sem ele: `loop T-NNN` do prompt, senao a primeira linha (80 caracteres)")
    p.add_argument("--arquivar", action="store_true",
                   help="arquiva a thread depois de ler a resposta com sucesso (padrao: deixar para conferir)")
    p.add_argument("--intervalo", type=float, default=10.0,
                   help="segundos entre consultas ao filho (padrao 10)")
    return p


def titulo_de(prompt, explicito):
    if explicito:
        return explicito
    achado = re.search(r"\bT-\d+\b", prompt)
    if achado:
        return "loop " + achado.group(0)
    for linha in prompt.splitlines():
        if linha.strip():
            return linha.strip()[:80]
    return "agente"


def chamar(exe, args, tempo):
    """Roda room-cli e devolve (codigo, stdout, stderr) como texto UTF-8."""
    try:
        p = subprocess.run([exe] + args, capture_output=True, stdin=subprocess.DEVNULL, timeout=tempo)
    except subprocess.TimeoutExpired:
        return None, "", "room-cli nao respondeu em %s s" % tempo
    except OSError as erro:
        return None, "", "nao foi possivel executar room-cli: %s" % erro
    return (p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"))


def json_de(texto):
    try:
        dado = json.loads(texto)
    except ValueError:
        return None
    return dado if isinstance(dado, dict) else None


def abrir_filho(exe, args, prompt):
    """Grava o prompt em arquivo temporario, abre o filho e devolve o id."""
    ident, caminho = tempfile.mkstemp(prefix="cloudroom-agente-", suffix=".txt")
    try:
        with os.fdopen(ident, "wb") as arquivo:
            arquivo.write(prompt.encode("utf-8"))
        cmd = ["thread", "spawn", "--provider", args.provider]
        for flag, valor in (("--model", args.model), ("--reasoning-level", args.reasoning_level),
                            ("--service-tier", args.service_tier)):
            if valor:
                cmd += [flag, valor]
        cmd += ["--title", titulo_de(prompt, args.titulo), "--shared-sandbox", "--prompt-file", caminho]
        _sinais["protegido"] = True
        try:
            codigo, saida, erro = chamar(exe, cmd, TEMPO_SPAWN)
        finally:
            _sinais["protegido"] = False
    finally:
        try:
            os.remove(caminho)
        except OSError:
            pass
    if codigo != 0:
        mensagem = (erro.strip() or saida.strip() or "sem mensagem")
        raise Falha(1, "room-cli thread spawn falhou (codigo %s): %s" % (codigo, mensagem))
    registro = json_de(saida)
    if not registro or not registro.get("id"):
        raise Falha(1, "room-cli thread spawn nao devolveu o id do filho: %s" % saida.strip()[:300])
    return str(registro["id"])


def esperar_resposta(exe, filho, intervalo):
    """Consulta o filho ate `busy` falso e devolve a resposta integral."""
    ruins = 0
    ultimo = ""
    while True:
        codigo, saida, erro = chamar(exe, ["thread", "output", filho, "--all"], TEMPO_CONSULTA)
        registro = json_de(saida) if codigo == 0 else None
        if registro is None:
            ruins += 1
            ultimo = (erro.strip() or saida.strip() or "sem mensagem")[:300]
        elif registro.get("busy"):
            ruins = 0
        else:
            falha = registro.get("error")
            estado = str(registro.get("state") or "")
            if falha:
                raise Falha(2, "filho %s falhou: %s" % (filho, falha))
            if estado.lower() in ESTADOS_DE_FALHA:
                raise Falha(2, "filho %s terminou no estado %s" % (filho, estado))
            resposta = registro.get("reply")
            if isinstance(resposta, str):
                return resposta
            ruins += 1
            ultimo = "filho terminou sem resposta (estado %s)" % (estado or "desconhecido")
        if ruins >= CONSULTAS_RUINS_SEGUIDAS:
            raise Falha(2, "consulta ao filho %s falhou %d vezes seguidas: %s" % (filho, ruins, ultimo))
        time.sleep(intervalo)


def parar_filho(exe, filho):
    for numero in (signal.SIGTERM, signal.SIGINT):
        signal.signal(numero, signal.SIG_IGN)
    codigo, saida, erro = chamar(exe, ["thread", "stop", filho], TEMPO_STOP)
    if codigo != 0:
        log("[AVISO] room-cli thread stop %s falhou: %s" % (filho, (erro.strip() or saida.strip())[:200]))


def main(argv):
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = montar_parser()
    if argv == ["--help"] or argv == ["-h"] or "--help" in argv[:-1] or "-h" in argv[:-1]:
        parser.print_help()
        return 0
    filho = None
    exe = None
    try:
        if not argv:
            raise Falha(1, "falta o prompt (ultimo argumento).")
        prompt = argv[-1]
        args, extras = parser.parse_known_args(argv[:-1])
        if extras:
            raise Falha(1, "opcao nao aceita: %s (veja --help)" % " ".join(extras))
        if not prompt.strip():
            raise Falha(1, "o prompt (ultimo argumento) esta vazio.")
        if not args.intervalo > 0:
            raise Falha(1, "--intervalo precisa ser maior que zero.")
        exe = shutil.which("room-cli")
        if not exe:
            raise Falha(1, "room-cli nao encontrado no PATH; o adaptador so funciona dentro de uma thread do Cloudroom.")
        signal.signal(signal.SIGTERM, _tratar_sinal)
        signal.signal(signal.SIGINT, _tratar_sinal)
        filho = abrir_filho(exe, args, prompt)
        log("thread=%s" % filho)
        if _sinais["recebido"] is not None:
            raise Interrompido()
        resposta = esperar_resposta(exe, filho, args.intervalo)
        sys.stdout.write(resposta + "\n")
        sys.stdout.flush()
        if args.arquivar:
            codigo, saida, erro = chamar(exe, ["thread", "archive", filho], TEMPO_CONSULTA)
            if codigo != 0:
                log("[AVISO] room-cli thread archive %s falhou: %s" % (filho, (erro.strip() or saida.strip())[:200]))
        return 0
    except Falha as falha:
        log("[ERRO] " + falha.mensagem)
        return falha.codigo
    except Interrompido:
        if filho:
            log("[AVISO] sinal recebido; parando o filho %s." % filho)
            parar_filho(exe, filho)
        else:
            log("[AVISO] sinal recebido antes do filho existir.")
        return 143


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
