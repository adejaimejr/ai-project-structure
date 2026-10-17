#!/usr/bin/env python3
"""Portao da T-082: documentacao da automacao do consenso.

Sem `verify_repository.py`: o `docs/CONSENSUS.md` da raiz precisa da mesma secao nova do template
e e proibido ao agente do loop; o agente de chat propaga depois (como em T-063).

1. `references/consenso.md` existe com uso, tabela de exit codes 0/1/2/5/6, comandos somente-
   leitura por ferramenta, sidecar, Origem, falso negativo da varredura, retomada e o que a
   operacao nunca faz; 2. `SKILL.md` com secao de consenso citando o script, --agente,
   docs/MEMORY.md, exit codes e julgamento humano, description com gatilho, versao em prosa
   coerente; 3. template de CONSENSUS.md com a secao fora de cerca e modelos cercados iguais aos
   da raiz; 4. `verificar_convencoes` cobra `**Origem:**`; 5. README, CHANGELOG 2.11.0 e
   evals.json; 6. projeto dos assets e raiz limpos em --strict; 7. versao coerente.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import (ASSETS, EVALS, ROOT, SKILL, autoteste, check, ler, montar, norm, resumo,  # noqa: E402
                                 validar, versao_coerente)

RE_EXIT = {c: re.compile(r"^\|\s*" + c + r"\s*\|", re.M) for c in ("0", "1", "2", "5", "6")}
RE_NUNCA = re.compile(r"^##+ [^\n]*nunca", re.M)
RE_SECAO_CONSENSO = re.compile(r"^## ([^\n]*consenso[^\n]*)$", re.M)
RE_DESCRIPTION = re.compile(r"^description:.*consenso", re.M)


def sem_cercas(texto):
    return re.sub(r"^\s*(`{3,}|~{3,}).*?^\s*\1\s*$", "", texto, flags=re.M | re.S)


def modelo(texto, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r"\s*$\s*```md\n(.*?)```", texto, re.M | re.S)
    return m.group(1) if m else None


def secao_skill(texto):
    m = RE_SECAO_CONSENSO.search(texto)
    if not m:
        return ""
    resto = texto[m.end():]
    fim = re.search(r"^## ", resto, re.M)
    return resto[:fim.start()] if fim else resto


def main():
    autoteste(RE_EXIT["5"], "| 5 | outra rodada ativa |", contra="| 50 | x |")
    autoteste(RE_NUNCA, norm("## O Que A Operacao Nunca Faz"), contra=norm("nunca no meio da prosa"))
    autoteste(RE_SECAO_CONSENSO, norm("## Rodar Uma Rodada De Consenso"), contra=norm("### Rodar Uma Rodada De Consenso"))
    autoteste(RE_DESCRIPTION, norm("description: Use para rodar uma rodada de consenso automatizada"), contra=norm("name: consenso"))

    ref = SKILL / "references" / "consenso.md"
    t = norm(ler(ref)) if ref.is_file() else ""
    ok1 = (ref.is_file() and "consenso.py" in t and all(rx.search(t) for rx in RE_EXIT.values())
           and "-s read-only" in t and "--mode ask" in t and "docs/consensus/" in t and "**origem:**" in t
           and "falso negativo" in t and "retomar" in t and RE_NUNCA.search(t) and "--agente" in t)
    faltas = [k for k, v in (("arquivo", ref.is_file()), ("consenso.py", "consenso.py" in t), ("exit codes", all(rx.search(t) for rx in RE_EXIT.values())),
                             ("-s read-only", "-s read-only" in t), ("--mode ask", "--mode ask" in t), ("docs/consensus/", "docs/consensus/" in t),
                             ("**Origem:**", "**origem:**" in t), ("falso negativo", "falso negativo" in t), ("retomar", "retomar" in t),
                             ("secao nunca", bool(RE_NUNCA.search(t))), ("--agente", "--agente" in t)) if not v]
    check(ok1, "1. references/consenso.md com uso, exit codes, comandos somente-leitura, sidecar, Origem, falso negativo, retomada e o que nunca faz",
          "faltando: " + ", ".join(faltas) if faltas else "")

    skill = ler(SKILL / "SKILL.md")
    sec = norm(secao_skill(norm(skill)))
    ok2 = (bool(sec) and "consenso.py" in sec and "--agente" in sec and "docs/memory.md" in sec
           and all(re.search(r"\b" + c + r"\b", sec) for c in ("0", "2", "5", "6"))
           and ("julgamento" in sec or "a preencher" in sec) and RE_DESCRIPTION.search(norm(skill)))
    check(ok2, "2. SKILL.md com secao de consenso citando consenso.py, --agente, docs/MEMORY.md, exit codes e julgamento humano; description com gatilho",
          f"secao={'sim' if sec else 'nao'} description={'sim' if RE_DESCRIPTION.search(norm(skill)) else 'nao'}")

    template = ler(ASSETS / "docs" / "CONSENSUS.md")
    raiz = ler(ROOT / "docs" / "CONSENSUS.md")
    fora = sem_cercas(template)
    ok3 = (all(x in fora for x in ("**Origem:**", "**Manifesto:**", "**Participantes:**", "docs/consensus/"))
           and all(modelo(template, m) is not None and modelo(template, m) == modelo(raiz, m) for m in ("Modelo De Debate", "Modelo De Achado")))
    check(ok3, "3. template de CONSENSUS.md com a secao de entrada automatizada fora de cerca, e modelos cercados iguais aos da raiz")

    verify = ler(EVALS / "verify_repository.py")
    check("**Origem:**" in verify, "4. verificar_convencoes cobra **Origem:** no template e na raiz")

    readme = norm(ler(SKILL / "README.md"))
    versao, ok_v, recente, det = versao_coerente("2.11.0")
    ok5_changelog = "consenso" in norm(recente) and ("references/consenso.md" in norm(recente) or "documenta" in norm(recente))
    try:
        evals = json.loads(ler(EVALS / "evals.json")).get("evals", [])
    except ValueError:
        evals = []
    eval_ok = any("consenso" in norm(e.get("prompt", "")) and all((EVALS / f).exists() for f in e.get("files", [])) for e in evals if isinstance(e, dict))
    check("consenso.py" in readme and ok5_changelog and eval_ok, "5. README cita consenso.py, CHANGELOG 2.11.0 cita a documentacao, evals.json tem eval de consenso",
          f"readme={'consenso.py' in readme} changelog={ok5_changelog} eval={eval_ok}")

    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo")
        code, out, _ = validar(r, "--strict", "--codigos")
        check(code == 0 and not out, "6a. projeto montado dos assets passa em --strict", "; ".join(out)[:160])
    code, out, _ = validar(ROOT, "--strict", "--codigos")
    check(code == 0 and not out, "6b. raiz limpa em --strict", "; ".join(out)[:160])
    check(ok_v, "7. versao 2.11.0 ou acima, coerente", det)
    return resumo("T-082")


if __name__ == "__main__":
    sys.exit(main())
