#!/usr/bin/env python3
"""Portao da T-054: `Rodada` ausente e `Rodada` com lixo depois do valor.

1. Entrada de consenso posterior a adocao sem `**Rodada:**`: AVISO em CONSENSUS.md, sem ERRO.
2. `**Rodada:** 1 de 1 e mais texto`: AVISO de formato.
3. `**Rodada:** 1 de 1`: limpo. 4. Entrada anterior a adocao sem Rodada: limpa (nao retroativo).
5. Projeto limpo e raiz em --strict. 6. Versao acima de 2.9.1 coerente; verify exit 0.
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
    def entrada(data, rodada):
        r_ = f"\n## {data} - X\n\n**Status:** resolvido\n\n**Metodo:** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n"
        return r_ + (f"\n**Rodada:** {rodada}\n" if rodada is not None else "")
    def anexar(r, texto):
        c = r / "docs" / "CONSENSUS.md"; c.write_text(c.read_text(encoding="utf-8") + texto, encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo"); code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 0 and not out, "5a. projeto limpo passa em --strict", "; ".join(out)[:160])
        r = montar(tmp, "c1"); anexar(r, entrada("2026-09-02", None)); code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 1 and any(l.startswith("AVISO|") and "docs/CONSENSUS.md" in l for l in out) and not any(l.startswith("ERRO|") for l in out),
              "1. Rodada ausente apos adocao e AVISO em CONSENSUS.md", "; ".join(out)[:160])
        r = montar(tmp, "c2"); anexar(r, entrada("2026-09-02", "1 de 1 e mais texto qualquer")); code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 1 and any(l.startswith("AVISO|") and "docs/CONSENSUS.md" in l for l in out), "2. Rodada com lixo depois do valor e AVISO", "; ".join(out)[:160])
        r = montar(tmp, "c3"); anexar(r, entrada("2026-09-02", "1 de 1")); code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 0 and not out, "3. Rodada 1 de 1 e limpa", "; ".join(out)[:160])
        r = montar(tmp, "c4"); anexar(r, entrada("2026-08-01", None)); code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 0 and not out, "4. entrada anterior a adocao sem Rodada nao e cobrada", "; ".join(out)[:160])
    code, out, _ = validar(ROOT, "--strict", "--codigos"); check(code == 0, "5b. raiz limpa em --strict", "; ".join(out)[:160])
    versao, ok, recente, det = versao_coerente("2.10.0"); check(ok, "6a. versao 2.10.0 ou acima, coerente", det)
    ok, resumo = verify_ok(); check(ok, "6b. verify_repository.py exit 0", resumo)

    total = 8
    print(f"\nPortao T-054: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
