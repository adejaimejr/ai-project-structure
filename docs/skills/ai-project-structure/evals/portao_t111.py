#!/usr/bin/env python3
"""Portao da T-111: o check 1 de `portao_t102.py` nao pode imprimir detalhe de falha quando passa.

Tarefa real e pequena, escolhida para a bancada da T-103 (spec 0008): o loop roda com o
adaptador Cloudroom e `--projeto` igual a pasta da thread. Escrito pelo gestor em 2026-10-21,
antes da rodada. Falha hoje pelo motivo certo depois da T-102: `portao_t102.py` sai 14/14,
mas a linha `[OK  ] 1.` termina em ": secao faltando", porque o detalhe e calculado sem olhar
se o check passou (o mesmo defeito que o `portao_t100.py` tinha no check 1).

1. `portao_t102.py` sai 0 com `Portao T-102: 14/14.` (o conserto nao pode quebrar o portao);
2. nenhuma linha `[OK  ]` do `portao_t102.py` traz detalhe de falha (": secao faltando" ou ": ausente");
3. o detalhe continua no caminho da falha: a fonte ainda tem "secao faltando" e "ausente"
   (apagar a mensagem deixaria o check 2 verde e perderia informacao; e o "nao apague o que falha").
"""

import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import EVALS, autoteste, check, ler, resumo  # noqa: E402

ALVO = EVALS / "portao_t102.py"
RE_OK_COM_DETALHE = re.compile(r"^\[OK  \] .*: (?:secao faltando|ausente)\s*$", re.M)
autoteste(RE_OK_COM_DETALHE, "[OK  ] 1. references/cloudroom.md existe com secoes de uso: secao faltando\n",
          contra="[FALHA] 1. references/cloudroom.md existe: secao faltando\n[OK  ] 1b. tabela de exit codes\n")


def main():
    p = subprocess.run([sys.executable, str(ALVO)], capture_output=True, text=True, errors="replace",
                       env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": __import__("os").environ.get("PATH", "")})
    saida = p.stdout
    resumo_alvo = next((l for l in saida.splitlines() if l.startswith("Portao T-102:")), "sem linha Portao")
    check(p.returncode == 0 and resumo_alvo.strip() == "Portao T-102: 14/14.",
          "1. portao_t102.py sai 0 com 14/14", "exit %s, %s" % (p.returncode, resumo_alvo))
    com_detalhe = RE_OK_COM_DETALHE.findall(saida)
    check(p.returncode == 0 and not com_detalhe,
          "2. nenhuma linha [OK] do portao_t102.py traz detalhe de falha",
          "; ".join(l.strip()[:90] for l in com_detalhe))
    fonte = ler(ALVO)
    check("secao faltando" in fonte and '"ausente"' in fonte,
          "3. o detalhe continua no caminho da falha (a fonte ainda tem 'secao faltando' e 'ausente')")
    return resumo("T-111")


if __name__ == "__main__":
    sys.exit(main())
