#!/usr/bin/env python3
"""Testa o modulo de loop em projetos descartaveis, com agente falso.

Uso:
    python3 docs/skills/ai-project-structure/evals/test_loop.py [--verbose]

Cobre os criterios de comportamento da spec 0004:

- `loop_task.py`: elegibilidade, fecho com evidencia de comando, bloqueio com
  pergunta, recusa de portao vermelho, tarefa dentro de cerca ``` ignorada e
  historico anterior intocado;
- `loop.sh`: os quatro caminhos (tarefa sem portao, portao verde, portao
  vermelho ate esgotar as tentativas, falta de contexto), incluindo a
  conferencia de que a saida da falha realimenta a tentativa seguinte.

Nenhuma chamada de modelo: o agente e um shell script que registra o prompt
recebido. Roda em segundos e nao custa nada, entao pode rodar sempre.

Nao e distribuido pelo `install.sh`: vive em `evals/`, so na fonte canonica.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 se tudo passar.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ASSETS = SKILL / "assets"
HELPER = SKILL / "scripts" / "loop_task.py"
LOOP = SKILL / "scripts" / "loop.sh"
VALIDADOR = SKILL / "scripts" / "validate_structure.py"

NUCLEO_DOCS = ("README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
               "CONSENSUS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md")

TASKS = """# TASKS

Formato de tarefa:

- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-01)`.

Modelo de linha:

```md
- T-999: Isto esta dentro de cerca e nao deve ser encontrado. (verifica: nao-rode-isto)
```

## Em Andamento

- T-019: Tarefa com portao declarado. (prioridade: alta) (verifica: {portao})

## Proximas Tarefas

- T-020: Tarefa sem portao declarado. (prioridade: media)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- 2026-08-10 T-001: Tarefa historica sem evidencia.

## Ideias

- (Vazio.)
"""

AGENTE_NORMAL = """#!/usr/bin/env bash
printf '%s\\n=====\\n' "$1" >> "$LOG_PROMPT"
"""

AGENTE_QUEBRADO = """#!/usr/bin/env bash
# agente mal configurado: falha e nao mexe em nada, como uma CLI que recusa
# rodar sem a flag certa
printf '%s\\n=====\\n' "$1" >> "$LOG_PROMPT"
echo "erro: flag obrigatoria ausente" >&2
exit 1
"""

AGENTE_QUEBRADO_MAS_TRABALHOU = """#!/usr/bin/env bash
# falha, mas deixou trabalho feito: o portao e quem decide
printf '%s\\n=====\\n' "$1" >> "$LOG_PROMPT"
echo "trabalho parcial" > "$PWD/rascunho.txt"
exit 1
"""

AGENTE_SEM_CONTEXTO = """#!/usr/bin/env bash
printf '%s\\n=====\\n' "$1" >> "$LOG_PROMPT"
echo "Qual banco de dados o projeto usa? Nao ha nada em STACK.md nem em ARCHITECTURE.md." \\
  > "$PWD/.loop-pergunta"
"""


class Resultado:
    def __init__(self, verbose=False):
        self.falhas = 0
        self.total = 0
        self.verbose = verbose

    def check(self, ok, titulo, detalhe=""):
        self.total += 1
        if not ok:
            self.falhas += 1
        if not ok or self.verbose:
            sufixo = f": {detalhe}" if detalhe else ""
            print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}{sufixo}")


def montar(tmp, portao_corpo="exit 0\n", portao_cmd="bash portao.sh"):
    root = Path(tmp) / "projeto"
    (root / "docs" / "archive").mkdir(parents=True)
    for nome in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / nome, root / nome)
    for nome in NUCLEO_DOCS:
        shutil.copy(ASSETS / "docs" / nome, root / "docs" / nome)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", root / "docs" / "archive" / "README.md")
    (root / "docs" / "TASKS.md").write_text(TASKS.format(portao=portao_cmd), encoding="utf-8")
    (root / "portao.sh").write_text(portao_corpo, encoding="utf-8")
    return root


def agente_falso(tmp, corpo):
    caminho = Path(tmp) / "agente-falso"
    caminho.write_text(corpo, encoding="utf-8")
    caminho.chmod(0o755)
    return caminho


def rodar_helper(*args):
    p = subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def rodar_loop(root, agente, log, tarefa="T-019", extra=()):
    env = dict(os.environ, LOG_PROMPT=str(log),
               PATH=f"{agente.parent}{os.pathsep}{os.environ['PATH']}")
    p = subprocess.run(
        ["bash", str(LOOP), "--tarefa", tarefa, "--projeto", str(root),
         "--agente", agente.name, *extra],
        capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def validar(root):
    p = subprocess.run([sys.executable, str(VALIDADOR), str(root), "--strict"],
                       capture_output=True, text=True)
    return p.returncode


def prompts(log):
    if not log.exists():
        return []
    return [p for p in log.read_text(encoding="utf-8").split("=====") if p.strip()]


def testar_helper(res):
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        code, out = rodar_helper("check", str(root), "T-019")
        res.check(code == 0 and out == "bash portao.sh", "check em tarefa elegivel", out)
        code, out = rodar_helper("check", str(root), "T-020")
        res.check(code == 1 and "nao declarou" in out, "check recusa tarefa sem (verifica:)", out[:70])
        code, out = rodar_helper("check", str(root), "T-001")
        res.check(code == 1 and "concluidas" in out, "check recusa tarefa concluida", out[:70])
        code, out = rodar_helper("check", str(root), "T-777")
        res.check(code == 1 and "nao encontrada" in out, "check recusa tarefa inexistente", out[:70])
        code, out = rodar_helper("check", str(root), "T-999")
        res.check(code == 1 and "nao encontrada" in out,
                  "tarefa dentro de cerca nao e encontrada", out[:70])

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        saida = Path(tmp) / "saida.txt"
        saida.write_text("tudo-certo\n", encoding="utf-8")
        code, out = rodar_helper("fechar", str(root), "T-019", "--saida", str(saida), "--codigo", "1")
        res.check(code == 1 and "recusa escrever evidencia" in out,
                  "fechar recusa portao vermelho", out[:70])
        code, out = rodar_helper("fechar", str(root), "T-019", "--saida", str(saida),
                                 "--codigo", "0", "--agente", "codex exec -m gpt-5.6-terra")
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        concluidas = texto.split("## Concluidas")[1]
        res.check("agente=codex exec -m gpt-5.6-terra" in concluidas,
                  "evidencia registra o agente que fez o trabalho")
        res.check(code == 0, "fechar aceita portao verde", out)
        res.check("T-019" in concluidas, "tarefa foi para Concluidas")
        res.check("Evidencia: tipo=comando" in concluidas, "evidencia com tipo=comando")
        res.check("procedimento=bash portao.sh" in concluidas, "procedimento traz o comando declarado")
        res.check("resultado=exit 0; tudo-certo" in concluidas, "resultado traz exit code e saida")
        em_andamento = texto.split("## Em Andamento")[1].split("## Proximas")[0]
        res.check("T-019" not in em_andamento, "tarefa saiu de Em Andamento")
        res.check("2026-08-10 T-001: Tarefa historica sem evidencia." in texto,
                  "historico intocado, sem evidencia inventada")
        res.check("revisao-manual" not in texto and "conferencia" not in texto,
                  "nenhuma evidencia de tipo nao comprovado")
        res.check(validar(root) == 0, "validador --strict exit 0 depois de fechar")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        pergunta = Path(tmp) / "pergunta.txt"
        pergunta.write_text("Qual banco de dados o projeto usa?\nNao consegui inferir.\n",
                            encoding="utf-8")
        code, out = rodar_helper("bloquear", str(root), "T-019", "--pergunta", str(pergunta))
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        aguardando = texto.split("## Aguardando Usuario")[1].split("## Concluidas")[0]
        res.check(code == 0, "bloquear move a tarefa", out)
        res.check("T-019" in aguardando, "tarefa foi para Aguardando Usuario")
        res.check("**Pergunta:** Qual banco de dados" in aguardando, "pergunta em uma linha")
        res.check("**Resposta:** (A preencher.)" in aguardando, "campo de resposta em aberto")
        res.check("(bloqueada: " in aguardando, "marcador de bloqueio com data")
        res.check("(Vazio.)" not in aguardando, "placeholder da secao substituido")
        res.check("Evidencia:" not in aguardando, "nenhuma evidencia no caminho de bloqueio")
        res.check(validar(root) == 0, "validador --strict exit 0 depois de bloquear")


def testar_loop(res):
    # A: tarefa sem (verifica:) e recusada antes de chamar o agente
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        agente = agente_falso(tmp, AGENTE_NORMAL)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log, tarefa="T-020")
        res.check(code == 1, "A: tarefa sem portao sai 1", f"exit {code}")
        res.check(not prompts(log), "A: agente nunca foi chamado")

    # B: portao verde na primeira tentativa
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp, "echo portao-verde\nexit 0\n")
        agente = agente_falso(tmp, AGENTE_NORMAL)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log)
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        concluidas = texto.split("## Concluidas")[1]
        res.check(code == 0, "B: portao verde sai 0", f"exit {code}")
        res.check("T-019" in concluidas, "B: tarefa foi para Concluidas")
        res.check("resultado=exit 0; portao-verde" in concluidas, "B: evidencia com a saida real")
        res.check(f"agente={agente.name}" in concluidas, "B: loop.sh repassa o agente para a evidencia")
        res.check(len(prompts(log)) == 1, "B: agente chamado uma vez")
        res.check("2026-08-10 T-001" in texto, "B: historico intocado")
        res.check(validar(root) == 0, "B: validador --strict exit 0 depois da rodada")

    # C: portao vermelho ate esgotar
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp, "echo portao-vermelho-detalhe\nexit 1\n")
        agente = agente_falso(tmp, AGENTE_NORMAL)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log)
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        ps = prompts(log)
        em_andamento = texto.split("## Em Andamento")[1].split("## Proximas")[0]
        res.check(code == 2, "C: portao vermelho sai 2", f"exit {code}")
        res.check("T-019" in em_andamento, "C: tarefa continua em Em Andamento")
        res.check("Evidencia:" not in texto, "C: nenhuma evidencia escrita")
        res.check(len(ps) == 3, "C: agente chamado 3 vezes", f"{len(ps)} chamadas")
        res.check(len(ps) > 1 and "portao-vermelho-detalhe" in ps[1],
                  "C: saida da falha realimenta a tentativa 2")
        res.check(ps and "portao-vermelho-detalhe" not in ps[0],
                  "C: tentativa 1 nao recebe realimentacao")
        res.check(validar(root) == 0, "C: validador --strict exit 0 depois da rodada")

    # C2: --tentativas muda o limite
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp, "exit 1\n")
        agente = agente_falso(tmp, AGENTE_NORMAL)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log, extra=("--tentativas", "5"))
        res.check(code == 2 and len(prompts(log)) == 5, "C2: --tentativas 5 chama 5 vezes",
                  f"exit {code}, {len(prompts(log))} chamadas")

    # E: agente falhou e nao mexeu em nada; parar em vez de queimar tentativa
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        agente = agente_falso(tmp, AGENTE_QUEBRADO)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log)
        res.check(code == 4, "E: agente quebrado sai 4", f"exit {code}")
        res.check(len(prompts(log)) == 1, "E: parou na primeira tentativa",
                  f"{len(prompts(log))} chamadas")
        res.check("nao alterou nenhum arquivo" in out, "E: diz que o agente nao mexeu em nada")
        res.check("Evidencia:" not in (root / "docs" / "TASKS.md").read_text(encoding="utf-8"),
                  "E: nenhuma evidencia escrita")

    # F: agente falhou mas trabalhou; o portao decide, o loop nao aborta
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp, "exit 1\n")
        agente = agente_falso(tmp, AGENTE_QUEBRADO_MAS_TRABALHOU)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log)
        res.check(code == 2, "F: agente que falhou mas mexeu segue ate o portao", f"exit {code}")
        res.check(len(prompts(log)) == 3, "F: as 3 tentativas foram usadas",
                  f"{len(prompts(log))} chamadas")

    # D: agente sinaliza falta de contexto
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        agente = agente_falso(tmp, AGENTE_SEM_CONTEXTO)
        log = Path(tmp) / "prompts.txt"
        code, out = rodar_loop(root, agente, log)
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        aguardando = texto.split("## Aguardando Usuario")[1].split("## Concluidas")[0]
        res.check(code == 3, "D: falta de contexto sai 3", f"exit {code}")
        res.check("T-019" in aguardando, "D: tarefa foi para Aguardando Usuario")
        res.check("**Pergunta:** Qual banco de dados" in aguardando, "D: pergunta registrada")
        res.check("**Resposta:** (A preencher.)" in aguardando, "D: campo de resposta em aberto")
        res.check("Evidencia:" not in texto, "D: nenhuma evidencia escrita")
        res.check(not (root / ".loop-pergunta").exists(), "D: arquivo de sinal removido")
        res.check(len(prompts(log)) == 1, "D: parou na primeira tentativa")
        res.check(validar(root) == 0, "D: validador --strict exit 0 depois da rodada")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Testa o modulo de loop com agente falso.")
    parser.add_argument("--verbose", action="store_true", help="Mostra tambem o que passou.")
    args = parser.parse_args(argv)

    res = Resultado(args.verbose)
    testar_helper(res)
    testar_loop(res)
    print(f"Modulo de loop: {res.total - res.falhas}/{res.total} verificacoes passaram.")
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
