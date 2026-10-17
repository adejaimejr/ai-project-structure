#!/usr/bin/env python3
"""Orquestra uma rodada mecanica de pareceres independentes.

Cada participante trabalha numa copia temporaria do projeto, fora dele, sem
`docs/consensus/`. O bruto e o manifesto entram no sidecar in-repo assim que
cada agente termina. Havendo posicao, a minuta entra no fim de CONSENSUS.md
por substituicao atomica, com julgamento em branco.

Somente biblioteca padrao (Python 3.8+).
"""

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

EXCLUIDOS_DA_COPIA = ["docs/consensus/", ".consenso-lock", "__pycache__/"]
IDS_RESERVADOS = {".", ".."}
TRAVESSAO = "\u2014"
LOCK_NOME = ".consenso-lock"

# Padroes minimos da T-077 / DEC-010. Palavra solta sem valor nao casa.
_RE_AWS = re.compile(r"AKIA[A-Z0-9]{16}")
_RE_PEM = re.compile(r"-----BEGIN[^\n]{0,80}PRIVATE KEY-----")
_RE_ROTULO = re.compile(
    r"(?i)(?:api_key|apikey|\btoken\b|\bsecret\b|\bpassword\b)\s*[=:]\s*\S{16,}"
)
# Prefixos exigem inicio de palavra e comprimento minimo: `sk-` solto casava
# `task-force`, `risk-based` e `desk-top` (falso positivo visto na revisao de T-077).
_RE_GHP = re.compile(r"\bghp_[A-Za-z0-9]{16,}")
_RE_SK = re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")
_RE_XOX = re.compile(r"\bxox[A-Za-z]-[A-Za-z0-9-]{8,}")
_RE_URL = re.compile(r"://[^/\s:]+:[^/\s@]+@")
PADROES_SEGREDO = (_RE_AWS, _RE_PEM, _RE_ROTULO, _RE_GHP, _RE_SK, _RE_XOX, _RE_URL)

# Estado da rodada corrente, para o handler de sinal enxergar os processos.
_interrompendo = threading.Event()
_processos_lock = threading.Lock()
_processos_vivos = []


def tem_segredo(texto):
    """True se o texto casa algum padrao minimo de segredo da T-077."""
    if texto is None:
        return False
    if isinstance(texto, bytes):
        texto = texto.decode("utf-8", "replace")
    if not texto:
        return False
    return any(padrao.search(texto) for padrao in PADROES_SEGREDO)


def reter_bruto_fora(stdout, stderr):
    """Guarda stdout e stderr fora do projeto. Nunca redige. Devolve o caminho."""
    destino = Path(tempfile.mkdtemp(prefix="consenso-retido-"))
    if not isinstance(stdout, bytes):
        stdout = stdout.encode("utf-8")
    if not isinstance(stderr, bytes):
        stderr = stderr.encode("utf-8")
    (destino / "stdout.txt").write_bytes(stdout)
    (destino / "stderr.txt").write_bytes(stderr)
    return destino


def avisar_retido(retido, projeto, run_id, identificador):
    print("Material retido por padrao de segredo: %s" % retido, file=sys.stderr)
    print("Conferir o material nesse diretorio.", file=sys.stderr)
    print("Para aceitar como esta, mova o diretorio para docs/consensus/%s/%s/."
          % (run_id, identificador), file=sys.stderr)
    print("Para descartar, apague. Depois: consenso.py retomar --projeto %s %s"
          % (projeto, run_id), file=sys.stderr)


def agora():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def soma(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def soma_texto(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def escrever_json(caminho, dados):
    """Grava o manifesto por substituicao atomica no mesmo diretorio."""
    escrever_bytes_atomico(caminho, json.dumps(dados, ensure_ascii=False, indent=2) + "\n")


def escrever_bytes_atomico(caminho, dados):
    """Temporario no mesmo diretorio, fsync e os.replace. Limpa o temporario."""
    caminho = Path(caminho)
    if isinstance(dados, str):
        dados = dados.encode("utf-8")
    temporario = caminho.parent / (".%s.%s.tmp" % (caminho.name, os.getpid()))
    try:
        with temporario.open("wb") as arquivo:
            arquivo.write(dados)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        os.replace(str(temporario), str(caminho))
    finally:
        if temporario.exists():
            temporario.unlink()


def ignorar_copia(projeto):
    projeto = Path(projeto).resolve()

    def ignorar(atual, nomes):
        removidos = {nome for nome in nomes if nome in {LOCK_NOME, "__pycache__"}}
        try:
            rel = Path(atual).resolve().relative_to(projeto)
        except ValueError:
            return removidos
        if rel.as_posix() == "docs" and "consensus" in nomes:
            removidos.add("consensus")
        return removidos

    return ignorar


def reter_registros(copia):
    """Esconde as entradas anteriores; os modelos cercados acima ficam."""
    caminho = Path(copia) / "docs" / "CONSENSUS.md"
    try:
        texto = caminho.read_text(encoding="utf-8")
    except OSError:
        return
    marcador = "## Registros"
    inicio = texto.find(marcador)
    if inicio < 0:
        return
    nota = (
        "## Registros\n\n"
        "> As entradas anteriores foram retidas de proposito por esta operacao.\n"
    )
    caminho.write_text(texto[:inicio] + nota, encoding="utf-8")


def prompt_do_participante(pergunta, participante, copia):
    return (
        "Participante: %s\n"
        "Copia isolada do projeto: %s\n"
        "Esta e uma copia somente-leitura do projeto: leia o que precisar. "
        "Nao edite nada fora da sua resposta.\n"
        "Responda em portugues, sem travessao. A resposta inteira no stdout "
        "sera reproduzida sem resumo. Nenhuma posicao contemporanea esta "
        "disponivel por construcao.\n\n"
        "Pergunta:\n\n"
        "%s"
    ) % (participante, copia, pergunta)


def executa(comando, prompt, copia):
    inicio = agora()
    try:
        processo = subprocess.Popen(
            comando + [prompt],
            cwd=str(copia),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as erro:
        return inicio, agora(), 127, b"", str(erro).encode("utf-8", "replace")
    with _processos_lock:
        _processos_vivos.append(processo)
    if _interrompendo.is_set():
        try:
            processo.terminate()
        except OSError:
            pass
    stdout, stderr = processo.communicate()
    with _processos_lock:
        if processo in _processos_vivos:
            _processos_vivos.remove(processo)
    return inicio, agora(), processo.returncode, stdout, stderr


def ao_sinal(signum, _frame):
    _interrompendo.set()
    with _processos_lock:
        alvos = list(_processos_vivos)
    for processo in alvos:
        try:
            processo.terminate()
        except OSError:
            pass
    # SIGINT: nao deixa o KeyboardInterrupt default furar o finally.
    if signum == signal.SIGINT:
        return


def sidecar_ignorado(projeto):
    """True quando o git trata docs/consensus/ como ignorado (DEC-008)."""
    if not (projeto / ".git").exists():
        return False
    processo = subprocess.run(
        ["git", "-C", str(projeto), "check-ignore", "-q", "docs/consensus/"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return processo.returncode == 0


def id_inseguro(identificador):
    if not identificador or identificador in IDS_RESERVADOS:
        return True
    return "/" in identificador or "\\" in identificador or os.sep in identificador


def adquirir_lock(projeto):
    lock_dir = Path(projeto) / LOCK_NOME
    try:
        os.mkdir(str(lock_dir))
    except FileExistsError:
        print("[ERRO] outra rodada ja esta em andamento neste projeto: lock em %s."
              % lock_dir, file=sys.stderr)
        print("Se uma rodada anterior terminou de forma inesperada e voce confirmou que",
              file=sys.stderr)
        print("nao ha rodada ativa, limpe o lock orfao com: rmdir \"%s\"" % lock_dir,
              file=sys.stderr)
        return None
    except OSError as erro:
        print("[ERRO] nao foi possivel criar o lock da rodada em %s: %s"
              % (lock_dir, erro), file=sys.stderr)
        return None
    return lock_dir


def soltar_lock(lock_dir):
    if lock_dir is None:
        return
    try:
        os.rmdir(str(lock_dir))
    except OSError:
        pass


def citar(texto):
    """Toda linha vira citacao Markdown; U+2014 vira hifen. Devolve (bloco, n)."""
    if texto is None:
        texto = ""
    n = texto.count(TRAVESSAO)
    texto = texto.replace(TRAVESSAO, "-")
    linhas = texto.splitlines()
    if not linhas:
        return "> \n", n
    return "\n".join("> " + linha for linha in linhas) + "\n", n


def montar_minuta(titulo, dono, run_id, pergunta, participantes, data):
    ids = [p["id"] for p in participantes]
    falhos = [p["id"] for p in participantes if p.get("resultado") != "posicao"]
    falhas_txt = ", ".join(falhos) if falhos else "nenhuma"
    manifesto_rel = "docs/consensus/%s/manifesto.json" % run_id
    partes = [
        "## %s - %s" % (data, titulo),
        "",
        "**Status:** aberto",
        "",
        "**Proximo passo:** %s le as posicoes e preenche as secoes de julgamento" % dono,
        "",
        "**Metodo:** pareceres-independentes",
        "",
        "**Exposicao previa a outras posicoes:** nao",
        "",
        "**Rodada:** 1 de 1",
        "",
        "**Origem:** automacao",
        "",
        "**Manifesto:** %s" % manifesto_rel,
        "",
        "**Participantes:** %s" % ", ".join(ids),
        "",
        "**Falhas:** %s" % falhas_txt,
        "",
        "### Contexto",
        "",
        "- Modo: debate",
        "- Rodada: 1 de 1",
        "- N: %s" % len(ids),
        "- Data: %s" % data,
        "- Manifesto: %s" % manifesto_rel,
        "",
        "### Pergunta Ou Decisao",
        "",
        citar(pergunta)[0].rstrip("\n"),
        "",
    ]
    for p in participantes:
        identificador = p["id"]
        if p.get("resultado") == "posicao":
            partes.extend([
                "### Posicao De %s" % identificador,
                "",
                citar(p.get("_stdout_texto", ""))[0].rstrip("\n"),
                "",
            ])
        else:
            bruto = "docs/consensus/%s/%s/" % (run_id, identificador)
            partes.extend([
                "### Falha De %s" % identificador,
                "",
                "- Exit: %s" % p.get("exit"),
                "- Bruto: %s" % bruto,
                "",
            ])
    for secao in (
        "Pontos De Acordo",
        "Riscos E Tradeoffs",
        "Consenso Final",
        "Decisao Para Registrar Em DECISIONS.md",
    ):
        partes.extend(["### %s" % secao, "", "- (A preencher.)", ""])
    return "\n".join(partes).rstrip() + "\n"


def gravar_minuta(projeto, minuta):
    """Acrescenta a minuta no fim, sem alterar o prefixo. Devolve hashes e o texto."""
    caminho = Path(projeto) / "docs" / "CONSENSUS.md"
    antes = caminho.read_text(encoding="utf-8")
    sha_antes = soma_texto(antes)
    adendo = ""
    if antes and not antes.endswith("\n"):
        adendo += "\n"
    adendo += "\n" + minuta.lstrip("\n")
    depois = antes + adendo
    escrever_bytes_atomico(caminho, depois.encode("utf-8"))
    return sha_antes, soma(caminho), "docs/CONSENSUS.md"


def run_debate(args):
    projeto = Path(args.projeto).resolve()
    pergunta_arquivo = Path(args.pergunta).resolve()
    participantes = args.agente or []
    if not projeto.is_dir():
        print("[ERRO] projeto nao encontrado: %s" % projeto, file=sys.stderr)
        return 1
    if not pergunta_arquivo.is_file():
        print("[ERRO] pergunta nao encontrada: %s" % pergunta_arquivo, file=sys.stderr)
        return 1
    if len(participantes) < 2:
        print("[ERRO] debate exige pelo menos dois --agente.", file=sys.stderr)
        return 1
    ids = [par[0] for par in participantes]
    if len(set(ids)) != len(ids) or any(id_inseguro(i) for i in ids):
        print("[ERRO] ids de participantes precisam ser distintos e seguros para diretorio.",
              file=sys.stderr)
        return 1
    trabalhos_cmd = []
    for identificador, texto_comando in participantes:
        comando = texto_comando.split()
        if not comando:
            print("[ERRO] comando vazio para %s." % identificador, file=sys.stderr)
            return 1
        trabalhos_cmd.append((identificador, comando))
    if sidecar_ignorado(projeto):
        print("[ERRO] docs/consensus/ esta ignorado pelo git; remova essa regra antes de rodar.",
              file=sys.stderr)
        return 1
    pergunta = pergunta_arquivo.read_text(encoding="utf-8")
    if tem_segredo(pergunta):
        print("[ERRO] a pergunta contem padrao de segredo; nenhum agente foi chamado.",
              file=sys.stderr)
        print("Conferir o arquivo da pergunta. Nada foi gravado em docs/consensus/.",
              file=sys.stderr)
        return 6

    lock_dir = adquirir_lock(projeto)
    if lock_dir is None:
        return 5

    anteriores = {
        signal.SIGINT: signal.getsignal(signal.SIGINT),
        signal.SIGTERM: signal.getsignal(signal.SIGTERM),
    }
    _interrompendo.clear()
    with _processos_lock:
        _processos_vivos.clear()
    try:
        signal.signal(signal.SIGINT, ao_sinal)
        signal.signal(signal.SIGTERM, ao_sinal)
        return _rodar_debate(args, projeto, pergunta_arquivo, participantes, trabalhos_cmd)
    finally:
        for sig, handler in anteriores.items():
            try:
                signal.signal(sig, handler)
            except (OSError, ValueError):
                pass
        soltar_lock(lock_dir)


def _rodar_debate(args, projeto, pergunta_arquivo, participantes, trabalhos_cmd):
    pergunta = pergunta_arquivo.read_text(encoding="utf-8")
    base = projeto / "docs" / "consensus"
    instante = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    run_id = "%s-debate" % instante
    rodada = base / run_id
    if rodada.exists():
        print("[ERRO] rodada ja existe: %s" % rodada, file=sys.stderr)
        return 1
    try:
        rodada.mkdir(parents=True)
    except OSError as erro:
        print("[ERRO] nao foi possivel criar sidecar: %s" % erro, file=sys.stderr)
        return 1

    manifesto = {
        "versao": 1,
        "run_id": run_id,
        "modo": "debate",
        "rodada": 1,
        "projeto": str(projeto),
        "inicio": agora(),
        "fim": None,
        "status": "em-andamento",
        "pergunta": {"arquivo": str(pergunta_arquivo), "sha256": soma(pergunta_arquivo)},
        "excluidos_da_copia": list(EXCLUIDOS_DA_COPIA),
        "participantes": [],
        "minuta": None,
    }
    (rodada / "pergunta.txt").write_bytes(pergunta_arquivo.read_bytes())
    escrever_json(rodada / "manifesto.json", manifesto)

    stdout_por_id = {}
    temporarios = []
    trabalhos = []
    try:
        for identificador, comando in trabalhos_cmd:
            if _interrompendo.is_set():
                break
            raiz_temporaria = Path(tempfile.mkdtemp(prefix="consenso-"))
            temporarios.append(raiz_temporaria)
            copia = raiz_temporaria / "projeto"
            shutil.copytree(str(projeto), str(copia), ignore=ignorar_copia(projeto))
            reter_registros(copia)
            prompt = prompt_do_participante(pergunta, identificador, copia)
            trabalhos.append((identificador, comando, str(copia), prompt))

        if trabalhos and not _interrompendo.is_set():
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(trabalhos)) as executor:
                futuros = {
                    executor.submit(executa, comando, prompt, copia): (
                        identificador, comando, copia, prompt)
                    for identificador, comando, copia, prompt in trabalhos
                }
                for futuro in concurrent.futures.as_completed(futuros):
                    identificador, comando, copia, prompt = futuros[futuro]
                    inicio, fim, codigo, stdout, stderr = futuro.result()
                    destino = rodada / identificador
                    destino.mkdir(exist_ok=True)
                    prompt_path = destino / "prompt.txt"
                    prompt_path.write_text(prompt, encoding="utf-8")
                    if tem_segredo(stdout) or tem_segredo(stderr):
                        retido = reter_bruto_fora(stdout, stderr)
                        avisar_retido(retido, projeto, run_id, identificador)
                        registro = {
                            "id": identificador,
                            "comando": comando,
                            "diretorio": copia,
                            "inicio": inicio,
                            "fim": fim,
                            "exit": codigo,
                            "prompt": "%s/prompt.txt" % identificador,
                            "sha256_prompt": soma(prompt_path),
                            "resultado": "retido-por-segredo",
                            "retido_em": str(retido),
                        }
                        manifesto["participantes"].append(registro)
                        escrever_json(rodada / "manifesto.json", manifesto)
                        continue
                    stdout_path = destino / "stdout.txt"
                    stderr_path = destino / "stderr.txt"
                    stdout_path.write_bytes(stdout)
                    stderr_path.write_bytes(stderr)
                    stdout_texto = stdout.decode("utf-8", "replace")
                    stdout_por_id[identificador] = stdout_texto
                    registro = {
                        "id": identificador,
                        "comando": comando,
                        "diretorio": copia,
                        "inicio": inicio,
                        "fim": fim,
                        "exit": codigo,
                        "prompt": "%s/prompt.txt" % identificador,
                        "sha256_prompt": soma(prompt_path),
                        "stdout": "%s/stdout.txt" % identificador,
                        "sha256_stdout": soma(stdout_path),
                        "stderr": "%s/stderr.txt" % identificador,
                        "resultado": "posicao" if codigo == 0 else "falha",
                        "travessoes_substituidos": stdout_texto.count(TRAVESSAO),
                    }
                    manifesto["participantes"].append(registro)
                    escrever_json(rodada / "manifesto.json", manifesto)
    finally:
        for temporario in temporarios:
            shutil.rmtree(str(temporario), ignore_errors=True)

    ordem = {identificador: indice for indice, (identificador, _) in enumerate(participantes)}
    manifesto["participantes"].sort(key=lambda p: ordem.get(p["id"], 999))
    manifesto["fim"] = agora()

    if _interrompendo.is_set():
        manifesto["status"] = "interrompida"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada interrompida: %s" % run_id, file=sys.stderr)
        return 1

    tem_retido = any(p.get("resultado") == "retido-por-segredo"
                     for p in manifesto["participantes"])
    if tem_retido:
        manifesto["status"] = "parada-segredo"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada parada por segredo: %s" % run_id, file=sys.stderr)
        return 6

    tem_posicao = any(p["resultado"] == "posicao" for p in manifesto["participantes"])
    if not tem_posicao:
        manifesto["status"] = "sem-posicao"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada sem posicao: %s" % run_id, file=sys.stderr)
        return 2

    if _interrompendo.is_set():
        manifesto["status"] = "interrompida"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada interrompida: %s" % run_id, file=sys.stderr)
        return 1

    data = dt.date.today().isoformat()
    for p in manifesto["participantes"]:
        p["_stdout_texto"] = stdout_por_id.get(p["id"], "")
    minuta = montar_minuta(args.titulo, args.dono, run_id, pergunta,
                           manifesto["participantes"], data)
    for p in manifesto["participantes"]:
        p.pop("_stdout_texto", None)

    if _interrompendo.is_set():
        manifesto["status"] = "interrompida"
        escrever_json(rodada / "manifesto.json", manifesto)
        print("Rodada interrompida: %s" % run_id, file=sys.stderr)
        return 1

    sha_antes, sha_depois, arquivo = gravar_minuta(projeto, minuta)
    manifesto["minuta"] = {
        "arquivo": arquivo,
        "entrada": "%s - %s" % (data, args.titulo),
        "sha256_antes": sha_antes,
        "sha256_depois": sha_depois,
    }
    manifesto["status"] = "concluida"
    escrever_json(rodada / "manifesto.json", manifesto)
    print("Rodada concluida: %s" % run_id)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Automacao mecanica de consenso.")
    subcomandos = parser.add_subparsers(dest="subcomando", required=True)
    debate = subcomandos.add_parser("debate", help="Roda pareceres independentes.")
    debate.add_argument("--projeto", default=".")
    debate.add_argument("--pergunta", required=True)
    debate.add_argument("--agente", action="append", nargs=2, metavar=("ID", "COMANDO"))
    debate.add_argument("--titulo", default="Debate")
    debate.add_argument("--dono", default="usuario")
    args = parser.parse_args(argv)
    return run_debate(args)


if __name__ == "__main__":
    sys.exit(main())
