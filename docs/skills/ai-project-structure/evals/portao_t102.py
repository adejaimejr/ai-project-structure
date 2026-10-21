#!/usr/bin/env python3
"""Portao da T-102: documentacao do adaptador Cloudroom e bump da skill (spec 0008).

Escrito pelo agente de planejamento em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: nao existe `references/cloudroom.md`, nada cita o adaptador e a versao e 2.13.0.
A 2.14.0 e da spec 0007 (github), que sai primeiro por decisao do usuario (DEC-009).

1. `references/cloudroom.md` existe, com secoes de uso, exit codes (0, 1, 2 e 143 em tabela) e
   limites que digam, com todas as letras, que o adaptador nao serve ao consenso, que sandbox
   propria fica fora, que o Mac (thread Local) nao foi exercitado e que o loop so vale com
   `--projeto` igual a pasta da thread (DEC-004); traz o exemplo de perfil
   `cloudroom_agente.py --provider`;
2. `SKILL.md` cita `cloudroom_agente.py` e aponta para `references/cloudroom.md`;
3. `references/loop.md` tem a linha da tabela de ferramentas para o Cloudroom;
4. `references/consenso.md` diz que o filho do Cloudroom nao entra como participante;
5. versao coerente em 2.15.0 ou acima (frontmatter, prosa, marcadores e secao mais recente do
   CHANGELOG da skill), e essa secao cita `cloudroom_agente.py`;
6. `install.sh` distribui o script (nao esta na lista de ignorados);
7. sem travessao nos arquivos tocados; `validate_structure.py . --strict` limpo; verificador exit 0.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ROOT, SKILL, autoteste, check, ler, norm, resumo, validar, verify_ok, versao_coerente  # noqa: E402

REF = SKILL / "references" / "cloudroom.md"
NOVA = "2.15.0"  # spec 0008/DEC-009: a 0007 (github) leva a 2.14.0
TRAVESSAO = "\u2014"  # escapado: o verificador acusa o caractere literal

RE_USO = re.compile(r"^##+ .*\buso\b", re.M)
RE_EXIT = re.compile(r"^##+ .*exit codes?", re.M)
RE_LIMITES = re.compile(r"^##+ .*limites", re.M)
RE_LINHA_143 = re.compile(r"^\|\s*143\s*\|", re.M)
RE_SEM_CONSENSO = re.compile(r"(?:consenso\.py|consenso)[^\n]{0,120}\bn[a]o\b|\bn[a]o\b[^\n]{0,120}consenso", re.I)
# Sentido, nao so palavra (revisao do gpt-6-luna em 2026-10-21): o limite tem de estar afirmado na mesma frase.
RE_SANDBOX_PROPRIA = re.compile(r"sandbox propria[^.\n]{0,100}(?:fica fora|fora do escopo|nao serve|nao e suportad|recusad)"
                                r"|(?:fica fora|fora do escopo|nao serve|recusa)[^.\n]{0,100}sandbox propria", re.I)
RE_MAC = re.compile(r"(?:\bmac\b|thread local)[^.\n]{0,100}nao (?:foi )?(?:exercitad|testad|conferid|verificad)"
                    r"|nao (?:foi )?(?:exercitad|testad|conferid|verificad)[^.\n]{0,100}(?:\bmac\b|thread local)", re.I)
# spec 0008/DEC-004, corrigida pela rodada de consenso de 2026-10-21: o loop so vale na pasta da thread.
RE_PASTA_THREAD = re.compile(r"(?<!nao )\b(?:so|somente|apenas)\b[^.\n]{0,80}--projeto[^.\n]{0,80}pasta da thread"
                             r"|--projeto[^.\n]{0,40}(?<!nao )\b(?:so|somente|apenas)\b[^.\n]{0,80}pasta da thread", re.I)
RE_PERFIL = re.compile(r"cloudroom_agente\.py\s+--provider\s+\S+")
RE_LINHA_LOOP = re.compile(r"^\|\s*cloudroom[^|]*\|[^|]*cloudroom_agente\.py", re.I | re.M)

autoteste(RE_USO, norm("## Uso\n"), contra=norm("## Usuario\n"))
autoteste(RE_EXIT, norm("## Exit Codes\n"))
autoteste(RE_LIMITES, norm("## Limites Declarados\n"))
autoteste(RE_LINHA_143, "| 143 | morto por SIGTERM |\n", contra="| 1 | erro |\n")
autoteste(RE_SEM_CONSENSO, norm("O adaptador nao serve ao consenso.py: siblings se enxergam."),
          contra=norm("O consenso usa copia por participante."))
autoteste(RE_LINHA_LOOP, "| Cloudroom (filho visivel) | `python3 <skill>/scripts/cloudroom_agente.py --provider claude-code` |\n",
          contra="| Claude Code | `claude -p` |\n")
autoteste(RE_PASTA_THREAD, norm("O loop so vale com --projeto igual a pasta da thread do Cloudroom."),
          contra=norm("O loop vale em qualquer --projeto."))
autoteste(RE_PASTA_THREAD, norm("--projeto so vale quando e a pasta da thread."),
          contra=norm("Funciona com qualquer --projeto, nao so a pasta da thread."))
autoteste(RE_SANDBOX_PROPRIA, norm("Filho em sandbox propria fica fora: a resposta nao e legivel."),
          contra=norm("Filho em sandbox propria funciona igual ao compartilhado."))
autoteste(RE_MAC, norm("Thread Local no Mac nao foi exercitada."),
          contra=norm("No Mac, em thread Local, funciona igual."))
autoteste(RE_PERFIL, "`python3 <skill>/scripts/cloudroom_agente.py --provider claude-code --model x`")


def main():
    texto = norm(ler(REF)) if REF.is_file() else ""
    ref_ok = REF.is_file() and RE_USO.search(texto) and RE_EXIT.search(texto) and RE_LIMITES.search(texto)
    check(ref_ok, "1. references/cloudroom.md existe com secoes de uso, exit codes e limites",
          "" if ref_ok else ("ausente" if not REF.is_file() else "secao faltando"))
    check(bool(REF.is_file() and RE_LINHA_143.search(texto) and all(re.search(r"^\|\s*%s\s*\|" % c, texto, re.M) for c in ("0", "1", "2"))),
          "1b. tabela de exit codes com 0, 1, 2 e 143")
    m_limites = RE_LIMITES.search(texto) if texto else None
    limites = texto[m_limites.start():] if m_limites else ""
    check(bool(limites and RE_SEM_CONSENSO.search(limites) and RE_SANDBOX_PROPRIA.search(limites) and RE_MAC.search(limites)),
          "1c. limites dizem que o adaptador nao serve ao consenso, que sandbox propria fica fora e que o Mac nao foi exercitado")
    check(bool(limites and RE_PASTA_THREAD.search(limites) and "--projeto" in limites),
          "1e. limites dizem que o loop so vale com --projeto igual a pasta da thread (DEC-004)")
    check(bool(texto and RE_PERFIL.search(texto)), "1d. exemplo de perfil com cloudroom_agente.py --provider")

    skill = ler(SKILL / "SKILL.md")
    check("cloudroom_agente.py" in skill and "references/cloudroom.md" in skill,
          "2. SKILL.md cita cloudroom_agente.py e aponta para references/cloudroom.md")
    check(bool(RE_LINHA_LOOP.search(ler(SKILL / "references" / "loop.md"))),
          "3. references/loop.md tem a linha da tabela de ferramentas para o Cloudroom")
    consenso_md = norm(ler(SKILL / "references" / "consenso.md"))
    check("cloudroom" in consenso_md and bool(re.search(r"cloudroom[^\n]{0,200}\bn[a]o\b", consenso_md)),
          "4. references/consenso.md diz que o filho do Cloudroom nao entra como participante")

    versao, ok_versao, recente, detalhe = versao_coerente(NOVA)
    check(ok_versao, "5. versao coerente em %s ou acima (frontmatter, prosa, marcadores, CHANGELOG)" % NOVA, detalhe)
    check("cloudroom_agente.py" in recente, "5b. a secao mais recente do CHANGELOG da skill cita cloudroom_agente.py")

    instalador = ler(SKILL / "install.sh")
    ignorados = re.search(r"ignorar_arquivo\(\)\s*\{.*?\}", instalador, re.S)
    check(bool((SKILL / "scripts" / "cloudroom_agente.py").is_file() and ignorados and "cloudroom" not in ignorados.group(0)),
          "6. install.sh distribui scripts/cloudroom_agente.py (nao esta na lista de ignorados)")

    tocados = [REF, SKILL / "SKILL.md", SKILL / "references" / "loop.md", SKILL / "references" / "consenso.md",
               SKILL / "CHANGELOG.md", SKILL / "scripts" / "cloudroom_agente.py"]
    com_travessao = [p.name for p in tocados if p.is_file() and TRAVESSAO in ler(p)]
    check(not com_travessao, "7. sem travessao nos arquivos tocados", ", ".join(com_travessao))
    codigo, linhas, _ = validar(ROOT, "--strict")
    check(codigo == 0, "7b. validate_structure.py . --strict limpo", linhas[-1] if linhas else "")
    ok, detalhe = verify_ok()
    check(ok, "7c. verify_repository.py em exit 0", detalhe)
    return resumo("T-102")


if __name__ == "__main__":
    sys.exit(main())
