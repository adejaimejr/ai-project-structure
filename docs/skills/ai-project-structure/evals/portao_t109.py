#!/usr/bin/env python3
"""Portao da T-109: bump 2.14.0 e dogfood do modulo `github` nesta raiz (spec 0007).

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: a skill esta em 2.13.0 e a raiz nao tem o bloco `github`.

1. versao coerente em 2.14.0 ou acima (frontmatter, prosa, marcadores do core, specs e loop, e
   secao mais recente do CHANGELOG da skill); o partial `github` na mesma versao;
2. a secao mais recente do CHANGELOG da skill cita `references/github.md`, `assets/github/` e o
   codigo `CONSENSO-ORIGEM-CORRIDA-INCOMPLETA` (T-104 no mesmo bump);
3. a raiz tem o bloco `github` identico ao partial, depois do ultimo bloco gerenciado e antes de
   "## Regras Do Projeto";
4. a regra de `AGENTS.md` e `docs/CONTRIBUTING.md` deixam de dizer que o checklist mora em
   `CONTRIBUTING.md` "ate a 2.14.0": os dois apontam para `references/github.md`;
5. `install.sh` distribui `assets/github/` e o partial (nada disso na lista de ignorados);
6. sem travessao no partial, no CHANGELOG da skill e no `AGENTS.md`; raiz limpa em `--strict`;
   verificador em exit 0.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, ROOT, SKILL, check, ler, resumo, validar, verify_ok, versao_coerente  # noqa: E402

NOVA = "2.14.0"
PARTIAL = ASSETS / "partials" / "AGENTS-github-block.md"
TRAVESSAO = chr(0x2014)
RE_BLOCO = re.compile(r"<!--\s*ai-project-structure:github:start.*?ai-project-structure:github:end\s*-->", re.S)


def main():
    versao, ok_versao, recente, detalhe = versao_coerente(NOVA)
    parcial = ler(PARTIAL) if PARTIAL.is_file() else ""
    m = re.search(r"github:start\s+v(\d+\.\d+\.\d+)", parcial)
    check(ok_versao and m and m.group(1) == versao, "1. versao coerente em %s ou acima, partial github na mesma versao" % NOVA,
          "%s; partial=%s" % (detalhe, m.group(1) if m else "ausente"))
    check(all(t in recente for t in ("references/github.md", "assets/github/", "CONSENSO-ORIGEM-CORRIDA-INCOMPLETA")),
          "2. CHANGELOG da skill, secao mais recente, cita references/github.md, assets/github/ e o codigo da T-104")

    agents = ler(ROOT / "AGENTS.md")
    b_raiz, b_partial = RE_BLOCO.search(agents), RE_BLOCO.search(parcial)
    regras = agents.find("\n## Regras Do Projeto")
    ultimos_end = [x.end() for x in re.finditer(r"ai-project-structure:(?:core|specs|loop):end\s*-->", agents)]
    check(bool(b_raiz and b_partial and b_raiz.group(0) == b_partial.group(0) and regras > b_raiz.end()
               and ultimos_end and b_raiz.start() > max(ultimos_end)),
          "3. raiz com o bloco github identico ao partial, depois do ultimo bloco e antes de Regras Do Projeto")

    contributing = ler(ROOT / "docs" / "CONTRIBUTING.md")
    regra = [l for l in agents.splitlines() if "Configuracao do repositorio" in l]
    check(bool(regra) and "references/github.md" in regra[0] and "ate a 2.14.0" not in regra[0]
          and "until skill 2.14.0" not in contributing and "references/github.md" in contributing,
          "4. AGENTS.md e CONTRIBUTING.md apontam o checklist para references/github.md, sem 'ate a 2.14.0'")

    instalador = ler(SKILL / "install.sh")
    ignorados = re.search(r"ignorar_arquivo\(\)\s*\{.*?\}", instalador, re.S)
    check(bool((ASSETS / "github").is_dir() and PARTIAL.is_file() and ignorados
               and "github" not in ignorados.group(0) and "assets/" not in ignorados.group(0)),
          "5. install.sh distribui assets/github/ e o partial")

    com_travessao = [p.name for p in (PARTIAL, SKILL / "CHANGELOG.md", ROOT / "AGENTS.md") if p.is_file() and TRAVESSAO in ler(p)]
    codigo, saida, _ = validar(ROOT, "--strict")
    ok, detalhe_v = verify_ok()
    check(not com_travessao and codigo == 0 and ok, "6. sem travessao, raiz limpa em --strict e verificador em exit 0",
          "%s; %s; %s" % (", ".join(com_travessao), saida[-1] if saida else "", detalhe_v))
    return resumo("T-109")


if __name__ == "__main__":
    sys.exit(main())
