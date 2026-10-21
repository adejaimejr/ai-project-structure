#!/usr/bin/env python3
"""Portao da T-106: assets do modulo `github` e partial do bloco (spec 0007).

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: `assets/github/` e `assets/partials/AGENTS-github-block.md` nao existem.

1. `assets/github/en/` e `assets/github/pt-BR/` tem exatamente a lista da spec, nada a mais
   (sem `release.yml`, DEC-001);
2. nenhum travessao (U+2014) em arquivo do modulo;
3. nada especifico deste repositorio: `adejaimejr` e `ai-project-structure` so aparecem no
   `ci.yml` (URL da Release, DEC-005); `verify_repository` nao aparece em lugar nenhum;
4. `ci.yml`: toda action fixada por SHA de 40 caracteres com versao em comentario,
   `permissions: contents: read`, `concurrency` com `cancel-in-progress: true`;
5. `ci.yml` (DEC-005): baixa o zip e o `.sha256` da Release `v{{SKILL_VERSION}}`, roda
   `sha256sum -c` e `validate_structure.py . --strict`, e em passo separado roda
   `{{QUALITY_COMMAND}}`;
6. `ci.yml`, `dependabot.yml` e `.gitattributes` identicos nas duas linguas (workflow nao se
   traduz; a lingua so muda texto para pessoas);
7. `config.yml` com `blank_issues_enabled: false`; `dependabot.yml` so com `github-actions`,
   mensal; `.gitattributes` com `* text=auto eol=lf`;
8. linguas de fato: `CONTRIBUTING.md` e `SECURITY.md` diferem entre en e pt-BR, e cada um usa
   palavras da propria lingua; `CODE_OF_CONDUCT.md` cita o Contributor Covenant 2.1 nas duas;
9. partial `assets/partials/AGENTS-github-block.md`: marcadores `github` pareados com versao
   igual a do bloco core, em pt-BR, com as regras (`.github/`, pull request, tag anotada,
   Release, `gh`), ate 25 linhas nao vazias entre os marcadores;
10. o partial nao cita este repositorio;
11. verificador em exit 0 e `validate_structure.py . --strict` limpo (nada mudou fora do modulo).
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, ROOT, check, ler, norm, resumo, validar, verify_ok  # noqa: E402

BASE = ASSETS / "github"
PARTIAL = ASSETS / "partials" / "AGENTS-github-block.md"
LISTA = sorted([
    "docs/CONTRIBUTING.md", "docs/SECURITY.md", "docs/CODE_OF_CONDUCT.md", "docs/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug.yml", ".github/ISSUE_TEMPLATE/feature.yml", ".github/ISSUE_TEMPLATE/config.yml",
    ".github/dependabot.yml", ".github/workflows/ci.yml", ".gitattributes",
])
IDENTICOS = (".github/workflows/ci.yml", ".github/dependabot.yml", ".gitattributes")
TRAVESSAO = chr(0x2014)
RE_USES = re.compile(r"^\s*-?\s*uses:\s*(\S+)(.*)$", re.M)
RE_PIN = re.compile(r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")


def arquivos(lingua):
    raiz = BASE / lingua
    if not raiz.is_dir():
        return []
    return sorted(str(p.relative_to(raiz)) for p in raiz.rglob("*") if p.is_file())


def texto(lingua, rel):
    p = BASE / lingua / rel
    return ler(p) if p.is_file() else ""


def main():
    en, pt = arquivos("en"), arquivos("pt-BR")
    check(en == LISTA and pt == LISTA, "1. en e pt-BR com exatamente a lista da spec (sem release.yml)",
          "en=%d pt-BR=%d; faltam=%s; sobram=%s" % (len(en), len(pt), sorted(set(LISTA) - set(en) | set(LISTA) - set(pt)),
                                                    sorted(set(en) - set(LISTA) | set(pt) - set(LISTA))))

    todos = [(l, r) for l in ("en", "pt-BR") for r in arquivos(l)]
    com_travessao = ["%s/%s" % (l, r) for l, r in todos if TRAVESSAO in texto(l, r)]
    check(bool(todos) and not com_travessao and TRAVESSAO not in (ler(PARTIAL) if PARTIAL.is_file() else ""),
          "2. sem travessao nos arquivos do modulo nem no partial", ", ".join(com_travessao))

    especificos = ["%s/%s" % (l, r) for l, r in todos
                   if r != ".github/workflows/ci.yml" and re.search(r"adejaimejr|ai-project-structure", texto(l, r))]
    check(bool(todos) and not especificos and not any("verify_repository" in texto(l, r) for l, r in todos),
          "3. nada deste repositorio fora da URL da Release no ci.yml", ", ".join(especificos))

    ci = texto("en", ".github/workflows/ci.yml")
    usos = RE_USES.findall(ci)
    sem_pin = [u for u, resto in usos if not RE_PIN.match(u) or not re.search(r"#\s*v\d", resto)]
    check(bool(usos) and not sem_pin and re.search(r"^permissions:\s*\n\s+contents:\s*read\s*$", ci, re.M)
          and re.search(r"^concurrency:", ci, re.M) and re.search(r"cancel-in-progress:\s*true", ci),
          "4. ci.yml com actions por SHA e versao em comentario, contents: read e concurrency cancelando",
          "sem pin: %s" % sem_pin if sem_pin else "")

    url = re.search(r"releases/download/v\{\{SKILL_VERSION\}\}/ai-project-structure-\{\{SKILL_VERSION\}\}\.zip", ci)
    passos = re.split(r"^\s*-\s+name:", ci, flags=re.M)
    p_valida = [p for p in passos if "validate_structure.py . --strict" in p]
    p_quality = [p for p in passos if "{{QUALITY_COMMAND}}" in p]
    check(bool(url) and ".sha256" in ci and "sha256sum -c" in ci and p_valida and p_quality
          and not set(map(id, p_valida)) & set(map(id, p_quality)),
          "5. ci.yml baixa zip e .sha256 da Release fixada, sha256sum -c, validador --strict, e QUALITY em passo separado")

    diferentes = [r for r in IDENTICOS if not texto("en", r) or texto("en", r) != texto("pt-BR", r)]
    check(not diferentes, "6. ci.yml, dependabot.yml e .gitattributes identicos nas duas linguas", ", ".join(diferentes))

    config = texto("en", ".github/ISSUE_TEMPLATE/config.yml") + texto("pt-BR", ".github/ISSUE_TEMPLATE/config.yml")
    dep = texto("en", ".github/dependabot.yml")
    check(config.count("blank_issues_enabled: false") == 2
          and re.findall(r"package-ecosystem:\s*\"?([\w-]+)", dep) == ["github-actions"]
          and re.search(r"interval:\s*\"?monthly", dep)
          and texto("en", ".gitattributes").strip().splitlines()[:1] == ["* text=auto eol=lf"],
          "7. config.yml sem issue em branco, dependabot so github-actions mensal, .gitattributes eol=lf")

    def lingua_ok(rel):
        e, p = norm(texto("en", rel)), norm(texto("pt-BR", rel))
        return e and p and e != p and len(re.findall(r"\bthe\b", e)) >= 3 and len(re.findall(r"\b(?:para|projeto|voce)\b", p)) >= 3
    coc = [texto(l, "docs/CODE_OF_CONDUCT.md") for l in ("en", "pt-BR")]
    check(lingua_ok("docs/CONTRIBUTING.md") and lingua_ok("docs/SECURITY.md")
          and all("Contributor Covenant" in c and "2.1" in c for c in coc),
          "8. CONTRIBUTING e SECURITY de fato em cada lingua; CODE_OF_CONDUCT cita o Contributor Covenant 2.1 nas duas")

    parcial = ler(PARTIAL) if PARTIAL.is_file() else ""
    m = re.search(r"<!--\s*ai-project-structure:github:start\s+v(\d+\.\d+\.\d+)\s*-->(.*?)<!--\s*ai-project-structure:github:end\s*-->",
                  parcial, re.S)
    core = re.search(r"ai-project-structure:core:start\s+v(\d+\.\d+\.\d+)", ler(ASSETS / "AGENTS.md"))
    corpo = norm(m.group(2)) if m else ""
    linhas = [l for l in (m.group(2).splitlines() if m else []) if l.strip()]
    check(bool(m and core and m.group(1) == core.group(1) and len(linhas) <= 25
               and all(t in corpo for t in (".github/", "pull request", "tag anotada", "release", "`gh`"))
               and re.search(r"\b(?:nao|para|mudanca)\b", corpo)),
          "9. partial com marcadores github pareados na versao do core, regras em pt-BR, ate 25 linhas",
          ("versao %s, core %s, %d linhas" % (m.group(1), core.group(1) if core else "?", len(linhas))) if m else "partial ausente ou sem marcadores")
    check(bool(parcial) and not re.search(r"adejaimejr|github\.com/", parcial), "10. o partial nao cita este repositorio")

    ok, detalhe = verify_ok()
    codigo, saida, _ = validar(ROOT, "--strict")
    check(ok and codigo == 0, "11. verificador em exit 0 e raiz limpa em --strict", "%s; %s" % (detalhe, saida[-1] if saida else ""))
    return resumo("T-106")


if __name__ == "__main__":
    sys.exit(main())
