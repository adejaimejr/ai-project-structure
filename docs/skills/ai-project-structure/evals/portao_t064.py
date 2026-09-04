#!/usr/bin/env python3
"""Portao da T-064: consertos sem decisao no validador (REVAL-2).

Cobra comportamento; nao dita nome de codigo. Casos:

1. `docs/MEMORY.md` fora de UTF-8: diagnostico para esse arquivo e exit 1, sem traceback.
2. Rotulo de consenso com acento combinante (`**Metodo:́**`): sem traceback.
3. `ENTRY_RE` e `DATE_RE` nao existem mais no validador.
4. Exemplo de entrada dentro de cerca `~~~` nao e lido como entrada.
5. Heading ATX com fechamento (`### Objetivo ###`) conta como heading.
6. `(spec: 0001-NNNN-ausente)` e acusado; `(spec: NNNN-slug)`, placeholder inteiro, segue tolerado.
7. `**Status:**` de spec no meio de um paragrafo nao conta como linha de status.
8. Projeto limpo montado de `assets/` e a raiz passam em `--strict`.
9. Versao acima de 2.8.1 e `verify_repository.py` em exit 0 (a tarefa nao toca o bloco core).
"""

import ast
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ROOT = SKILL.parents[2]
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
HEADINGS = ["Objetivo", "O Que Foi Feito", "Arquivos Criados Ou Alterados", "Decisoes Tomadas",
            "Aprendizados Para MEMORY.md", "Pendencias", "Proximo Passo Recomendado"]
VERSAO_ANTES = "2.8.1"

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
    t = r / "docs" / "TASKS.md"
    t.write_text(t.read_text(encoding="utf-8").replace("(convencoes-2-2-0-desde: AAAA-MM-DD)", "(convencoes-2-2-0-desde: 2026-09-01)"), encoding="utf-8")
    return r


def validar(r, strict=True):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(r), "--codigos"] + (["--strict"] if strict else []),
                       capture_output=True, text=True, errors="replace")
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()], p.stderr


def anexar(r, rel, texto):
    p = r / rel
    p.write_text(p.read_text(encoding="utf-8") + texto, encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo")
        code, out, err = validar(r)
        check(code == 0 and not out and not err.strip(), "8a. projeto limpo montado de assets passa em --strict", "; ".join(out)[:160])

        r = montar(tmp, "c1")
        (r / "docs" / "MEMORY.md").write_bytes(b"# MEMORY\n\xe9 latin-1\n")
        code, out, err = validar(r)
        check(code == 1 and any(l.split("|")[2] == "docs/MEMORY.md" for l in out) and "Traceback" not in err,
              "1. MEMORY.md fora de UTF-8 vira diagnostico, sem traceback", ("; ".join(out) + " " + err.strip()[-80:])[:200])

        r = montar(tmp, "c2")
        anexar(r, "docs/CONSENSUS.md", "\n## 2026-09-02 - X\n\n**Status:** aberto\n\n**Proximo passo:** eu\n\n**Metodo:́** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n\n**Rodada:** 1 de 1\n")
        code, out, err = validar(r)
        check("Traceback" not in err and code in (0, 1), "2. rotulo com acento combinante nao derruba o validador", err.strip()[-120:])

        r = montar(tmp, "c4")
        anexar(r, "docs/CONSENSUS.md", "\n## 2026-09-02 - Exemplo em cerca til\n\n**Status:** resolvido\n\n**Metodo:** debate-aberto\n\n**Exposicao previa a outras posicoes:** sim\n\n**Rodada:** 1 de 1\n\nExemplo:\n\n~~~md\n## 2026-01-01 - Entrada dentro de cerca til\n~~~\n")
        code, out, err = validar(r)
        check(code == 0 and not out, "4. exemplo em cerca ~~~ nao e lido como entrada", "; ".join(out)[:160])

        r = montar(tmp, "c5")
        anexar(r, "docs/SESSION.md", "\n## 2026-09-02 - Claude\n\n" + "\n\n".join(f"### {h} ###\n\n- x" for h in HEADINGS) + "\n")
        code, out, err = validar(r)
        check(code == 0 and not out, "5. heading ATX com fechamento conta como heading", "; ".join(out)[:160])

        r = montar(tmp, "c6a")
        t = r / "docs" / "TASKS.md"
        t.write_text(t.read_text(encoding="utf-8").replace("## Em Andamento\n\n", "## Em Andamento\n\n- T-009: Ref com NNNN no meio. (spec: 0001-NNNN-ausente)\n", 1), encoding="utf-8")
        code, out, err = validar(r, strict=False)
        check(code == 1 and any(l.startswith("ERRO|") and "docs/TASKS.md" in l for l in out), "6a. (spec: 0001-NNNN-ausente) e acusado", "; ".join(out)[:160])
        r = montar(tmp, "c6b")
        t = r / "docs" / "TASKS.md"
        t.write_text(t.read_text(encoding="utf-8").replace("## Em Andamento\n\n", "## Em Andamento\n\n- T-009: Placeholder inteiro. (spec: NNNN-slug)\n", 1), encoding="utf-8")
        code, out, err = validar(r, strict=False)
        check(code == 0, "6b. (spec: NNNN-slug), placeholder inteiro, segue tolerado", "; ".join(out)[:160])

        r = montar(tmp, "c7")
        (r / "docs" / "specs").mkdir()
        (r / "docs" / "specs" / "0001-x.md").write_text("# Spec 0001\n\nIsto nao e linha de status, mas contem **Status:** Rascunho\n", encoding="utf-8")
        code, out, err = validar(r, strict=False)
        check(code == 1 and any(l.startswith("ERRO|") and "0001-x.md" in l for l in out), "7. Status de spec no meio da prosa nao conta", "; ".join(out)[:160])

    fonte = VALIDATOR.read_text(encoding="utf-8")
    nomes = {t.id for no in ast.parse(fonte).body if isinstance(no, ast.Assign) for t in no.targets if isinstance(t, ast.Name)}
    check("ENTRY_RE" not in nomes and "DATE_RE" not in nomes, "3. ENTRY_RE e DATE_RE removidos")

    code, out, err = validar(ROOT)
    check(code == 0, "8b. raiz do repositorio limpa em --strict", "; ".join(out)[:160])

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    check(tuple(int(x) for x in versao.split(".")) > tuple(int(x) for x in VERSAO_ANTES.split(".")), f"9a. SKILL.md com versao acima de {VERSAO_ANTES}", versao)
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "9b. verify_repository.py exit 0", resumo)

    total = 12
    print(f"\nPortao T-064: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
