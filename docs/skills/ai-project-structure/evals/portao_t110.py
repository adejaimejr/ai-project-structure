#!/usr/bin/env python3
"""Portao da T-110: `description` do `SKILL.md` dentro do teto de 1024 caracteres do padrao Agent Skills.

Escrito pelo agente de coordenacao em 2026-10-21, antes do trabalho. Hoje falha pelo motivo
certo: o `description` tem 1479 caracteres. O texto novo foi aprovado pelo usuario no chat.

1. o `description` tem de 1 a 1024 caracteres (agentskills.io/specification);
1b. o `description` e YAML seguro sem aspas: nada de ": " nem " #" (a 2.14.0 saiu com ": " no meio, invalido para parser estrito);
2. ficam os gatilhos: estrutura multiagente, `AGENTS.md e docs/`, memoria do projeto em
   `docs/`, converter, ATUALIZAR, VALIDAR, specs, loop (ativar, rodar, configurar), modulo
   github, consenso ("roda um consenso", "segunda opiniao", "revalida o achado", "retoma a
   rodada");
3. fica a regra de nao disparar em pedido generico ("cria projeto", "inicia projeto novo",
   "monta a base"), com quem decide (usuario ou agente gestor) e a oferta em uma linha;
4. `name` continua `ai-project-structure` e igual ao nome da pasta;
5. versao coerente em 2.14.1 ou acima, com a secao mais recente do CHANGELOG da skill citando
   o `description`;
6. sem travessao no `SKILL.md`; verificador em exit 0; raiz limpa em `--strict`.

O portao prova que os gatilhos estao no texto, nao que o modelo dispara nos mesmos pedidos:
isso so um eval com modelo real mostra (limite declarado ao usuario).
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ROOT, SKILL, check, ler, norm, resumo, validar, verify_ok, versao_coerente  # noqa: E402

GATILHOS = ("estrutura multiagente", "agents.md e docs/", "memoria do projeto em docs/", "converter", "atualizar",
            "validar", "specs", "ativar, rodar ou configurar o loop", "modulo github", "roda um consenso",
            "segunda opiniao", "revalida o achado", "retoma a rodada")
NEGATIVOS = ("nao dispare", "cria projeto", "inicia projeto novo", "monta a base", "agente gestor", "uma linha")


def main():
    skill = ler(SKILL / "SKILL.md")
    fm = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    campos = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", fm.group(1), re.M)) if fm else {}
    desc = campos.get("description", "").strip()
    check(1 <= len(desc) <= 1024, "1. description com 1 a 1024 caracteres", "%d caracteres" % len(desc))
    check(desc and ": " not in desc and " #" not in desc, "1b. description em YAML seguro (sem ': ' nem ' #')")
    d = norm(desc)
    faltam = [g for g in GATILHOS if g not in d]
    check(not faltam, "2. gatilhos presentes", "faltam: %s" % faltam if faltam else "")
    faltam = [g for g in NEGATIVOS if g not in d]
    check(not faltam, "3. regra de nao disparar em pedido generico, com quem decide e oferta em uma linha",
          "faltam: %s" % faltam if faltam else "")
    check(campos.get("name", "").strip() == "ai-project-structure" == SKILL.name, "4. name igual ao nome da pasta")
    versao, ok_versao, recente, detalhe = versao_coerente("2.14.1")
    check(ok_versao and "description" in recente, "5. versao coerente em 2.14.1 ou acima, CHANGELOG citando o description", detalhe)
    ok, detalhe_v = verify_ok()
    codigo, saida, _ = validar(ROOT, "--strict")
    check(chr(0x2014) not in skill and ok and codigo == 0, "6. sem travessao, verificador em exit 0 e raiz limpa em --strict",
          "%s; %s" % (detalhe_v, saida[-1] if saida else ""))
    return resumo("T-110")


if __name__ == "__main__":
    sys.exit(main())
