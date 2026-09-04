#!/usr/bin/env python3
"""Portao da T-065: o portao dos evals deixa de ser cego (achado REVAL-4).

`verify_repository.py` ja passava antes da T-065, entao ele sozinho nao prova
que a tarefa foi feita: fecharia a tarefa verde com trabalho zero. Este
script falha enquanto o trabalho nao existir e passa quando existir. Cobra o
resultado, nao o jeito de chegar la:

1. Todo codigo em `CODIGOS` de `validate_structure.py` aparece em pelo menos
   um oracle de `FIXTURES` em `verify_repository.py` (cobertura positiva).
2. Todo diretorio de fixture com `docs/TASKS.md` em `evals/fixtures/` esta
   declarado em `FIXTURES` (inventario contra o disco).
3. `verify_repository.py` declara o conjunto de etapas obrigatorias e falha se
   uma sumir: existe uma constante `ETAPAS` (lista de nomes de funcao) e `main`
   a percorre.
4. `test_loop.py` assere o conteudo do prompt entregue ao agente: a tarefa
   (`T-019`), o comando do portao, a frase "NAO APAGUE O QUE FALHA" e a
   proibicao de editar `docs/MEMORY.md`.
5. `verificar_versao` cobre a versao em prosa: `SKILL.md` ("versao da
   estrutura: X.Y.Z") e o `CHANGELOG.md` da skill.
6. `verify_repository.py` continua saindo 0.

Vive em `evals/`, nao e distribuido. Somente biblioteca padrao.
"""

import ast
import re
import subprocess
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
VERIFY = EVALS / "verify_repository.py"
TEST_LOOP = EVALS / "test_loop.py"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def constante(caminho, nome):
    """Valor literal de uma constante de modulo, sem importar o modulo."""
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == nome for t in no.targets
        ):
            return ast.literal_eval(no.value)
    return None


def main():
    codigos = constante(VALIDATOR, "CODIGOS") or set()
    fixtures = constante(VERIFY, "FIXTURES") or {}

    # 1. cobertura positiva por codigo
    cobertos = set()
    for oraculo in fixtures.values():
        for diag in oraculo.get("diagnosticos", []):
            partes = diag.split("|")
            if len(partes) >= 2:
                cobertos.add(partes[1])
    sem = sorted(set(codigos) - cobertos)
    check(not sem, f"todos os {len(codigos)} codigos tem fixture que os produza",
          f"{len(sem)} sem oracle: {', '.join(sem)}" if sem else f"{len(cobertos)} cobertos")

    # 2. inventario de fixtures no disco
    no_disco = sorted(
        p.parent.parent.relative_to(EVALS / "fixtures").as_posix()
        for p in (EVALS / "fixtures").rglob("docs/TASKS.md")
    )
    fora = [d for d in no_disco if d not in fixtures]
    check(not fora, "toda fixture no disco esta declarada em FIXTURES",
          ", ".join(fora) if fora else f"{len(no_disco)} diretorios")

    # 3. manifesto de etapas
    etapas = constante(VERIFY, "ETAPAS")
    fonte = VERIFY.read_text(encoding="utf-8")
    check(isinstance(etapas, (list, tuple)) and len(etapas) >= 10 and "for " in fonte and "ETAPAS" in fonte.split("def main")[-1],
          "verify_repository.py declara ETAPAS e main as percorre",
          f"{len(etapas)} etapas" if etapas else "constante ausente")

    # 4. prompt do loop assertado
    tl = TEST_LOOP.read_text(encoding="utf-8")
    exigidos = ["T-019", "NAO APAGUE O QUE FALHA", "docs/MEMORY.md", "bash portao.sh"]
    faltando = [e for e in exigidos if tl.count(e) < 2]  # uma vez e so o fixture; duas e assercao
    check(not faltando, "test_loop.py assere tarefa, portao e regras criticas no prompt",
          "sem assercao para: " + ", ".join(faltando) if faltando else "")

    # 5. versao em prosa
    check("versao da estrutura" in fonte and "CHANGELOG" in fonte.split("def verificar_versao")[-1].split("\ndef ")[0],
          "verificar_versao cobre a versao em prosa do SKILL.md e do CHANGELOG")

    # 6. o portao principal continua verde
    p = subprocess.run([sys.executable, str(VERIFY)], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "verify_repository.py exit 0", resumo)

    print(f"\nPortao T-065: {6 - len(falhas)}/6.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
