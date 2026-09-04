#!/usr/bin/env python3
"""Portao da T-073: `install.sh` avisa e pede confirmacao em destino divergente (REVAL-7).

Roda o instalador com HOME falso e stdin controlado. Casos:

1. Destino inexistente: instala, exit 0, sem pergunta.
2. Destino identico: reinstala, exit 0, sem pergunta.
3. Destino divergente (arquivo editado e arquivo extra), sem terminal e sem
   flag: recusa com exit diferente de zero, lista os arquivos divergentes e
   NAO sobrescreve.
4. Destino divergente com `--sim`: sobrescreve, exit 0.
5. Destino divergente com resposta `s` no stdin: sobrescreve; com `n`: recusa e
   nao sobrescreve.
6. `__pycache__` continua fora do destino.
7. `--help` documenta `--sim`.
8. `verify_repository.py` exercita destino divergente (cita "diverg" em
   `verificar_install` ou em etapa propria) e sai 0.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
INSTALL = SKILL / "install.sh"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def instalar(home, *args, stdin=None):
    env = dict(os.environ, HOME=str(home))
    p = subprocess.run(["bash", str(INSTALL), "--claude", *args], cwd=str(home), env=env,
                       capture_output=True, text=True, input=stdin,
                       stdin=(subprocess.DEVNULL if stdin is None else None))
    return p.returncode, p.stdout + p.stderr


def main():
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp) / "home"
        home.mkdir()
        dest = home / ".claude" / "skills" / "ai-project-structure"

        code, out = instalar(home)
        check(code == 0 and dest.is_dir() and "[s/N]" not in out and "?" not in out.split("Concluido")[0][-40:],
              "1. destino inexistente instala sem pergunta", f"exit {code}")

        code, out = instalar(home)
        check(code == 0 and "diverg" not in out.lower(), "2. destino identico reinstala sem pergunta", f"exit {code}")

        (dest / "SKILL.md").open("a", encoding="utf-8").write("\neditado localmente\n")
        (dest / "extra.md").write_text("x", encoding="utf-8")
        code, out = instalar(home)
        editado = "editado localmente" in (dest / "SKILL.md").read_text(encoding="utf-8")
        check(code != 0 and editado and "SKILL.md" in out and "extra.md" in out,
              "3. divergente sem terminal e sem flag: recusa, lista e nao sobrescreve",
              f"exit {code}; editado preservado={editado}; " + out.strip().replace("\n", " ")[-160:])

        code, out = instalar(home, stdin="n\n")
        editado = "editado localmente" in (dest / "SKILL.md").read_text(encoding="utf-8")
        check(code != 0 and editado, "5b. divergente com resposta n: recusa e nao sobrescreve", f"exit {code}")

        code, out = instalar(home, stdin="s\n")
        editado = "editado localmente" in (dest / "SKILL.md").read_text(encoding="utf-8")
        check(code == 0 and not editado, "5a. divergente com resposta s: sobrescreve", f"exit {code}")

        (dest / "SKILL.md").open("a", encoding="utf-8").write("\neditado de novo\n")
        code, out = instalar(home, "--sim")
        editado = "editado de novo" in (dest / "SKILL.md").read_text(encoding="utf-8")
        check(code == 0 and not editado, "4. divergente com --sim: sobrescreve sem perguntar", f"exit {code}")

        check(not list(dest.rglob("__pycache__")), "6. nenhum __pycache__ no destino")

    code, out = instalar(Path(tempfile.mkdtemp()), "--help")
    check("--sim" in out, "7. --help documenta --sim")

    vr = (EVALS / "verify_repository.py").read_text(encoding="utf-8")
    corpo = vr.split("def verificar_install", 1)[-1].split("\ndef ", 1)[0].lower()
    check("diverg" in corpo and "--sim" in corpo,
          "8a. verificar_install exercita destino divergente com e sem --sim")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True, env=env)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "8b. verify_repository.py exit 0", resumo)

    total = 10
    print(f"\nPortao T-073: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
