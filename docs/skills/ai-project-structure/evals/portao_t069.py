#!/usr/bin/env python3
"""Portao da T-069: os seis checks de nivel ERRO decididos em T-059.

Cobra comportamento, nao nome de codigo: cada caso monta um projeto minimo a
partir de `assets/`, injeta o defeito e exige que `validate_structure.py` saia
1 com pelo menos um ERRO no arquivo certo. Um projeto limpo montado do mesmo
jeito precisa continuar limpo em `--strict`, para o conserto nao virar falso
positivo. Por fim, exige o bump de versao que a tarefa declara e o verificador
geral em exit 0 (que, desde a T-065, ja obriga cada codigo novo a ter fixture).

Casos:

1. linha em "Concluidas" sem prefixo de data;
2. marcador verifica com comando vazio;
3. marcadores `core` com `end` antes de `start`;
4. bloco `loop` com `start` sem `end` e sem versao;
5. arquivo do nucleo com zero bytes;
6. `T-001` no arquivo vivo e `T-001` em `docs/archive/TASKS-*.md`.

Vive em `evals/`, nao e distribuido. Somente biblioteca padrao.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
VERSAO_ANTES = "2.5.1"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def montar(tmp, nome):
    r = Path(tmp) / nome
    (r / "docs" / "archive").mkdir(parents=True)
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / f, r / f)
    for f in NUCLEO:
        shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
    tasks = r / "docs" / "TASKS.md"
    tasks.write_text(tasks.read_text(encoding="utf-8").replace(
        "(convencoes-2-2-0-desde: AAAA-MM-DD)", "(convencoes-2-2-0-desde: 2026-09-01)"),
        encoding="utf-8")
    return r


def validar(r, strict=False):
    cmd = [sys.executable, str(VALIDATOR), str(r), "--codigos"] + (["--strict"] if strict else [])
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()]


def erro_em(linhas, arquivo):
    return [l for l in linhas if l.startswith("ERRO|") and l.split("|")[2] == arquivo]


def concluir(r, linha):
    t = (r / "docs" / "TASKS.md").read_text(encoding="utf-8")
    (r / "docs" / "TASKS.md").write_text(
        t.replace("- (Vazio. Ao concluir", linha + "\n- (Vazio. Ao concluir"), encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # 0. controle: projeto limpo continua limpo
        r = montar(tmp, "limpo")
        code, out = validar(r, strict=True)
        check(code == 0 and not out, "controle: projeto limpo montado de assets passa em --strict",
              "; ".join(out)[:200])

        # 1. concluida sem data
        r = montar(tmp, "c1")
        concluir(r, "- T-009: Concluida sem data e sem evidencia.")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "docs/TASKS.md"), "1. concluida sem data e ERRO em TASKS.md", "; ".join(out)[:200])

        # 2. verifica vazio
        r = montar(tmp, "c2")
        concluir(r, "- 2026-09-03 T-009: Fechou com verifica vazio. (verifica: )\n  - Evidencia: tipo=comando; procedimento=nada; resultado=ok")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "docs/TASKS.md"), "2. marcador verifica vazio e ERRO em TASKS.md", "; ".join(out)[:200])

        # 3. marcadores invertidos
        r = montar(tmp, "c3")
        ag = r / "AGENTS.md"
        t = ag.read_text(encoding="utf-8")
        s = re.search(r"<!-- ai-project-structure:core:start v[\d.]+ -->", t).group(0)
        e = "<!-- ai-project-structure:core:end -->"
        ag.write_text(t.replace(s, "@@S@@").replace(e, "@@E@@").replace("@@S@@", e).replace("@@E@@", s), encoding="utf-8")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "AGENTS.md"), "3. marcadores core invertidos e ERRO em AGENTS.md", "; ".join(out)[:200])

        # 4. bloco loop despareado e sem versao
        r = montar(tmp, "c4")
        ag = r / "AGENTS.md"
        ag.write_text(ag.read_text(encoding="utf-8").replace(
            "## Regras Do Projeto",
            "<!-- ai-project-structure:loop:start -->\n## Loop\n\nsem fim\n\n## Regras Do Projeto"), encoding="utf-8")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "AGENTS.md"), "4. bloco loop sem end e sem versao e ERRO em AGENTS.md", "; ".join(out)[:200])

        # 5. arquivo do nucleo vazio
        r = montar(tmp, "c5")
        (r / "docs" / "SESSION.md").write_text("", encoding="utf-8")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "docs/SESSION.md"), "5. SESSION.md com zero bytes e ERRO em SESSION.md", "; ".join(out)[:200])

        # 6. ID repetido no archive
        r = montar(tmp, "c6")
        (r / "docs" / "archive" / "TASKS-2025.md").write_text(
            "# TASKS 2025\n\n## Concluidas\n\n- 2025-01-01 T-001: antiga.\n", encoding="utf-8")
        code, out = validar(r)
        check(code == 1 and erro_em(out, "docs/TASKS.md"), "6. T-001 vivo e no archive e ERRO em TASKS.md", "; ".join(out)[:200])

    # 7. bump de versao declarado pela tarefa
    fm = re.search(r'^version:\s*"?([\d.]+)"?', (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.M)
    versao = fm.group(1) if fm else "?"
    check(versao != VERSAO_ANTES and versao > VERSAO_ANTES, f"SKILL.md com versao acima de {VERSAO_ANTES}", f"encontrada {versao}")

    # 8. verificador geral (cobertura por codigo, paridade dos blocos, versao coerente)
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "verify_repository.py exit 0", resumo)

    total = 9
    print(f"\nPortao T-069: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
