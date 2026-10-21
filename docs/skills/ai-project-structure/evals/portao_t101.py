#!/usr/bin/env python3
"""Portao da T-101: bateria `evals/test_cloudroom_agente.py`, etapa no verificador e o
adaptador passando pelo `loop.sh` de ponta a ponta (spec 0008).

Escrito pelo agente de planejamento em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: nao ha bateria, nao ha etapa no verificador e nao ha adaptador para o loop chamar.

1. `evals/test_cloudroom_agente.py` existe, sai 0 e imprime `N/N verificacoes passaram` com N >= 20;
2. a bateria importa `mock_room_cli` e cobre o loop (cita `loop.sh` e `--tempo-maximo`);
3. `verify_repository.py` tem a etapa (cita `test_cloudroom_agente.py` e `CLOUDROOM_TESTES_MINIMO`)
   e fecha com ao menos 81 verificacoes em exit 0;
4. `loop.sh --agente "python3 <adaptador> --provider ... --intervalo 0.2"` no cenario `escreve`
   (o filho falso grava um arquivo no projeto) com portao que exige esse arquivo: exit 0, tarefa
   fechada e evidencia com `agente=` citando `cloudroom_agente.py`;
5. o mesmo com cenario `lento` e `--tempo-maximo 2`: exit 4 em poucos segundos e o `room-cli`
   falso recebeu `stop` (o SIGTERM do loop virou parada do filho).
"""

import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, EVALS, SKILL, check, ler, resumo, verify_ok  # noqa: E402
import mock_room_cli as mock  # noqa: E402

WRAPPER = SKILL / "scripts" / "cloudroom_agente.py"
LOOP = SKILL / "scripts" / "loop.sh"
BATERIA = EVALS / "test_cloudroom_agente.py"
VERIFICADOR = EVALS / "verify_repository.py"
PISO_BATERIA = 20
PISO_VERIFICADOR = 81
NUCLEO_DOCS = ("README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
               "CONSENSUS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md")
TASKS = """# TASKS

- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-01)`.

## Em Andamento

- T-019: Tarefa com portao declarado. (prioridade: alta) (verifica: bash portao.sh)

## Proximas Tarefas

- (Vazio.)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- 2026-08-10 T-001: Tarefa historica sem evidencia.
"""


def montar(tmp):
    root = Path(tmp) / "projeto"
    (root / "docs" / "archive").mkdir(parents=True)
    for nome in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / nome, root / nome)
    for nome in NUCLEO_DOCS:
        shutil.copy(ASSETS / "docs" / nome, root / "docs" / nome)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", root / "docs" / "archive" / "README.md")
    (root / "docs" / "TASKS.md").write_text(TASKS, encoding="utf-8")
    (root / "portao.sh").write_text("test -f trabalho-do-filho.txt\n", encoding="utf-8")
    return root


def rodar_loop(root, env, *extra, timeout=60):
    agente = "%s %s --provider claude-code --model claude-sonnet-5-5 --intervalo 0.2" % (
        Path(sys.executable).name, WRAPPER)
    inicio = time.monotonic()
    try:
        p = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(root), "--agente", agente, *extra],
                           capture_output=True, text=True, errors="replace", env=env, timeout=timeout)
        return p.returncode, p.stdout + p.stderr, time.monotonic() - inicio
    except subprocess.TimeoutExpired:
        return None, "loop.sh estourou %ss" % timeout, time.monotonic() - inicio


def main():
    total = 0
    ok_bateria = False
    if BATERIA.is_file():
        p = subprocess.run([sys.executable, str(BATERIA)], capture_output=True, text=True, errors="replace",
                           env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": Path(sys.executable).parent.as_posix() + ":" + __import__("os").environ["PATH"]})
        m = re.search(r"(\d+)/(\d+) verificacoes passaram", p.stdout)
        total = int(m.group(2)) if m else 0
        ok_bateria = p.returncode == 0 and total >= PISO_BATERIA and (int(m.group(1)) == total if m else False)
    check(ok_bateria, "1. evals/test_cloudroom_agente.py existe, sai 0 e tem ao menos %d verificacoes" % PISO_BATERIA,
          "ausente" if not BATERIA.is_file() else "%d verificacoes" % total)
    texto_bateria = ler(BATERIA) if BATERIA.is_file() else ""
    check("mock_room_cli" in texto_bateria and "loop.sh" in texto_bateria and "--tempo-maximo" in texto_bateria,
          "2. a bateria usa o room-cli falso e cobre o loop (cita loop.sh e --tempo-maximo)")

    texto_verificador = ler(VERIFICADOR)
    check("test_cloudroom_agente.py" in texto_verificador and "CLOUDROOM_TESTES_MINIMO" in texto_verificador,
          "3. verify_repository.py tem a etapa da bateria do adaptador com piso declarado")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        _, estado, env = mock.instalar(tmp, "escreve")
        codigo, saida, dur = rodar_loop(root, env) if WRAPPER.is_file() else (None, "adaptador ausente", 0)
        tasks = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        concluidas = tasks.split("## Concluidas")[1] if "## Concluidas" in tasks else ""
        fechou = "T-019" in concluidas and "agente=" in concluidas and "cloudroom_agente.py" in concluidas
        check(codigo == 0 and fechou and len(mock.por_comando(estado, "spawn")) == 1,
              "4. loop.sh com o adaptador como --agente: filho falso escreve no projeto, portao verde, tarefa fechada com agente= citando cloudroom_agente.py",
              "exit %s em %.1fs; %s" % (codigo, dur, saida.strip().splitlines()[-1][:120] if saida.strip() else ""))

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        _, estado, env = mock.instalar(tmp, "lento")
        codigo, saida, dur = rodar_loop(root, env, "--tempo-maximo", "2") if WRAPPER.is_file() else (None, "adaptador ausente", 0)
        check(codigo == 4 and dur < 25 and bool(mock.por_comando(estado, "stop")),
              "5. loop.sh --tempo-maximo 2 com filho lento: exit 4 em poucos segundos e o filho recebeu thread stop",
              "exit %s em %.1fs, stop=%s" % (codigo, dur, bool(mock.por_comando(estado, "stop"))))

    ok, detalhe = verify_ok()
    m = re.search(r"(\d+)/(\d+)", detalhe)
    n = int(m.group(2)) if m else 0
    check(ok and n >= PISO_VERIFICADOR, "6. verify_repository.py em exit 0 com ao menos %d verificacoes" % PISO_VERIFICADOR, detalhe)
    return resumo("T-101")


if __name__ == "__main__":
    sys.exit(main())
