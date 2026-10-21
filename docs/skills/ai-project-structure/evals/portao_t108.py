#!/usr/bin/env python3
"""Portao da T-108: entrevista, `references/github.md`, README da skill, prosa da raiz e evals (spec 0007).

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: nao ha pergunta 5, nem `references/github.md`, nem evals 13 e 14.

1. `SKILL.md`, secao "3. Entrevista": pergunta 5 sobre o modulo `github`, com a opcao "Nao"
   marcada como recomendada (DEC-004) e a lingua en ou pt-BR so no sim;
2. `SKILL.md` aponta para `references/github.md` e para `assets/github/`, e diz que sem
   resposta explicita o modulo nao ativa;
3. `references/github.md` existe, com secoes de ativacao, checklist do repositorio pela `gh`
   (descricao, topics, ruleset, labels) e fluxo bump, tag, Release;
4. `references/github.md` traz as respostas: `{{QUALITY_COMMAND}}` preenchido do `QUALITY.md`
   ou placeholder com aviso, nunca comando inventado; `{{SKILL_VERSION}}`; o limite do `.sha256`
   (integridade, nao autenticidade, DEC-005); `CODE_OF_CONDUCT.md` e `.gitattributes` perguntados
   item a item com os defaults (DEC-006); arquivo existente pulado, nunca mesclado, e listado
   (DEC-007);
5. `references/github.md` diz que a skill nao roda `gh` nem nada com efeito externo;
6. `README.md` da skill cita `references/github.md`;
7. `assets/docs/QUALITY.md` e `SKILL.md` dizem que a raiz minima admite `.github/` e dotfiles
   quando o modulo `github` esta ativo;
8. `evals/evals.json` com 14 entradas, ids 13 e 14 sobre o modulo `github` (ativar em projeto
   existente; scaffold com a pergunta 5 respondida);
9. sem travessao nos arquivos tocados; verificador em exit 0; raiz limpa em `--strict`.
"""

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, EVALS, ROOT, SKILL, check, ler, norm, resumo, validar, verify_ok  # noqa: E402

REF = SKILL / "references" / "github.md"
TRAVESSAO = chr(0x2014)


def secao(texto, titulo_re):
    m = re.search(r"^(#{2,4}) " + titulo_re + r".*$", texto, re.M)
    if not m:
        return ""
    nivel = len(m.group(1))
    resto = texto[m.end():]
    fim = re.search(r"^#{2,%d} " % nivel, resto, re.M)
    return resto[:fim.start()] if fim else resto


def main():
    skill = norm(ler(SKILL / "SKILL.md"))
    entrevista = secao(skill, r"3\. entrevista")
    p5 = re.search(r"\*\*5\..*?(?=\n\*\*\d+\.|\n```)", entrevista, re.S)
    p5 = p5.group(0) if p5 else ""
    check(bool(p5 and "github" in p5 and re.search(r"nao \(recomendado\)", p5) and "pt-br" in p5 and re.search(r"\ben\b|ingles", p5)),
          "1. pergunta 5 sobre o modulo github, 'Nao (recomendado)' e lingua en ou pt-BR no sim", p5[:120].replace("\n", " "))
    check("references/github.md" in skill and "assets/github/" in skill
          and re.search(r"(sem resposta|nunca ativ)[^\n]{0,160}github|github[^\n]{0,160}(sem resposta|nunca ativ)", skill),
          "2. SKILL.md aponta references/github.md e assets/github/, e nao ativa sem resposta explicita")

    ref = norm(ler(REF)) if REF.is_file() else ""
    check(bool(ref and re.search(r"^##+ .*ativ", ref, re.M) and re.search(r"^##+ .*(checklist|configura)", ref, re.M)
               and re.search(r"^##+ .*(release|tag)", ref, re.M)
               and all(t in ref for t in ("descri", "topic", "ruleset", "label"))),
          "3. references/github.md com ativacao, checklist gh (descricao, topics, ruleset, labels) e fluxo de Release",
          "ausente" if not ref else "")
    check(bool(ref and "{{quality_command}}" in ref and "{{skill_version}}" in ref and "integridade" in ref and "autenticidade" in ref
               and "code_of_conduct.md" in ref and ".gitattributes" in ref and re.search(r"item a item|por item", ref)
               and re.search(r"pul[ae]", ref) and re.search(r"nunca mescl|nao mescl", ref)
               and re.search(r"nunca inv|nao inv", ref)),
          "4. references/github.md com placeholders, limite do .sha256, defaults por item e arquivo existente pulado")
    check(bool(ref and re.search(r"(skill|agente)[^\n]{0,80}nao (roda|executa)[^\n]{0,40}`?gh`?|nunca (roda|executa)[^\n]{0,40}`?gh`?", ref)),
          "5. references/github.md diz que a skill nao roda gh")

    check("references/github.md" in ler(SKILL / "README.md"), "6. README.md da skill cita references/github.md")

    quality = norm(ler(ASSETS / "docs" / "QUALITY.md"))
    check(bool(re.search(r"\.github/[^\n]*github|github[^\n]*\.github/", quality)
               and re.search(r"\.github/[^\n]{0,200}(dotfile|arquivos? com ponto|\.gitattributes)", quality + skill)),
          "7. QUALITY.md do template e SKILL.md admitem .github/ e dotfiles com o modulo github ativo")

    evals = json.loads(ler(EVALS / "evals.json"))["evals"]
    novos = {e["id"]: norm(e["prompt"] + " " + e.get("expected_output", "")) for e in evals if e["id"] in (13, 14)}
    check(len(evals) == 14 and set(novos) == {13, 14} and all("github" in t for t in novos.values())
          and any("pergunta 5" in t or "scaffold" in t or "novo projeto" in t for t in novos.values()),
          "8. evals.json com 14 entradas, 13 e 14 sobre o modulo github", "%d entradas" % len(evals))

    tocados = [SKILL / "SKILL.md", REF, SKILL / "README.md", ASSETS / "docs" / "QUALITY.md", EVALS / "evals.json"]
    com_travessao = [p.name for p in tocados if p.is_file() and TRAVESSAO in ler(p)]
    ok, detalhe = verify_ok()
    codigo, saida, _ = validar(ROOT, "--strict")
    check(not com_travessao and ok and codigo == 0, "9. sem travessao, verificador em exit 0 e raiz limpa em --strict",
          "%s; %s; %s" % (", ".join(com_travessao), detalhe, saida[-1] if saida else ""))
    return resumo("T-108")


if __name__ == "__main__":
    sys.exit(main())
