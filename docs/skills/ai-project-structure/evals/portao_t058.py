#!/usr/bin/env python3
"""Portao da T-058: duas rodadas simultaneas no mesmo projeto nao correm em TASKS.md.

1. Duas execucoes de loop.sh na mesma tarefa ao mesmo tempo: exatamente uma segue; a outra sai
   diferente de zero em poucos segundos e a mensagem cita o lock.
2. Terminada a rodada, nenhum lock fica para tras; a proxima execucao roda normalmente.
3. test_loop.py tem caso de lock; references/loop.md documenta a restricao; verify exit 0; versao coerente.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ROOT = SKILL.parents[2]
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


def montar(tmp, nome, data="2026-09-01"):
    r = Path(tmp) / nome
    (r / "docs" / "archive").mkdir(parents=True)
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / f, r / f)
    for f in NUCLEO:
        shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
    t = r / "docs" / "TASKS.md"
    t.write_text(t.read_text(encoding="utf-8").replace("(convencoes-2-2-0-desde: AAAA-MM-DD)", f"(convencoes-2-2-0-desde: {data})"), encoding="utf-8")
    return r


def validar(r, *flags):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(r), *flags], capture_output=True, text=True, errors="replace")
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()], p.stderr


def versao_coerente(acima_de):
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    ok_acima = tuple(int(x) for x in versao.split(".")) >= tuple(int(x) for x in acima_de.split("."))
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    partes = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8").split("\n## ", 2)
    recente = partes[1] if len(partes) > 1 else ""
    return versao, ok_acima and prosa == {versao} and marcadores == {versao} and recente.startswith(versao), recente, f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}"


def verify_ok():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True, env=env)
    return p.returncode == 0, next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")


def main():
    LOOP = SKILL / "scripts" / "loop.sh"
    TASKS = "# TASKS\n\n- `(convencoes-2-2-0-desde: 2026-09-01)`\n\n## Em Andamento\n\n- T-019: Alvo. (verifica: bash portao.sh)\n\n## Proximas Tarefas\n\n- (Vazio.)\n\n## Aguardando Usuario\n\n- (Vazio.)\n\n## Concluidas\n\n- (Vazio.)\n"
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "c1"); (r / "docs" / "TASKS.md").write_text(TASKS, encoding="utf-8"); (r / "portao.sh").write_text("exit 0\n", encoding="utf-8")
        ag = Path(tmp) / "agente-lento"; ag.write_text("#!/usr/bin/env bash\nsleep 4\n", encoding="utf-8"); ag.chmod(0o755)
        env = dict(os.environ, PATH=f"{ag.parent}{os.pathsep}{os.environ['PATH']}", PYTHONDONTWRITEBYTECODE="1")
        a = subprocess.Popen(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(r), "--agente", ag.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, stdin=subprocess.DEVNULL)
        import time; time.sleep(1.0)
        try:
            b = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(r), "--agente", ag.name], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL, timeout=3)
            b_code, b_out = b.returncode, b.stdout + b.stderr
        except subprocess.TimeoutExpired:
            # Sem lock, a segunda execucao entra e fica esperando o agente: e o defeito.
            b_code, b_out = None, "(segunda execucao nao foi recusada; seguiu em paralelo)"
        sa, _ = a.communicate(timeout=60)
        texto = (r / "docs" / "TASKS.md").read_text(encoding="utf-8")
        check(b_code is not None and b_code != 0 and "lock" in norm(b_out), "1a. segunda execucao simultanea e recusada citando o lock", f"exit {b_code}; " + b_out.strip().replace("\n", " ")[-140:])
        check(a.returncode == 0 and texto.count("T-019") == 1 and "Evidencia:" in texto, "1b. primeira execucao segue e fecha a tarefa uma vez", f"exit {a.returncode}")
        sobras = [p.name for p in r.iterdir() if "lock" in p.name.lower()]
        check(not sobras, "2a. nenhum lock fica para tras", ", ".join(sobras))
        (r / "docs" / "TASKS.md").write_text(TASKS, encoding="utf-8")
        ag2 = Path(tmp) / "agente-rapido"; ag2.write_text("#!/usr/bin/env bash\ntrue\n", encoding="utf-8"); ag2.chmod(0o755)
        c = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(r), "--agente", ag2.name], capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
        check(c.returncode == 0, "2b. proxima execucao roda normalmente", f"exit {c.returncode}")
    tl = (EVALS / "test_loop.py").read_text(encoding="utf-8"); check("lock" in tl.lower(), "3a. test_loop.py cobre o lock")
    lm = norm((SKILL / "references" / "loop.md").read_text(encoding="utf-8")); check("lock" in lm and "simultane" in lm, "3b. loop.md documenta o lock e a rodada simultanea")
    versao, ok, recente, det = versao_coerente("2.10.0"); check(ok, "3c. versao 2.10.0 ou acima, coerente", det)
    ok, resumo = verify_ok(); check(ok, "3d. verify_repository.py exit 0", resumo)

    total = 8
    print(f"\nPortao T-058: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
