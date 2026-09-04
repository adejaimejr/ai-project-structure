#!/usr/bin/env python3
"""Portao da T-060: os consertos sem decisao do modulo de loop (REVAL-3 e REVAL-4).

Cobra comportamento com agente falso, um caso por item da tarefa. Nenhum caso
dita como consertar; cada um diz o que tem de acontecer. No fim, bump de
versao coerente e o verificador geral em exit 0 (a tarefa nao toca o bloco
core, entao a paridade com a raiz se mantem).

1. Agente que troca o comando do marcador verifica na propria linha: a
   evidencia nunca registra o comando trocado como `procedimento=`.
2. `fechar` e `bloquear` preservam as sub-linhas preexistentes da tarefa.
3. Saida do portao com bytes fora de UTF-8 e portao verde: tarefa fecha, exit 0.
4. Saida do portao de 1,2MB e portao vermelho: tres tentativas e exit 2, nunca exit 4.
5. `.loop-pergunta` vazio: exit 3, tarefa em Aguardando Usuario, arquivo removido.
6. Modo do `TASKS.md` (0664) preservado depois de `fechar`.
7. `--seco --agente X` nao grava `agente=` na evidencia.
8. `loop_task.py check` nao grava `scripts/__pycache__` na skill.
9. O agente recebe stdin fechado: conteudo no stdin do `loop.sh` nao chega a ele.
10. O prompt diz que propagar bloco gerenciado para o `AGENTS.md` da raiz e do agente de chat.
11. A tabela de exit codes de `references/loop.md` tem o 4.
12. Versao acima de 2.8.0 e coerente; `verify_repository.py` exit 0.
"""

import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ASSETS = SKILL / "assets"
LOOP = SKILL / "scripts" / "loop.sh"
HELPER = SKILL / "scripts" / "loop_task.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
VERSAO_ANTES = "2.8.0"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


TASKS = """# TASKS

- `(convencoes-2-2-0-desde: 2026-09-01)`

## Em Andamento

- T-019: Tarefa alvo. (verifica: {portao})
  - Cuidado: nao alterar a variavel X
  - Contexto: ver spec 0001

## Proximas Tarefas

- (Vazio.)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- (Vazio.)
"""


def montar(tmp, nome, portao="bash portao.sh", portao_corpo="exit 0\n", agente_corpo="true\n"):
    r = Path(tmp) / nome
    (r / "docs" / "archive").mkdir(parents=True)
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / f, r / f)
    for f in NUCLEO:
        shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
    (r / "docs" / "TASKS.md").write_text(TASKS.format(portao=portao), encoding="utf-8")
    (r / "portao.sh").write_text(portao_corpo, encoding="utf-8")
    ag = Path(tmp) / f"{nome}-agente"
    ag.write_text("#!/usr/bin/env bash\n" + agente_corpo, encoding="utf-8")
    ag.chmod(0o755)
    return r, ag


def rodar(r, ag, extra=(), stdin_texto=None, env_extra=None):
    env = dict(os.environ, PATH=f"{ag.parent}{os.pathsep}{os.environ['PATH']}", LOG_PROMPT=str(r / "prompt.log"))
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(r), "--agente", ag.name, *extra],
                       capture_output=True, text=True, errors="replace", env=env,
                       input=stdin_texto)
    return p.returncode, p.stdout + p.stderr


def tasks(r):
    return (r / "docs" / "TASKS.md").read_text(encoding="utf-8", errors="replace")


def secao(r, nome):
    t = tasks(r)
    return t.split("## " + nome)[1].split("\n## ")[0] if "## " + nome in t else ""


def main():
    with tempfile.TemporaryDirectory() as tmp:
        # 1. agente troca o verifica na propria linha
        r, ag = montar(tmp, "c1", agente_corpo='sed -i "" "s/(verifica: bash portao.sh)/(verifica: true)/" docs/TASKS.md\n',
                       portao_corpo="echo suite-real; exit 0\n")
        code, out = rodar(r, ag)
        conc = secao(r, "Concluidas")
        check("procedimento=true" not in conc, "1. evidencia nunca registra o comando trocado pelo agente",
              f"exit {code}; " + conc.strip().replace("\n", " ")[:160])

        # 2. sub-linhas preservadas em fechar e bloquear
        r, ag = montar(tmp, "c2")
        code, out = rodar(r, ag)
        conc = secao(r, "Concluidas")
        check(code == 0 and "Cuidado: nao alterar" in conc and "Contexto: ver spec" in conc,
              "2a. fechar preserva as sub-linhas preexistentes", conc.strip().replace("\n", " ")[:160])
        r, ag = montar(tmp, "c2b", agente_corpo='echo "Qual banco?" > "$PWD/.loop-pergunta"\n')
        code, out = rodar(r, ag)
        ag_sec = secao(r, "Aguardando Usuario")
        check(code == 3 and "Cuidado: nao alterar" in ag_sec and "**Pergunta:**" in ag_sec,
              "2b. bloquear preserva as sub-linhas preexistentes", ag_sec.strip().replace("\n", " ")[:160])

        # 3. saida nao UTF-8 com portao verde
        r, ag = montar(tmp, "c3", portao_corpo="printf 'ok \\xff\\xfe fim\\n'; exit 0\n")
        code, out = rodar(r, ag)
        check(code == 0 and "T-019" in secao(r, "Concluidas"), "3. saida fora de UTF-8 nao impede o fecho",
              f"exit {code}; " + out[-160:].replace("\n", " "))

        # 4. saida enorme com portao vermelho
        r, ag = montar(tmp, "c4", agente_corpo='echo x >> "$PWD/trabalho.txt"; printf "%s\\n=====\\n" "$1" >> "$LOG_PROMPT"\n',
                       portao_corpo='head -c 1200000 /dev/zero | tr "\\0" x; echo; exit 1\n')
        code, out = rodar(r, ag)
        chamadas = (r / "prompt.log").read_text(errors="replace").count("=====") if (r / "prompt.log").exists() else 0
        check(code == 2 and chamadas == 3, "4. saida de 1,2MB do portao nao vira exit 4; tres tentativas e exit 2",
              f"exit {code}, {chamadas} chamadas")

        # 5. pergunta vazia
        r, ag = montar(tmp, "c5", agente_corpo=': > "$PWD/.loop-pergunta"\n')
        code, out = rodar(r, ag)
        check(code == 3 and "T-019" in secao(r, "Aguardando Usuario") and not (r / ".loop-pergunta").exists(),
              "5. .loop-pergunta vazio: exit 3, tarefa bloqueada, arquivo removido", f"exit {code}")

        # 6. modo do arquivo
        r, ag = montar(tmp, "c6")
        os.chmod(r / "docs" / "TASKS.md", 0o664)
        code, out = rodar(r, ag)
        modo = stat.S_IMODE((r / "docs" / "TASKS.md").stat().st_mode)
        check(code == 0 and modo == 0o664, "6. modo 0664 do TASKS.md preservado depois de fechar", oct(modo))

        # 7. --seco --agente nao grava agente=
        r, ag = montar(tmp, "c7")
        code, out = rodar(r, ag, extra=("--seco",))
        check(code == 0 and "agente=" not in secao(r, "Concluidas"), "7. --seco nao grava agente= na evidencia", f"exit {code}")

        # 8. check nao grava __pycache__ na skill
        pc = SKILL / "scripts" / "__pycache__"
        if pc.exists():
            shutil.rmtree(pc)
        r, ag = montar(tmp, "c8")
        env = dict(os.environ)
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        subprocess.run([sys.executable, str(HELPER), "check", str(r), "T-019"], capture_output=True, text=True, env=env)
        check(not pc.exists(), "8. loop_task.py check nao grava scripts/__pycache__ na skill")
        if pc.exists():
            shutil.rmtree(pc)

        # 9. stdin fechado para o agente
        r, ag = montar(tmp, "c9", agente_corpo='x="$(cat)"; echo "stdin:$x" > "$PWD/stdin.txt"\n')
        code, out = rodar(r, ag, stdin_texto="segredo-do-stdin\n")
        lido = (r / "stdin.txt").read_text(errors="replace") if (r / "stdin.txt").exists() else "(agente nao escreveu)"
        check("segredo-do-stdin" not in lido, "9. agente recebe stdin fechado", lido.strip()[:80])

        # 10. prompt diz quem propaga bloco gerenciado
        r, ag = montar(tmp, "c10", agente_corpo='printf "%s\\n=====\\n" "$1" >> "$LOG_PROMPT"\n')
        rodar(r, ag)
        prompt = norm((r / "prompt.log").read_text(errors="replace")) if (r / "prompt.log").exists() else ""
        check("agents.md" in prompt and "propag" in prompt and "agente de chat" in prompt,
              "10. prompt diz que propagar bloco gerenciado ao AGENTS.md e do agente de chat")

    # 11. tabela de exit codes com o 4
    loop_md = (SKILL / "references" / "loop.md").read_text(encoding="utf-8")
    m = re.search(r"\| Codigo \| Significado \|.*?(?=\n\n)", loop_md, re.S)
    check(m is not None and re.search(r"^\| 4 \|", m.group(0), re.M) is not None, "11. tabela de exit codes de loop.md tem o 4")

    # 12. versao e verificador
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm = re.search(r'^version:\s*"?([\d.]+)"?', skill, re.M)
    versao = fm.group(1) if fm else "0.0.0"
    acima = tuple(int(x) for x in versao.split(".")) > tuple(int(x) for x in VERSAO_ANTES.split("."))
    check(acima, f"12a. SKILL.md com versao acima de {VERSAO_ANTES}", versao)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True, env=env)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "12b. verify_repository.py exit 0", resumo)

    total = 14
    print(f"\nPortao T-060: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
