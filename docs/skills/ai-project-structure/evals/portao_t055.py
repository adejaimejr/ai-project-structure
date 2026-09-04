#!/usr/bin/env python3
"""Portao da T-055: o Modelo De Debate e o Modelo De Achado de docs/CONSENSUS.md da raiz
sao os do template.

1. O bloco cercado sob "## Modelo De Debate" da raiz e identico ao do asset.
2. Idem para "## Modelo De Achado".
3. O verificador cobra essa igualdade (cita "Modelo De Debate") e sai 0; raiz limpa em --strict.
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
    def modelo(texto, titulo):
        m = re.search(rf"^## {re.escape(titulo)}\s*$\s*```md\n(.*?)```", texto, re.M | re.S)
        return m.group(1) if m else None
    raiz = (ROOT / "docs" / "CONSENSUS.md").read_text(encoding="utf-8"); asset = (ASSETS / "docs" / "CONSENSUS.md").read_text(encoding="utf-8")
    for titulo in ("Modelo De Debate", "Modelo De Achado"):
        a_, b_ = modelo(raiz, titulo), modelo(asset, titulo)
        check(a_ is not None and a_ == b_, f"{titulo} da raiz identico ao do template", "ausente" if a_ is None else f"{len(a_)} vs {len(b_) if b_ else 0} bytes")
    vr = (EVALS / "verify_repository.py").read_text(encoding="utf-8"); check("Modelo De Debate" in vr, "3a. verificador cobra os modelos da raiz")
    code, out, _ = validar(ROOT, "--strict", "--codigos"); check(code == 0, "3b. raiz limpa em --strict", "; ".join(out)[:160])
    ok, resumo = verify_ok(); check(ok, "3c. verify_repository.py exit 0", resumo)

    total = 5
    print(f"\nPortao T-055: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
