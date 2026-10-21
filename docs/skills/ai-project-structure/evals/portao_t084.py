#!/usr/bin/env python3
"""Portao da T-084: `loop.sh` com limite de tempo por tentativa (`--tempo-maximo <segundos>`).

Escrito pelo agente gestor em 2026-10-21, antes de delegar, no molde de `portao_t058.py`.
Com o `loop.sh` de hoje ele falha pelo motivo certo: a flag nao existe (exit 1, "Argumento
desconhecido") e o agente que dorme segura a rodada.
1. `--help` documenta `--tempo-maximo`.
2. Agente que dorme sem mexer em nada, com `--tempo-maximo 2`: a rodada termina em poucos segundos
   com exit 4 (agente falhou e nao alterou arquivo), e a saida cita o limite de tempo.
3. Agente que escreve um arquivo e depois dorme, com `--tempo-maximo 2` e portao verde: exit 0 em
   poucos segundos, tarefa fechada com evidencia; o caminho e o de "agente saiu diferente de zero
   mas alterou arquivos", entao a saida avisa e o portao decide. Nenhum processo filho do agente
   pode continuar segurando stdout: o teste mede o tempo total ate o loop devolver o controle.
4. Sem a flag, agente normal continua fechando a tarefa (padrao generoso, sem regressao).
5. Valor invalido (`abc`, `0`) sai 1 antes de chamar o agente.
6. `references/loop.md` documenta a flag (uso e menciona SIGTERM); `test_loop.py` tem caso com a
   flag; bloco loop (partial) sem mudanca de conteudo: e mecanica do script, nao regra do agente.
7. `test_loop.py` passa com pelo menos 78 verificacoes (hoje 77). 8. versao coerente em 2.13.0
   ou acima (bump da rodada, feito pelo gestor). 9. verificador exit 0.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, SKILL, check, ler, resumo, verify_ok, versao_coerente  # noqa: E402

LOOP = SKILL / "scripts" / "loop.sh"
NOVA = "2.13.0"
PISO_BATERIA = 78
SHA_LOOP_PARTIAL = "586e5ce0b016a119a18f28610f0e9cfe31aa7db54fd96fadb2fef6ee1c0e9312"
NUCLEO_DOCS = ("README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
               "CONSENSUS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md")
TASKS = """# TASKS

- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-01)`.

## Em Andamento

- T-019: Tarefa com portao declarado. (prioridade: alta) (verifica: bash portao.sh)

## Proximas Tarefas

- (Vazio.)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- 2026-08-10 T-001: Tarefa historica sem evidencia.
"""
AGENTE_DORME = "#!/usr/bin/env bash\nsleep 60\n"
AGENTE_TRABALHA_E_DORME = "#!/usr/bin/env bash\necho feito > \"$PWD/rascunho.txt\"\nsleep 60\n"
AGENTE_NORMAL = "#!/usr/bin/env bash\nexit 0\n"
TETO = 25  # segundos: 2 de limite mais folga larga; 60 de sono nunca cabe aqui


def montar(tmp, portao_corpo="exit 0\n"):
    root = Path(tmp) / "projeto"
    (root / "docs" / "archive").mkdir(parents=True)
    for nome in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / nome, root / nome)
    for nome in NUCLEO_DOCS:
        shutil.copy(ASSETS / "docs" / nome, root / "docs" / nome)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", root / "docs" / "archive" / "README.md")
    (root / "docs" / "TASKS.md").write_text(TASKS, encoding="utf-8")
    (root / "portao.sh").write_text(portao_corpo, encoding="utf-8")
    return root


def agente(tmp, corpo):
    caminho = Path(tmp) / "agente-falso"
    caminho.write_text(corpo, encoding="utf-8")
    caminho.chmod(0o755)
    return caminho


def rodar(root, ag, *extra, timeout=TETO + 40):
    env = dict(os.environ, PATH=f"{ag.parent}{os.pathsep}{os.environ['PATH']}", PYTHONDONTWRITEBYTECODE="1")
    inicio = time.monotonic()
    try:
        p = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(root), "--agente", ag.name, *extra],
                           capture_output=True, text=True, errors="replace", env=env, timeout=timeout)
        return p.returncode, p.stdout + p.stderr, time.monotonic() - inicio
    except subprocess.TimeoutExpired as e:
        saida = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return None, saida + f"\n[portao] loop.sh estourou {timeout}s", time.monotonic() - inicio


def concluida(root):
    texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
    return "T-019" in texto.split("## Concluidas")[1]


def main():
    ajuda = subprocess.run(["bash", str(LOOP), "--help"], capture_output=True, text=True, errors="replace").stdout
    check("--tempo-maximo" in ajuda, "1. loop.sh --help documenta --tempo-maximo")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        codigo, saida, dur = rodar(root, agente(tmp, AGENTE_DORME), "--tempo-maximo", "2")
        check(codigo == 4 and dur < TETO and not concluida(root),
              "2. agente que dorme sem mexer em nada: exit 4 em poucos segundos, tarefa aberta",
              f"exit {codigo} em {dur:.1f}s")
        check(codigo == 4 and re.search(r"tempo m[aá]ximo|limite de tempo|SIGTERM", saida, re.I) is not None, "2b. a saida cita o limite de tempo (ou o SIGTERM) e nao e erro de uso", saida.strip().splitlines()[-1][:120] if saida.strip() else "vazia")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        codigo, saida, dur = rodar(root, agente(tmp, AGENTE_TRABALHA_E_DORME), "--tempo-maximo", "2")
        check(codigo == 0 and dur < TETO and concluida(root),
              "3. agente que trabalha e depois dorme: encerrado no limite, portao verde fecha a tarefa em poucos segundos",
              f"exit {codigo} em {dur:.1f}s; concluida={concluida(root)}")
        check("[AVISO]" in saida and "portao decide" in saida, "3b. a saida avisa que o agente saiu diferente de zero e deixa o portao decidir")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        codigo, saida, dur = rodar(root, agente(tmp, AGENTE_NORMAL))
        check(codigo == 0 and concluida(root), "4. sem a flag, agente normal segue fechando a tarefa", f"exit {codigo}")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        exits = []
        for valor in ("abc", "0"):
            codigo, saida, _ = rodar(root, agente(tmp, AGENTE_NORMAL), "--tempo-maximo", valor)
            exits.append(codigo)
        check(exits == [1, 1] and not concluida(root), "5. --tempo-maximo abc e 0 saem 1 sem chamar o agente", f"exits {exits}")

    doc = ler(SKILL / "references" / "loop.md")
    check("--tempo-maximo" in doc and "SIGTERM" in doc, "6a. references/loop.md documenta --tempo-maximo e o SIGTERM")
    check("--tempo-maximo" in ler(SKILL / "evals" / "test_loop.py"), "6b. test_loop.py tem caso com --tempo-maximo")
    partial = ler(ASSETS / "partials" / "AGENTS-loop-block.md")
    sha = hashlib.sha256(re.sub(r":start\s+v\d+\.\d+\.\d+", ":start vX", partial).encode("utf-8")).hexdigest()
    check(sha == SHA_LOOP_PARTIAL, "6c. bloco loop (partial) sem mudanca de conteudo: timeout e mecanica do script, nao regra do agente")

    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(SKILL / "evals" / "test_loop.py")], capture_output=True, text=True, errors="replace", env=env)
    m = re.search(r"(\d+)/(\d+) verificacoes passaram", p.stdout)
    n = int(m.group(2)) if m else 0
    check(p.returncode == 0 and n >= PISO_BATERIA, f"7. test_loop.py exit 0 com pelo menos {PISO_BATERIA} verificacoes", f"exit {p.returncode}; {n} verificacoes")

    versao, ok, _, det = versao_coerente(NOVA)
    check(ok, f"8. versao {NOVA} ou acima, coerente", det)
    ok, res = verify_ok()
    check(ok, "9. verify_repository.py exit 0", res)
    return resumo("T-084")


if __name__ == "__main__":
    sys.exit(main())
