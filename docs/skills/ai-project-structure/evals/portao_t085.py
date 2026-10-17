#!/usr/bin/env python3
"""Portao da T-085: a fixture `aguardando-project` nao envelhece.

O validador compara `(bloqueada: AAAA-MM-DD)` com `date.today()` (limite
`BLOCKED_MAX_DAYS`). Data absoluta na fixture passa do limite sozinha e o
verificador cai sem regressao nenhuma: em 2026-10-17 as datas de setembro de
2026 derrubaram `verify_repository.py` para 71/74 e, com ele, todo portao da
spec 0006 que o chama.

1. A fixture nao carrega data absoluta em `(bloqueada:)`: usa o token `{{HOJE-N}}`,
   que o verificador materializa relativo ao dia da execucao. `valido` sai limpo em
   `--strict`; `invalido` continua acusando uma bloqueada antiga de proposito, e o
   oracle a espera.
2. Viagem no tempo, pela mesma funcao que o verificador usa: materializada como se
   hoje fosse um ano atras, `valido` ganha TASK-BLOQUEADA-ANTIGA; como se fosse
   daqui a um ano, `invalido` perde a dele. Fixture com data absoluta sairia igual
   nas tres materializacoes: e isso que estes checks acusam.
3. Em projeto real o check segue relativo a hoje (`date.today()` continua no
   validador), a raiz passa em `--strict`, a versao e coerente e o verificador sai 0.

Vive em `evals/`, nao e distribuido, e nunca grava bytecode.
"""

import os
import re
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ROOT = SKILL.parents[2]
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
FIXTURE = EVALS / "fixtures" / "aguardando-project"
DATA_ABSOLUTA_RE = re.compile(r"\(bloqueada:\s*\d{4}-\d{2}-\d{2}\s*\)")
TOKEN_RE = re.compile(r"\{\{HOJE([+-]\d+)?\}\}")
ANTIGA = "TASK-BLOQUEADA-ANTIGA"
falhas = []

sys.path.insert(0, str(EVALS))
import verify_repository as vr  # noqa: E402


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def materializar_e_validar(caso, hoje, strict):
    """Materializa `caso` com a funcao do verificador e roda o validador real.

    Devolve (exit, linhas, detalhe). Sem a funcao no verificador, devolve exit None:
    e o estado anterior ao conserto e conta como falha em quem chamar."""
    fn = getattr(vr, "materializar_fixture", None)
    if fn is None:
        return None, [], "verify_repository.py nao expoe materializar_fixture(origem, destino, hoje)"
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "fixture"
        fn(FIXTURE / caso, destino, hoje=hoje)
        code, out = vr.rodar_validador(destino, strict=strict, codigos=True)
    linhas = [l for l in out.splitlines() if l.strip()]
    return code, linhas, f"exit {code}; " + ("; ".join(linhas) if linhas else "sem diagnostico")


def versao_coerente(acima_de):
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    ok_acima = tuple(int(x) for x in versao.split(".")) >= tuple(int(x) for x in acima_de.split("."))
    prosa = set(re.findall(r"versao da estrutura:\s*(\d+\.\d+\.\d+)", skill, re.I))
    marcadores = set()
    for path in (ASSETS / "AGENTS.md", ASSETS / "partials" / "AGENTS-specs-block.md", ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(re.findall(r":start\s+v(\d+\.\d+\.\d+)", path.read_text(encoding="utf-8")))
    partes = (SKILL / "CHANGELOG.md").read_text(encoding="utf-8").split("\n## ", 2)
    recente = partes[1] if len(partes) > 1 else ""
    return versao, ok_acima and prosa == {versao} and marcadores == {versao} and recente.startswith(versao), f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}"


def verify_ok(minimo):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True, errors="replace", env=env)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), p.stdout.strip()[-160:])
    m = re.search(r"(\d+)/(\d+)", resumo)
    total = int(m.group(2)) if m else 0
    return p.returncode == 0 and total >= minimo, resumo


def main():
    hoje = date.today()
    ano_atras = hoje - timedelta(days=365)
    ano_frente = hoje + timedelta(days=365)

    # 1. Forma da fixture e comportamento no dia real.
    absolutas, tokens = [], 0
    for caso in ("valido", "invalido"):
        for md in sorted((FIXTURE / caso).rglob("*.md")):
            texto = md.read_text(encoding="utf-8")
            absolutas += [f"{caso}/{md.relative_to(FIXTURE / caso).as_posix()}: {m.group(0)}" for m in DATA_ABSOLUTA_RE.finditer(texto)]
            tokens += len(TOKEN_RE.findall(texto))
    check(not absolutas and tokens > 0, "1a. fixture sem data absoluta em (bloqueada:), com token {{HOJE-N}}", "; ".join(absolutas) or f"{tokens} token(s)")

    code, linhas, det = materializar_e_validar("valido", hoje, strict=True)
    check(code == 0 and not linhas, "1b. valido materializada hoje: --strict exit 0, sem diagnostico", det)

    code, linhas, det = materializar_e_validar("invalido", hoje, strict=False)
    oracle = vr.FIXTURES.get("aguardando-project/invalido", {}).get("diagnosticos", [])
    acusa = any(ANTIGA in l for l in linhas)
    esperado = any(ANTIGA in d for d in oracle)
    check(code == 1 and acusa and esperado, "1c. invalido materializada hoje acusa uma bloqueada antiga de proposito, e o oracle a espera",
          f"exit {code}; acusa={acusa}; no oracle={esperado}")

    # 2. Viagem no tempo: a data gerada acompanha `hoje`.
    code, linhas, det = materializar_e_validar("valido", ano_atras, strict=True)
    check(code == 1 and any(ANTIGA in l for l in linhas), "2a. valido materializada como um ano atras ganha TASK-BLOQUEADA-ANTIGA", det)

    code, linhas, det = materializar_e_validar("invalido", ano_frente, strict=False)
    check(code is not None and not any(ANTIGA in l for l in linhas), "2b. invalido materializada como daqui a um ano perde a antiga (ela tambem e relativa)",
          det if code is None else f"exit {code}; antigas={sum(ANTIGA in l for l in linhas)}")

    # 3. Projeto real e integridade do repositorio.
    p = subprocess.run([sys.executable, str(VALIDATOR), str(ROOT), "--strict"], capture_output=True, text=True, errors="replace")
    check(p.returncode == 0, "3a. validate_structure.py --strict na raiz: exit 0", f"exit {p.returncode}")
    fonte = VALIDATOR.read_text(encoding="utf-8")
    check("date.today()" in fonte and "BLOCKED_MAX_DAYS" in fonte, "3b. validador segue relativo a hoje em projeto real (date.today e BLOCKED_MAX_DAYS no fonte)")
    versao, ok, det = versao_coerente("2.11.0")
    check(ok, "3c. versao 2.11.0 ou acima, coerente", det)
    ok, resumo = verify_ok(74)
    check(ok, "3d. verify_repository.py exit 0 com 74 ou mais verificacoes", resumo)

    total = 9
    print(f"\nPortao T-085: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
