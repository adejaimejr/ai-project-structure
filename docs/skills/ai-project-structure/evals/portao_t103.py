#!/usr/bin/env python3
"""Portao da T-103: residuo mecanico da bancada real do adaptador Cloudroom (spec 0008).

Tarefa do agente de chat, nao do loop: ela registra perfil em `docs/MEMORY.md` e escreve a
evidencia da comparacao. Escrito pelo agente de planejamento em 2026-10-21; hoje falha pelo
motivo certo: nao ha perfil nem rodada real.

1. `docs/MEMORY.md` tem o perfil `Cloudroom, executar:` com `cloudroom_agente.py --provider`
   (o caminho da skill e placeholder que o agente de chat resolve; o modelo vem do usuario);
2. `docs/TASKS.md` tem em Concluidas uma tarefa fechada pelo loop com `agente=` citando
   `cloudroom_agente.py` (a bancada real: a T-101 e a candidata);
3. a propria T-103 esta concluida com evidencia que cita o id da thread filha (`cr_child_`)
   e `tipo=revisao-manual` ou `tipo=conferencia` (comparacao e julgamento humano);
4. verificador exit 0.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ROOT, autoteste, check, ler, norm, resumo, verify_ok  # noqa: E402

RE_PERFIL = re.compile(r"^\s*-\s*cloudroom,\s*executar:.*cloudroom_agente\.py.*--provider\s+\S+", re.M)
RE_EVIDENCIA_LOOP = re.compile(r"^\s*-\s*evidencia:\s*tipo=comando;\s*agente=[^;]*cloudroom_agente\.py[^;]*--provider", re.M)
RE_T103 = re.compile(r"^- \d{4}-\d{2}-\d{2} t-103:.*\n\s*-\s*evidencia:\s*tipo=(?:revisao-manual|conferencia);[^\n]*cr_child_", re.M)

autoteste(RE_PERFIL, norm("  - Cloudroom, executar: `python3 <skill>/scripts/cloudroom_agente.py --provider claude-code --model claude-sonnet-5-5`"),
          contra=norm("  - Claude, executar: `claude -p --permission-mode bypassPermissions --model opus`"))
autoteste(RE_EVIDENCIA_LOOP, norm("  - Evidencia: tipo=comando; agente=python3 /x/scripts/cloudroom_agente.py --provider claude-code --model m; procedimento=bash portao.sh; resultado=exit 0"),
          contra=norm("  - Evidencia: tipo=comando; agente=claude -p; procedimento=bash portao.sh; resultado=exit 0"))
autoteste(RE_T103, norm("- 2026-10-22 T-103: Bancada real. (spec: 0008-adaptador-cloudroom)\n  - Evidencia: tipo=revisao-manual; procedimento=loop.sh na T-101 pelo adaptador, thread cr_child_abc; resultado=verde"),
          contra=norm("- 2026-10-22 T-103: Bancada real.\n  - Evidencia: tipo=comando; procedimento=x; resultado=cr_child_abc"))


def main():
    memoria = norm(ler(ROOT / "docs" / "MEMORY.md"))
    check(bool(RE_PERFIL.search(memoria)), "1. docs/MEMORY.md tem o perfil Cloudroom, executar com cloudroom_agente.py --provider")
    tasks = norm(ler(ROOT / "docs" / "TASKS.md"))
    concluidas = tasks.split("## concluidas", 1)[1] if "## concluidas" in tasks else ""
    check(bool(RE_EVIDENCIA_LOOP.search(concluidas)),
          "2. uma tarefa em Concluidas foi fechada pelo loop com agente= citando cloudroom_agente.py --provider")
    check(bool(RE_T103.search(concluidas)),
          "3. T-103 concluida com evidencia revisao-manual ou conferencia citando o id da thread filha (cr_child_)")
    ok, detalhe = verify_ok()
    check(ok, "4. verify_repository.py em exit 0", detalhe)
    return resumo("T-103")


if __name__ == "__main__":
    sys.exit(main())
