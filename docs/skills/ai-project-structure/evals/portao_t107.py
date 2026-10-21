#!/usr/bin/env python3
"""Portao da T-107: validador e verificador reconhecem o bloco `github` (spec 0007).

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: `MARKER_RE` so aceita core, specs e loop, e o verificador nao conhece o bloco.

Cada caso monta um projeto limpo dos assets e insere o bloco do partial
`assets/partials/AGENTS-github-block.md` antes de "## Regras Do Projeto":

1. bloco bem formado: `--strict` limpo, nenhum codigo `GITHUB-*`;
2. sem o bloco: nenhum codigo `GITHUB-*` (projeto que nao ativa nao paga nada);
3. sem o marcador `end`: ERRO `GITHUB-MARCADOR-INVALIDO` (e `MARCADOR-DESPAREADO`, que ja existe);
4. start sem versao: ERRO `GITHUB-MARCADOR-INVALIDO`;
5. start com versao diferente da do bloco core: AVISO `GITHUB-VERSAO-DIVERGENTE`, exit 0 sem
   `--strict` e 1 com;
6. os dois codigos em `CODIGOS`;
7. fixture `evals/fixtures/github-project/` com `valido/` e `invalido/`, citada no verificador
   com os dois codigos no oraculo;
8. `verify_repository.py` cobre o bloco: regex do bloco `github`, `github` na regex de versao,
   o partial na lista de marcadores e paridade com a raiz quando o bloco estiver ativo;
9. verificador em exit 0 com pelo menos 80 verificacoes; raiz limpa em `--strict`.
"""

import re
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, EVALS, ROOT, SKILL, check, ler, montar, resumo, validar, verify_ok  # noqa: E402

PARTIAL = ASSETS / "partials" / "AGENTS-github-block.md"
FIXTURE = EVALS / "fixtures" / "github-project"
PISO_VERIFICADOR = 80
INVALIDO, DIVERGENTE = "GITHUB-MARCADOR-INVALIDO", "GITHUB-VERSAO-DIVERGENTE"


def bloco_partial():
    if not PARTIAL.is_file():
        # Sem o partial (T-106), o portao usa um bloco minimo na versao do core para nao depender da ordem.
        v = re.search(r"core:start\s+(v\S+)", ler(ASSETS / "AGENTS.md")).group(1)
        return "<!-- ai-project-structure:github:start %s -->\n## GitHub\n\n- Regra.\n<!-- ai-project-structure:github:end -->\n" % v
    return ler(PARTIAL).strip() + "\n"


def caso(tmp, nome, transforma=None, com_bloco=True):
    r = montar(tmp, nome)
    agents = r / "AGENTS.md"
    texto = ler(agents)
    if com_bloco:
        bloco = bloco_partial()
        if transforma:
            bloco = transforma(bloco)
        texto = texto.replace("## Regras Do Projeto", bloco + "\n## Regras Do Projeto", 1)
    agents.write_text(texto, encoding="utf-8")
    return r


def codigos(r, *flags):
    codigo, linhas, _ = validar(r, "--codigos", *flags)
    return codigo, [l.split("|") for l in linhas if l.count("|") >= 3]


def nivel(linhas, cod):
    return {l[0] for l in linhas if l[1] == cod}


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = caso(tmp, "ok")
        codigo, linhas = codigos(r, "--strict")
        check(codigo == 0 and not any(l[1].startswith("GITHUB-") for l in linhas),
              "1. bloco github bem formado: --strict limpo", "; ".join("|".join(l) for l in linhas[:4]) or "exit %s" % codigo)

        r = caso(tmp, "sem", com_bloco=False)
        _, linhas = codigos(r)
        check(not any(l[1].startswith("GITHUB-") for l in linhas), "2. sem o bloco: nenhum codigo GITHUB-*")

        r = caso(tmp, "sem-end", lambda b: re.sub(r"<!--\s*ai-project-structure:github:end\s*-->\n?", "", b))
        _, linhas = codigos(r)
        check("ERRO" in nivel(linhas, INVALIDO) and "ERRO" in nivel(linhas, "MARCADOR-DESPAREADO"),
              "3. sem o end: ERRO %s e MARCADOR-DESPAREADO" % INVALIDO, "; ".join("|".join(l) for l in linhas[:4]))

        r = caso(tmp, "sem-versao", lambda b: re.sub(r"(github:start)\s+v\S+", r"\1", b))
        _, linhas = codigos(r)
        check("ERRO" in nivel(linhas, INVALIDO), "4. start sem versao: ERRO %s" % INVALIDO,
              "; ".join("|".join(l) for l in linhas[:4]))

        r = caso(tmp, "divergente", lambda b: re.sub(r"(github:start)\s+v\S+", r"\1 v9.9.9", b))
        c_sem, linhas = codigos(r)
        c_com, _ = codigos(r, "--strict")
        check(nivel(linhas, DIVERGENTE) == {"AVISO"} and c_sem == 0 and c_com == 1,
              "5. versao diferente do core: AVISO %s (exit 0 sem --strict, 1 com)" % DIVERGENTE,
              "exit %s / %s; %s" % (c_sem, c_com, "; ".join("|".join(l) for l in linhas[:3])))

    fonte = ler(SKILL / "scripts" / "validate_structure.py")
    declaracoes = fonte.split("def ", 1)[0]
    check(INVALIDO in declaracoes and DIVERGENTE in declaracoes, "6. os dois codigos em CODIGOS")

    verificador = ler(EVALS / "verify_repository.py")
    check(FIXTURE.is_dir() and (FIXTURE / "valido").is_dir() and (FIXTURE / "invalido").is_dir()
          and '"github-project"' in verificador and INVALIDO in verificador and DIVERGENTE in verificador,
          "7. fixture github-project (valido e invalido) no verificador, com os dois codigos no oraculo")

    check(re.search(r"ai-project-structure:github:start", verificador) is not None
          and re.search(r"\(\?:core\|specs\|loop\|github\)|github\|", verificador) is not None
          and "AGENTS-github-block.md" in verificador,
          "8. verificador com regex do bloco github, github na regex de versao e o partial na lista de marcadores")

    ok, detalhe = verify_ok()
    m = re.search(r"(\d+)/(\d+)", detalhe)
    n = int(m.group(2)) if m else 0
    codigo, saida, _ = validar(ROOT, "--strict")
    check(ok and n >= PISO_VERIFICADOR and codigo == 0,
          "9. verificador em exit 0 com pelo menos %d verificacoes e raiz limpa em --strict" % PISO_VERIFICADOR,
          "%s; %s" % (detalhe, saida[-1] if saida else ""))
    return resumo("T-107")


if __name__ == "__main__":
    sys.exit(main())
