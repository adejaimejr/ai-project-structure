#!/usr/bin/env python3
"""Portao da T-062: duas ambiguidades de texto em `references/atualizacao.md` (REVAL-5).

1. O passo "v1 -> v2" diz, sem ambiguidade, onde a secao resgatada do
   `AGENTS.md` v1 vai parar: como item dentro de "## Regras Do Projeto" ou
   como subsecao dela, e nao como secao `##` irma.
2. O passo de migrar `TASKS.md` diz o que fazer com a data das linhas
   concluidas: prefixar quando conhecida, ou deixar sem data e declarar que a
   linha nao e cobrada.
3. Versao acima de 2.9.0 e coerente, secao mais recente do CHANGELOG cita a
   atualizacao, `verify_repository.py` em exit 0.
"""

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ASSETS = SKILL / "assets"
VERSAO_ANTES = "2.9.0"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


def secao(texto, titulo_regex):
    # O titulo fica em [^\n]* de proposito: com re.S, um .* no titulo engolia o
    # documento inteiro e o corpo capturado ficava vazio (falso negativo do portao).
    m = re.search(rf"^#{{2,3}} {titulo_regex}[^\n]*$(.*?)(?=^#{{2,3}} |\Z)", texto, re.M | re.S | re.I)
    return m.group(1) if m else ""


def main():
    doc = (SKILL / "references" / "atualizacao.md").read_text(encoding="utf-8")
    v1 = norm(secao(doc, r"v1 [^\n]*v2"))
    check(bool(v1) and "regras do projeto" in v1 and ("###" in v1 or "subsecao" in v1 or "como item" in v1 or "dentro de" in v1)
          and ("irma" in v1 or "nao" in v1),
          "1. passo v1 -> v2 diz onde a secao resgatada vai (dentro, nao irma)", v1.strip()[:200])
    migrar = norm(secao(doc, r"7\. migrar tasks"))
    check(bool(migrar) and "data" in migrar and ("conhecida" in migrar or "souber" in migrar) and ("nao e cobrada" in migrar or "sem data" in migrar),
          "2. passo de migrar TASKS diz o que fazer com a data das concluidas", migrar.strip()[:200])

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    acima = tuple(int(x) for x in versao.split(".")) > tuple(int(x) for x in VERSAO_ANTES.split("."))
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    partes = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8").split("\n## ", 2)
    recente = partes[1] if len(partes) > 1 else ""
    check(acima and prosa == {versao} and marcadores == {versao} and recente.startswith(versao) and "atualizacao" in norm(recente),
          f"3a. versao acima de {VERSAO_ANTES}, coerente, e CHANGELOG cita a atualizacao",
          f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "3b. verify_repository.py exit 0", resumo)

    total = 4
    print(f"\nPortao T-062: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
