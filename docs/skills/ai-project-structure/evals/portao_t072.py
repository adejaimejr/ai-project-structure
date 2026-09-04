#!/usr/bin/env python3
"""Portao da T-072: parenteses no comando do marcador verifica sao acusados.

Cobra comportamento e texto, sem ditar nome de codigo. Nao roda o
`verify_repository.py`: a tarefa muda o texto do bloco core em `assets/`, e a
propagacao para o `AGENTS.md` da raiz e do agente de chat, depois da rodada;
ate la a paridade estaria quebrada de proposito. O que o verificador cobraria
de versao e de cobertura por codigo esta replicado aqui.

1. Projeto com `(verifica: python3 -c "print(1)")` em tarefa aberta: o
   validador sai 1 com ERRO em `docs/TASKS.md`.
2. `loop_task.py check` nessa tarefa sai 1 e a mensagem fala de parenteses.
3. Projeto limpo montado de `assets/` passa em `--strict`.
4. O bloco core de `assets/AGENTS.md`, o cabecalho de `assets/docs/TASKS.md` e
   `references/loop.md` dizem que parenteses no comando nao sao suportados.
5. Versao acima de 2.7.0 e coerente: frontmatter do `SKILL.md`, toda "versao da
   estrutura" em prosa, marcadores de `assets/AGENTS.md` e dos dois partials, e
   heading no `CHANGELOG.md` da skill.
6. Todo codigo de `CODIGOS` tem oracle em `FIXTURES` (o codigo novo incluido).
7. A raiz deste repositorio continua limpa em `--strict`.
"""

import ast
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
HELPER = SKILL / "scripts" / "loop_task.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
VERSAO_ANTES = "2.7.0"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


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
        "(convencoes-2-2-0-desde: AAAA-MM-DD)", "(convencoes-2-2-0-desde: 2026-09-01)"), encoding="utf-8")
    return r


def validar(r, strict=False):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(r), "--codigos"] + (["--strict"] if strict else []),
                       capture_output=True, text=True)
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()]


def constante(caminho, nome):
    for no in ast.parse(caminho.read_text(encoding="utf-8")).body:
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nome for t in no.targets):
            return ast.literal_eval(no.value)
    return None


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo")
        code, out = validar(r, strict=True)
        check(code == 0 and not out, "3. projeto limpo montado de assets passa em --strict", "; ".join(out)[:200])

        r = montar(tmp, "c1")
        t = r / "docs" / "TASKS.md"
        t.write_text(t.read_text(encoding="utf-8").replace(
            "## Em Andamento\n\n", '## Em Andamento\n\n- T-009: Comando com parenteses. (verifica: python3 -c "print(1)")\n', 1),
            encoding="utf-8")
        code, out = validar(r)
        check(code == 1 and any(l.startswith("ERRO|") and l.split("|")[2] == "docs/TASKS.md" for l in out),
              "1. verifica com parenteses e ERRO em docs/TASKS.md", "; ".join(out)[:200])
        p = subprocess.run([sys.executable, str(HELPER), "check", str(r), "T-009"], capture_output=True, text=True)
        msg = (p.stdout + p.stderr).strip()
        check(p.returncode == 1 and "parentes" in norm(msg), "2. loop_task check recusa e explica os parenteses", msg[:160])

    core = ASSETS / "AGENTS.md"
    m = re.search(r"core:start.*?core:end", core.read_text(encoding="utf-8"), re.S)
    bloco = m.group(0) if m else ""
    # A frase precisa estar no item que define o marcador, nao em qualquer lugar
    # do bloco (a palavra "parenteses" ja aparece na regra do travessao).
    item = next((l for l in bloco.splitlines() if "(verifica: <comando>)" in l), "")
    check("parentes" in norm(item), "4a. o item do bloco core que define (verifica: <comando>) diz que parenteses nao sao suportados", item[:160])
    check("parentes" in norm((ASSETS / "docs" / "TASKS.md").read_text(encoding="utf-8")), "4b. cabecalho de assets/docs/TASKS.md diz o mesmo")
    check("parentes" in norm((SKILL / "references" / "loop.md").read_text(encoding="utf-8")), "4c. references/loop.md diz o mesmo")

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    acima = tuple(int(x) for x in versao.split(".")) > tuple(int(x) for x in VERSAO_ANTES.split("."))
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    changelog = re.search(rf"^## {re.escape(versao)}\b", (SKILL / "CHANGELOG.md").read_text(encoding="utf-8"), re.M) is not None
    check(acima and prosa == {versao} and marcadores == {versao} and changelog,
          f"5. versao acima de {VERSAO_ANTES} e coerente em SKILL.md, prosa, marcadores dos assets e CHANGELOG",
          f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)} changelog={changelog}")

    codigos = set(constante(VALIDATOR, "CODIGOS") or [])
    fixtures = constante(EVALS / "verify_repository.py", "FIXTURES") or {}
    cobertos = {d.split("|")[1] for o in fixtures.values() for d in o.get("diagnosticos", []) if d.count("|") >= 1}
    sem = sorted(codigos - cobertos)
    check(not sem, f"6. todos os {len(codigos)} codigos tem oracle em FIXTURES", ", ".join(sem))

    code, out = validar(ROOT, strict=True)
    check(code == 0, "7. raiz do repositorio limpa em --strict", "; ".join(out)[:200])

    total = 9
    print(f"\nPortao T-072: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
