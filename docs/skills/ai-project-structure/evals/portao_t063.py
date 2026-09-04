#!/usr/bin/env python3
"""Portao da T-063: templates de `assets/` acompanham o bloco core (REVAL-6).

Tarefa de texto nos templates mais uma frase no bloco core. Nao roda o
`verify_repository.py` porque a propagacao do core para o `AGENTS.md` da raiz
e do agente de chat, depois da rodada. Cobra:

1. `assets/docs/QUALITY.md` fala de evidencia de fechamento, Aguardando Usuario,
   campos de independencia (Metodo, Exposicao previa, Rodada) e achado.
2. `assets/docs/PROMPTS.md`: o prompt de consenso pede Metodo, Exposicao previa
   e Rodada; algum prompt cita a evidencia em `TASKS.md`.
3. `assets/docs/ONBOARDING.md` cita `MEMORY.md`, evidencia e Aguardando Usuario.
4. `assets/docs/README.md` diz que `CONSENSUS.md` tambem registra achado.
5. O modelo de `assets/docs/SESSION.md` traz a nota "qualquer agente serve se
   tiver contexto suficiente".
6. `assets/docs/ARCHITECTURE.md` sem `docs/skills/`; `GLOSSARY.md` sem "Codex".
7. `assets/docs/TASKS.md` traz exemplo de evidencia `revisao-manual` e o modelo
   de linha concluida nao cita `0001-login-social`.
8. No bloco core, o item `docs/ARCHITECTURE.md` da leitura relevante diz
   "quando existir" (ou "se existir").
9. `verificar_convencoes` do verificador cobre QUALITY, PROMPTS, ONBOARDING e README.
10. Projeto limpo montado de `assets/` e a raiz passam em `--strict`.
11. Versao coerente entre `SKILL.md`, prosa, marcadores dos assets e CHANGELOG,
    e a secao mais recente do CHANGELOG cita os templates (QUALITY).
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


def asset(rel):
    return norm((ASSETS / "docs" / rel).read_text(encoding="utf-8"))


def main():
    q = asset("QUALITY.md")
    check("evidencia" in q and "aguardando usuario" in q and "metodo" in q and "exposicao previa" in q and "rodada" in q and "achado" in q,
          "1. QUALITY.md cobre evidencia, Aguardando Usuario, independencia e achado")
    p = asset("PROMPTS.md")
    check("metodo" in p and "exposicao previa" in p and "rodada" in p and "evidencia" in p,
          "2. PROMPTS.md pede os campos de independencia e cita evidencia")
    o = asset("ONBOARDING.md")
    check("memory.md" in o and "evidencia" in o and "aguardando usuario" in o, "3. ONBOARDING.md cita MEMORY.md, evidencia e Aguardando Usuario")
    r = asset("README.md")
    linha = next((l for l in r.splitlines() if "`consensus.md`" in l), "")
    check("achado" in linha, "4. README.md diz que CONSENSUS.md tambem registra achado", linha[:120])
    s = asset("SESSION.md")
    check("qualquer agente serve se tiver contexto suficiente" in s, "5. modelo de SESSION.md traz a nota sobre qualquer agente")
    check("docs/skills" not in asset("ARCHITECTURE.md") and "codex" not in asset("GLOSSARY.md"),
          "6. ARCHITECTURE.md sem docs/skills e GLOSSARY.md sem Codex")
    t = asset("TASKS.md")
    check("tipo=revisao-manual" in t and "0001-login-social" not in t,
          "7. TASKS.md com exemplo revisao-manual e sem 0001-login-social no modelo")

    core_txt = (ASSETS / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(r"core:start.*?core:end", core_txt, re.S)
    item = next((l for l in (m.group(0) if m else "").splitlines() if "docs/ARCHITECTURE.md" in l and re.match(r"^\d+\.", l.strip())), "")
    check("quando existir" in norm(item) or "se existir" in norm(item), "8. item docs/ARCHITECTURE.md da leitura relevante diz quando existir", item[:120])

    vr = (EVALS / "verify_repository.py").read_text(encoding="utf-8")
    func = vr.split("def verificar_convencoes", 1)[-1].split("\ndef ", 1)[0]
    check(all(n in func for n in ("QUALITY.md", "PROMPTS.md", "ONBOARDING.md", "README.md")),
          "9. verificar_convencoes cobre QUALITY, PROMPTS, ONBOARDING e README")

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "limpo"
        (d / "docs" / "archive").mkdir(parents=True)
        for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
            shutil.copy(ASSETS / f, d / f)
        for f in NUCLEO:
            shutil.copy(ASSETS / "docs" / f, d / "docs" / f)
        shutil.copy(ASSETS / "docs" / "archive" / "README.md", d / "docs" / "archive" / "README.md")
        tk = d / "docs" / "TASKS.md"
        tk.write_text(tk.read_text(encoding="utf-8").replace("(convencoes-2-2-0-desde: AAAA-MM-DD)", "(convencoes-2-2-0-desde: 2026-09-01)"), encoding="utf-8")
        pr = subprocess.run([sys.executable, str(VALIDATOR), str(d), "--strict", "--codigos"], capture_output=True, text=True)
        check(pr.returncode == 0 and not pr.stdout.strip(), "10a. projeto limpo montado de assets passa em --strict", pr.stdout.strip()[:160])
    pr = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), "--strict", "--codigos"], capture_output=True, text=True)
    check(pr.returncode == 0, "10b. raiz do repositorio limpa em --strict", pr.stdout.strip()[:160])

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    partes = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8").split("\n## ", 2)
    recente = partes[1] if len(partes) > 1 else ""
    check(recente.startswith(versao) and "quality" in norm(recente) and prosa == {versao} and marcadores == {versao},
          "11. CHANGELOG mais recente cita os templates e a versao e coerente",
          f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}")

    total = 12
    print(f"\nPortao T-063: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
