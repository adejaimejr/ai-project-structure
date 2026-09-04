#!/usr/bin/env python3
"""Portao da T-071: o bloco core diz o alcance real de duas regras.

Tarefa de texto no `assets/AGENTS.md`. Nao roda o `verify_repository.py`
porque a propagacao para o `AGENTS.md` da raiz e do agente de chat, depois da
rodada. Cobra:

1. O item do bloco core sobre o travessao diz onde ele e acusado: cita
   `docs/` e as pontes (`CLAUDE.md`), e nao promete "qualquer texto".
2. A secao "Arquivos-Ponte Sao Imutaveis" diz o que o validador confere de
   fato (a mencao a `AGENTS.md`) e que o resto da regra e leitura, nao script.
3. O aviso do ponto cego continua em ate 4 linhas (criterio da spec 0005).
4. A secao mais recente do `CHANGELOG.md` da skill registra a mudanca de
   texto (cita travessao e ponte) e a versao continua coerente entre
   `SKILL.md`, prosa, marcadores dos assets e CHANGELOG.
5. Um projeto montado de `assets/` passa em `--strict`, e a raiz tambem.
"""

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


def secao(texto, titulo):
    m = re.search(rf"^## {re.escape(titulo)}\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    return m.group(1) if m else ""


def main():
    core_texto = (ASSETS / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(r"core:start.*?core:end", core_texto, re.S)
    core = m.group(0) if m else ""

    linha_travessao = next((l for l in core.splitlines() if "travess" in norm(l) and "nunca use" in norm(l)), "")
    n = norm(linha_travessao)
    check(bool(linha_travessao) and "docs/" in n and "claude.md" in n and "qualquer" not in n.replace("qualquer ocorrencia", ""),
          "1. item do travessao diz o alcance (docs/ e pontes) e nao promete qualquer texto", linha_travessao[:160])

    pontes = norm(secao(core, "Arquivos-Ponte Sao Imutaveis"))
    check("validador" in pontes and "agents.md" in pontes and ("mencao" in pontes or "menciona" in pontes or "cita" in pontes),
          "2. secao das pontes diz o que o validador confere de fato")

    m2 = re.search(r"^### Ponto Cego Da Validacao Cruzada\s*$(.*?)(?=^#{2,3} |\Z)", core, re.M | re.S)
    linhas = [l for l in (m2.group(1) if m2 else "").splitlines() if l.strip()]
    check(m2 is not None and len(linhas) <= 4, "3. aviso do ponto cego em ate 4 linhas", f"{len(linhas)} linhas")

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    changelog = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8")
    partes = changelog.split("\n## ", 2)
    recente = partes[1] if len(partes) > 1 else ""
    check(recente.startswith(versao) and "travess" in norm(recente) and "ponte" in norm(recente)
          and prosa == {versao} and marcadores == {versao},
          "4. CHANGELOG mais recente registra travessao e ponte, versao coerente",
          f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}")

    with tempfile.TemporaryDirectory() as tmp:
        r = Path(tmp) / "limpo"
        (r / "docs" / "archive").mkdir(parents=True)
        for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            shutil.copy(ASSETS / f, r / f)
        for f in NUCLEO:
            shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
        shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
        t = r / "docs" / "TASKS.md"
        t.write_text(t.read_text(encoding="utf-8").replace("(convencoes-2-2-0-desde: AAAA-MM-DD)", "(convencoes-2-2-0-desde: 2026-09-01)"), encoding="utf-8")
        p = subprocess.run([sys.executable, str(VALIDATOR), str(r), "--strict", "--codigos"], capture_output=True, text=True)
        check(p.returncode == 0 and not p.stdout.strip(), "5a. projeto limpo montado de assets passa em --strict", p.stdout.strip()[:200])
    p = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), "--strict", "--codigos"], capture_output=True, text=True)
    check(p.returncode == 0, "5b. raiz do repositorio limpa em --strict", p.stdout.strip()[:200])

    total = 6
    print(f"\nPortao T-071: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
