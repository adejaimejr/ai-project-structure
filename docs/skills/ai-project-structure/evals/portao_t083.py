#!/usr/bin/env python3
"""Portao da T-083: bancada real da automacao do consenso neste repositorio.

Tarefa do agente de chat, nao do loop: a operacao escreve docs/CONSENSUS.md e a comparacao de
qualidade com a rodada na mao de 2026-09-03 e revisao-manual. Este portao cobra so o residuo
mecanico da rodada real:

1. um run dir em docs/consensus/ com modo=debate, status=concluida, dois participantes com
   resultado=posicao, comandos distintos, stdout acima de 500 bytes e sha256 batendo;
2. entrada em docs/CONSENSUS.md (ou no archive) com **Manifesto:** apontando para esse run, e a
   raiz limpa em --strict; 3. docs/MEMORY.md com perfis de consenso somente-leitura para Codex
   e Grok; 4. verificador em exit 0.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ROOT, autoteste, check, ler, manifesto, norm, resumo, rodadas, sha256, validar, verify_ok  # noqa: E402

# Linha de perfil, na forma de MEMORY.md (`- Ferramenta, intencao: comando`). A forma
# solta `codex.*consenso.*read-only` casava a nota do cursor-agent, que cita os tres.
RE_CODEX = re.compile(r"^\s*-\s*codex,\s*consenso:.*read-only.*$", re.M)
RE_GROK = re.compile(r"^\s*-\s*grok,\s*consenso:.*--mode ask.*$", re.M)


def run_valido(run):
    m = manifesto(run)
    if m.get("modo") != "debate" or m.get("status") != "concluida":
        return None
    posicoes = [p for p in m.get("participantes", []) if isinstance(p, dict) and p.get("resultado") == "posicao"]
    if len(posicoes) < 2:
        return None
    comandos = {tuple(p.get("comando") or []) for p in posicoes}
    for p in posicoes:
        f = run / str(p.get("id")) / "stdout.txt"
        if not f.is_file() or f.stat().st_size <= 500 or sha256(f) != p.get("sha256_stdout"):
            return None
    return m if len(comandos) >= 2 else None


def main():
    autoteste(RE_CODEX, norm("  - Codex, consenso: `codex exec -s read-only --skip-git-repo-check -m gpt-5.6-terra`"),
              contra=norm("  - **`cursor-agent` funciona para o Grok**, mais Codex e GPT. Perfil de consenso (read-only por construcao): `cursor-agent -p --mode ask`"))
    autoteste(RE_GROK, norm("  - Grok, consenso: `cursor-agent -p --mode ask --force --model cursor-grok-4.6-xhigh`"),
              contra=norm("  - Grok, executar: `grok --always-approve -p`. Perfil de consenso: `cursor-agent -p --mode ask`"))

    validos = [(run, run_valido(run)) for run in rodadas(ROOT)]
    validos = [(run, m) for run, m in validos if m]
    check(bool(validos), "1. run dir real em docs/consensus/: debate concluido, dois participantes com posicao, comandos distintos, bruto acima de 500 bytes, sha256 batendo",
          ", ".join(run.name for run in rodadas(ROOT)) or "nenhum run dir")

    textos = [ler(ROOT / "docs" / "CONSENSUS.md")] + [ler(p) for p in (ROOT / "docs" / "archive").glob("CONSENSUS-*.md")]
    pontes = [run for run, _ in validos if any(f"**Manifesto:** docs/consensus/{run.name}/manifesto.json" in t for t in textos)]
    code, out, _ = validar(ROOT, "--strict", "--codigos")
    check(bool(pontes) and code == 0 and not out, "2. entrada com ponte para o manifesto real e raiz limpa em --strict",
          f"pontes={[r.name for r in pontes]} strict exit {code} {'; '.join(out)[:100]}")

    memoria = norm(ler(ROOT / "docs" / "MEMORY.md"))
    check(RE_CODEX.search(memoria) and RE_GROK.search(memoria), "3. docs/MEMORY.md com perfis de consenso somente-leitura para Codex e Grok",
          f"codex={'sim' if RE_CODEX.search(memoria) else 'nao'} grok={'sim' if RE_GROK.search(memoria) else 'nao'}")

    ok, det = verify_ok()
    check(ok, "4. verify_repository.py exit 0", det)
    return resumo("T-083")


if __name__ == "__main__":
    sys.exit(main())
