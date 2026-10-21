#!/usr/bin/env python3
"""Portao da T-100: `scripts/cloudroom_agente.py`, adaptador que faz um filho do Cloudroom
se comportar como CLI headless para `loop.sh` (spec 0008).

Escrito pelo agente de planejamento em 2026-10-21, antes de qualquer codigo, contra o
`room-cli` falso de `evals/mock_room_cli.py` (que imita o que a CLI real respondeu nas
sondas do mesmo dia). Hoje falha pelo motivo certo: o script nao existe.

Contrato cobrado (DEC-001, DEC-004, DEC-006 e DEC-007 da spec 0008):
1. o script existe, compila, usa so biblioteca padrao e nao contem `sed -i`, `perl`,
   `timeout ` nem `setsid`;
2. `--help` sai 0 e documenta `--titulo`, `--arquivar`, `--intervalo` e os exit codes 0, 1, 2 e 143;
3. sem `room-cli` no PATH: exit 1 antes de qualquer coisa, mensagem cita `room-cli`, nada chamado;
4. cenario `ok`: exit 0, stdout e exatamente a resposta do filho mais quebra de linha; o spawn
   recebeu `--provider`, `--model`, `--shared-sandbox` (acrescentado pelo adaptador) e
   `--prompt-file` cujo conteudo e o prompt inteiro (100KB, com quebras e `--` dentro); a
   leitura usou `--all`; stderr registra `thread=<id>`;
4b. cenario `pergunta`: o filho que pergunta em vez de responder sai 0 com a pergunta no stdout
   (o adaptador nao distingue; quem decide e o portao da tarefa);
5. cenario `longo`: stdout traz a resposta inteira, sem o aviso de corte;
6. cenario `falha`: exit 2, stderr cita o erro do filho, stdout vazio;
7. cenario `lento` mais SIGTERM no adaptador: `room-cli thread stop <id>` em ate 5 s e exit 143;
8. titulo: `--titulo` vira `--title`; sem ele, prompt com `T-NNN` gera titulo com o T-NNN;
9. `--arquivar` chama `thread archive` depois de ler a resposta; sem a flag, nao chama;
10. `--top-level`, `--prompt` e `--prompt-file` vindos de fora sao recusados com exit 1, sem spawn;
11. prompt acima de 262144 bytes: a CLI recusa e o adaptador sai 1 sem consultar nada.
"""

import ast
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import SKILL, check, ler, resumo  # noqa: E402
import mock_room_cli as mock  # noqa: E402

WRAPPER = SKILL / "scripts" / "cloudroom_agente.py"
# Revisao do gpt-6-luna em 2026-10-21: a CLI aceita mais flags (como --request-id), e o mock tambem;
# o adaptador so pode usar as que a DEC-003 e a DEC-006 da spec 0008 preveem.
PERMITIDAS_NO_SPAWN = {"--provider", "--model", "--shared-sandbox", "--prompt-file", "--title"}
PROMPT = ("Voce esta trabalhando no projeto.\nSua tarefa e a T-019, descrita em docs/TASKS.md.\n"
          "-- linha com dois hifens --\n--provider dentro do texto nao e flag\n"
          "acentuacao: coracao, acao\n" + ("x" * 100000) + "\nfim do prompt\n")


def rodar(env, *args, prompt=PROMPT, timeout=60):
    if not WRAPPER.is_file():
        return None, "", "scripts/cloudroom_agente.py ausente"
    try:
        p = subprocess.run([sys.executable, str(WRAPPER), *args, prompt], capture_output=True, text=True,
                           errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return None, "", "adaptador estourou %ss" % timeout


def main():
    existe = WRAPPER.is_file()
    fonte = ler(WRAPPER) if existe else ""
    compila = False
    so_stdlib = False
    if existe:
        try:
            arvore = ast.parse(fonte)
            compila = True
            modulos = set()
            for no in ast.walk(arvore):
                if isinstance(no, ast.Import):
                    modulos.update(a.name.split(".")[0] for a in no.names)
                elif isinstance(no, ast.ImportFrom) and no.module:
                    modulos.add(no.module.split(".")[0])
            stdlib = getattr(sys, "stdlib_module_names", None)
            so_stdlib = all(m in stdlib for m in modulos) if stdlib else True
        except SyntaxError:
            pass
    check(existe and compila and so_stdlib, "1. scripts/cloudroom_agente.py existe, compila e importa so biblioteca padrao",
          "ausente" if not existe else ("nao compila" if not compila else ("import fora da stdlib" if not so_stdlib else "")))
    check(existe and not re.search(r"sed -i|\bperl\b|\btimeout \d|\bsetsid\b", fonte),
          "1b. sem sed -i, perl, timeout(1) ou setsid (portabilidade nos tres sistemas)")

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        codigo, out, err = rodar(env, "--help", prompt="ignorado") if existe else (None, "", "")
        ajuda = out + err
        check(codigo == 0 and all(t in ajuda for t in ("--titulo", "--arquivar", "--intervalo", "room-cli thread spawn"))
              and re.search(r"\b143\b", ajuda) and re.search(r"\b2\b", ajuda),
              "2. --help sai 0 e documenta --titulo, --arquivar, --intervalo e os exit codes (0, 1, 2, 143)")

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        # PATH vazio, e nao "o PATH sem o falso": o room-cli real pode estar em /usr/local/bin
        # e abriria um filho de verdade, gastando modelo, quando o adaptador existir.
        vazio = Path(tmp) / "path-vazio"
        vazio.mkdir()
        env["PATH"] = str(vazio)
        codigo, out, err = rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        check(codigo == 1 and "room-cli" in err and not mock.chamadas(estado) and not out.strip(),
              "3. sem room-cli no PATH: exit 1 antes de qualquer coisa, mensagem cita room-cli, nada chamado",
              "exit %s" % codigo)

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok", resposta="RESPOSTA-OK TOKEN-100\nsegunda linha")
        codigo, out, err = rodar(env, "--provider", "claude-code", "--model", "claude-sonnet-5-5", "--intervalo", "0.2")
        spawns = mock.por_comando(estado, "spawn")
        args = spawns[0]["args"] if spawns else []
        flags = [x for x in args if x.startswith("--")]
        outputs = mock.por_comando(estado, "output")
        check(codigo == 0 and out == "RESPOSTA-OK TOKEN-100\nsegunda linha\n",
              "4. cenario ok: exit 0 e stdout e exatamente a resposta do filho mais quebra de linha",
              "exit %s, stdout=%r" % (codigo, out[:80]))
        check(len(spawns) == 1 and "--provider" in args and "claude-code" in args and "--model" in args
              and "claude-sonnet-5-5" in args and "--shared-sandbox" in args and "--prompt-file" in args
              and "--prompt" not in args and set(flags) <= PERMITIDAS_NO_SPAWN and len(flags) == len(set(flags)),
              "4a. um spawn so, com --provider, --model, --shared-sandbox acrescentado e --prompt-file (nunca --prompt), "
              "e nenhuma flag alem dessas e de --title, cada uma uma vez",
              "flags=%s" % flags)
        check(spawns and spawns[0]["prompt"] == PROMPT, "4b. o conteudo do --prompt-file e o prompt inteiro, byte a byte (100KB, quebras, `--` dentro)")
        check(outputs and all(c.get("all") for c in outputs[-1:]), "4c. a leitura final da resposta usou --all",
              "%d consultas" % len(outputs))
        check("thread=cr_child_mock1" in err, "4d. stderr registra thread=<id> do filho", err.strip()[-160:])

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "pergunta")
        codigo, out, err = rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        check(codigo == 0 and mock.RESPOSTA_PERGUNTA in out,
              "4e. filho que pergunta em vez de responder: exit 0 com a pergunta no stdout (quem decide e o portao da tarefa)")

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "longo")
        codigo, out, err = rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        check(codigo == 0 and "FIM-DA-RESPOSTA-LONGA" in out and "truncated" not in out and len(out) > 19000,
              "5. cenario longo: stdout traz a resposta inteira, sem aviso de corte", "len=%d" % len(out))

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "falha")
        codigo, out, err = rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        check(codigo == 2 and mock.ERRO_FALHA in err and not out.strip(),
              "6. cenario falha: exit 2, stderr cita o erro do filho, stdout vazio", "exit %s" % codigo)

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "lento")
        if existe:
            p = subprocess.Popen([sys.executable, str(WRAPPER), "--provider", "claude-code", "--intervalo", "0.2", PROMPT],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, stdin=subprocess.DEVNULL)
            limite = time.monotonic() + 10
            while time.monotonic() < limite and not mock.por_comando(estado, "output"):
                time.sleep(0.1)
            p.send_signal(signal.SIGTERM)
            inicio = time.monotonic()
            try:
                p.communicate(timeout=8)
                codigo = p.returncode
            except subprocess.TimeoutExpired:
                p.kill()
                p.communicate()
                codigo = None
            demora = time.monotonic() - inicio
            parou = bool(mock.por_comando(estado, "stop"))
        else:
            codigo, demora, parou = None, 0, False
        check(codigo == 143 and parou and demora < 5,
              "7. cenario lento + SIGTERM: room-cli thread stop em ate 5 s e exit 143",
              "exit %s, stop=%s, %.1fs" % (codigo, parou, demora))

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        rodar(env, "--provider", "claude-code", "--intervalo", "0.2", "--titulo", "titulo explicito")
        rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        rodar(env, "--provider", "claude-code", "--intervalo", "0.2", prompt="Primeira linha sem tarefa\nsegunda")
        spawns = mock.por_comando(estado, "spawn")
        titulos = [s.get("title") or "" for s in spawns]
        check(len(titulos) == 3 and titulos[0] == "titulo explicito" and "T-019" in titulos[1]
              and titulos[2].startswith("Primeira linha sem tarefa") and len(titulos[2]) <= 80,
              "8. titulo: --titulo passa como --title; sem ele, T-NNN do prompt; senao a primeira linha, ate 80 caracteres",
              "titulos=%s" % titulos)

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        rodar(env, "--provider", "claude-code", "--intervalo", "0.2", "--arquivar")
        ordem = [c["cmd"] for c in mock.chamadas(estado)]
        arquiva = "archive" in ordem and ordem.index("archive") > max(i for i, c in enumerate(ordem) if c == "output")
        rodar(env, "--provider", "claude-code", "--intervalo", "0.2")
        depois = [c["cmd"] for c in mock.chamadas(estado)]
        check(arquiva and depois.count("archive") == 1,
              "9. --arquivar chama thread archive depois da ultima leitura; sem a flag, nao chama", "ordem=%s" % ordem)

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        c1, _, e1 = rodar(env, "--provider", "claude-code", "--top-level", "--intervalo", "0.2")
        c2, _, e2 = rodar(env, "--provider", "claude-code", "--prompt", "x", "--intervalo", "0.2")
        c3, _, e3 = rodar(env, "--provider", "claude-code", "--prompt-file", "/tmp/x", "--intervalo", "0.2")
        check((c1, c2, c3) == (1, 1, 1) and not mock.por_comando(estado, "spawn"),
              "10. --top-level, --prompt e --prompt-file vindos de fora: exit 1 sem spawn", "exits=%s" % ((c1, c2, c3),))

    with tempfile.TemporaryDirectory() as tmp:
        _, estado, env = mock.instalar(tmp, "ok")
        # O Linux limita cada argumento a 131072 bytes (MAX_ARG_STRLEN): um prompt de 262145 bytes
        # nao passa por exec. Achado pelo subagente da T-100 em 2026-10-21. O prompt vai por arquivo
        # e o adaptador roda por runpy num subprocesso, com o argv montado dentro dele: continua caixa-preta.
        grande = Path(tmp) / "prompt-grande.txt"
        grande.write_text("y" * (mock.LIMITE_PROMPT + 1), encoding="utf-8")
        ponte = ("import runpy, sys\n"
                 "w, f = sys.argv[1], sys.argv[2]\n"
                 "sys.argv = [w, '--provider', 'claude-code', '--intervalo', '0.2', open(f, encoding='utf-8').read()]\n"
                 "runpy.run_path(w, run_name='__main__')\n")
        if existe:
            p = subprocess.run([sys.executable, "-c", ponte, str(WRAPPER), str(grande)], capture_output=True, text=True,
                               errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=60)
            codigo, out, err = p.returncode, p.stdout, p.stderr
        else:
            codigo, out, err = None, "", ""
        check(codigo == 1 and not mock.por_comando(estado, "output") and "262144" in err,
              "11. prompt acima de 262144 bytes: a CLI recusa, o adaptador sai 1 com a mensagem e nao consulta nada",
              "exit %s" % codigo)

    return resumo("T-100")


if __name__ == "__main__":
    sys.exit(main())
