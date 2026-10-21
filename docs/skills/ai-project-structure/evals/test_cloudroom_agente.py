#!/usr/bin/env python3
"""Testa o adaptador Cloudroom (`scripts/cloudroom_agente.py`) contra um `room-cli` falso.

Uso:
    python3 docs/skills/ai-project-structure/evals/test_cloudroom_agente.py [--verbose]

Cobre os criterios de comportamento da spec 0008:

- o adaptador sozinho: validacao de uso, spawn (flags, prompt por arquivo, titulo), cada
  cenario do `room-cli` falso (`ok`, `longo`, `falha`, `lento`, `pergunta`), parada por sinal,
  `--arquivar`, prompt grande e as falhas da CLI (spawn recusado, consulta quebrada, filho
  que termina sem resposta);
- o adaptador como `--agente` do `loop.sh`: filho que escreve no projeto fecha a tarefa,
  portao vermelho realimenta a tentativa seguinte, filho que falha vira exit 4 e
  `--tempo-maximo` para o filho com `thread stop`.

Nenhuma chamada de modelo e nenhuma thread real: o `room-cli` e o falso de
`evals/mock_room_cli.py`, e o PATH de todo teste tira qualquer outro `room-cli`
(o real abre thread paga). O cenario "sem room-cli" usa um PATH sem nenhum.

Nao e distribuido pelo `install.sh`: vive em `evals/`, so na fonte canonica.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 se tudo passar.
"""

import argparse
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

EVALS = Path(__file__).resolve().parent
sys.path.insert(0, str(EVALS))
import mock_room_cli as mock  # noqa: E402

SKILL = EVALS.parent
ASSETS = SKILL / "assets"
WRAPPER = SKILL / "scripts" / "cloudroom_agente.py"
LOOP = SKILL / "scripts" / "loop.sh"
VALIDADOR = SKILL / "scripts" / "validate_structure.py"

NUCLEO_DOCS = ("README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
               "CONSENSUS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md")
# O Linux limita cada argumento a 131072 bytes: o prompt de teste fica bem abaixo disso.
PROMPT = ("Voce esta trabalhando no projeto.\nSua tarefa e a T-019, descrita em docs/TASKS.md.\n"
          "-- linha com dois hifens --\n--provider dentro do texto nao e flag\n"
          "acentuacao: coracao, acao, ç ã é\n" + ("x" * 60000) + "\nfim do prompt\n")
BASE = ("--provider", "claude-code", "--intervalo", "0.2")

TASKS = """# TASKS

- Data de adocao das convencoes: `(convencoes-2-2-0-desde: 2026-09-01)`.

## Em Andamento

- T-019: Tarefa com portao declarado. (prioridade: alta) (verifica: {portao})

## Proximas Tarefas

- (Vazio.)

## Aguardando Usuario

- (Vazio.)

## Concluidas

- 2026-08-10 T-001: Tarefa historica sem evidencia.
"""

# `room-cli` de bolso para as falhas que o falso nao imita. Modo em $STUB_MODO.
STUB = """#!/usr/bin/env bash
echo "$2" >> "$STUB_LOG"
case "$2:$STUB_MODO" in
  spawn:recusa)     echo "refused: no quota" >&2; exit 1 ;;
  spawn:sem-id)     echo '{"note": "sem id aqui"}'; exit 0 ;;
  spawn:lixo)       echo 'isto nao e json'; exit 0 ;;
  spawn:*)          echo '{"id": "cr_child_stub1"}'; exit 0 ;;
  output:quebra)    echo "connection reset" >&2; exit 1 ;;
  output:sem-reply) echo '{"busy": false, "state": "idle", "error": null}'; exit 0 ;;
  output:parado)    echo '{"busy": false, "state": "stopped", "error": null}'; exit 0 ;;
  output:alterna)   n=$(grep -c output "$STUB_LOG"); if [ $((n % 2)) -eq 1 ]; then echo "x" >&2; exit 1; fi
                    if [ "$n" -ge 8 ]; then echo '{"busy": false, "state": "idle", "reply": "FIM-ALTERNADO"}'; else echo '{"busy": true, "state": "running"}'; fi
                    exit 0 ;;
esac
exit 0
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


def path_seguro(extra=()):
    """PATH sem nenhum diretorio que tenha um `room-cli` (o real abre thread paga), com `extra` na frente."""
    limpos = [d for d in os.environ.get("PATH", "").split(os.pathsep)
              if d and not (Path(d) / "room-cli").exists() and not (Path(d) / "room-cli.exe").exists()]
    return os.pathsep.join([str(e) for e in extra] + limpos)


def ambiente(tmp, cenario):
    """Instala o falso e devolve (estado_dir, env) com o PATH saneado."""
    bin_dir, estado, env = mock.instalar(tmp, cenario)
    env["PATH"] = path_seguro([bin_dir])
    return estado, env


def ambiente_stub(tmp, modo):
    bin_dir = Path(tmp) / "bin-stub"
    bin_dir.mkdir()
    exe = bin_dir / "room-cli"
    exe.write_text(STUB, encoding="utf-8")
    exe.chmod(0o755)
    log = Path(tmp) / "stub.log"
    env = dict(os.environ, PATH=path_seguro([bin_dir]), STUB_MODO=modo, STUB_LOG=str(log),
               PYTHONDONTWRITEBYTECODE="1")
    return log, env


def chamadas_stub(log):
    return log.read_text(encoding="utf-8").split() if log.exists() else []


def rodar(env, *args, prompt=PROMPT, timeout=60):
    try:
        p = subprocess.run([sys.executable, str(WRAPPER), *args, prompt], capture_output=True, text=True,
                           errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return None, "", f"adaptador estourou {timeout}s"


def montar(tmp, portao="test -f trabalho-do-filho.txt"):
    root = Path(tmp) / "projeto"
    (root / "docs" / "archive").mkdir(parents=True)
    for nome in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / nome, root / nome)
    for nome in NUCLEO_DOCS:
        shutil.copy(ASSETS / "docs" / nome, root / "docs" / nome)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", root / "docs" / "archive" / "README.md")
    (root / "portao.sh").write_text(portao + "\n", encoding="utf-8")
    (root / "docs" / "TASKS.md").write_text(TASKS.format(portao="bash portao.sh"), encoding="utf-8")
    return root


def rodar_loop(root, env, *extra, timeout=90):
    agente = f"{sys.executable} {WRAPPER} --provider claude-code --model claude-sonnet-5-5 --intervalo 0.2"
    inicio = time.monotonic()
    try:
        p = subprocess.run(["bash", str(LOOP), "--tarefa", "T-019", "--projeto", str(root), "--agente", agente, *extra],
                           capture_output=True, text=True, errors="replace", env=env, stdin=subprocess.DEVNULL,
                           timeout=timeout)
        return p.returncode, p.stdout + p.stderr, time.monotonic() - inicio
    except subprocess.TimeoutExpired:
        return None, f"loop.sh estourou {timeout}s", time.monotonic() - inicio


def concluidas(root):
    texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
    return texto.split("## Concluidas")[1] if "## Concluidas" in texto else ""


def testar_uso(res):
    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        res.check(shutil.which("room-cli", path=env["PATH"]) == str(Path(tmp) / "bin" / "room-cli"),
                  "A0: o room-cli que o PATH do teste resolve e o falso, nunca o real")
        res.check(bool(shutil.which("bash", path=env["PATH"])) and bool(shutil.which("python3", path=env["PATH"])),
                  "A0: o PATH saneado ainda acha bash e python3")
        codigo, out, err = rodar(env, "--help", prompt="ignorado")
        ajuda = out + err
        res.check(codigo == 0 and all(t in ajuda for t in ("--titulo", "--arquivar", "--intervalo", "room-cli thread spawn", "143")),
                  "A1: --help sai 0 e documenta as opcoes e o exit 143", f"exit {codigo}")
        res.check(not mock.chamadas(estado), "A1: --help nao chama o room-cli")

        res.check(subprocess.run([sys.executable, str(WRAPPER)], capture_output=True, text=True, env=env,
                                 stdin=subprocess.DEVNULL).returncode == 1,
                  "A2: sem argumento nenhum (sem prompt): exit 1")
        c1 = rodar(env, "--provider", "claude-code", prompt="   \n")[0]
        c2 = rodar(env, prompt="algo")[0]
        c3 = rodar(env, "--provider", "claude-code", "--nao-existe", "x")[0]
        c4 = [rodar(env, "--provider", "claude-code", "--intervalo", v)[0] for v in ("0", "-1", "abc")]
        res.check((c1, c2, c3) == (1, 1, 1) and c4 == [1, 1, 1],
                  "A2: prompt vazio, falta de --provider, opcao desconhecida e --intervalo invalido: exit 1",
                  f"{(c1, c2, c3)} {c4}")
        res.check(not mock.chamadas(estado), "A2: nenhuma dessas recusas chegou ao room-cli")

        c5 = [rodar(env, "--provider", "claude-code", flag, "x")[0] for flag in ("--top-level", "--prompt", "--prompt-file")]
        res.check(c5 == [1, 1, 1] and not mock.por_comando(estado, "spawn"),
                  "A3: --top-level, --prompt e --prompt-file vindos de fora: exit 1 sem spawn", f"exits {c5}")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        vazio = Path(tmp) / "path-vazio"
        vazio.mkdir()
        env["PATH"] = str(vazio)  # PATH vazio, nao "o PATH sem o falso": o real pode estar em /usr/local/bin
        codigo, out, err = rodar(env, *BASE)
        res.check(codigo == 1 and "room-cli" in err and not out.strip() and not mock.chamadas(estado),
                  "A4: sem room-cli no PATH: exit 1, mensagem cita room-cli, stdout vazio e nada chamado", f"exit {codigo}")


def testar_cenarios(res):
    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        env["MOCK_ROOM_RESPOSTA"] = "RESPOSTA-OK TOKEN-101\nsegunda linha"
        codigo, out, err = rodar(env, *BASE, "--model", "claude-sonnet-5-5")
        spawns = mock.por_comando(estado, "spawn")
        args = spawns[0]["args"] if spawns else []
        flags = [a for a in args if a.startswith("--")]
        res.check(codigo == 0 and out == "RESPOSTA-OK TOKEN-101\nsegunda linha\n",
                  "B1: cenario ok: exit 0 e stdout e a resposta do filho mais uma quebra de linha", f"exit {codigo}, {out[:60]!r}")
        res.check(len(spawns) == 1 and "--shared-sandbox" in args and "--prompt-file" in args and "--prompt" not in args
                  and "--top-level" not in args and len(flags) == len(set(flags)),
                  "B2: um spawn so, com --shared-sandbox e --prompt-file, nunca --prompt nem --top-level", f"flags {flags}")
        res.check("claude-code" in args and "claude-sonnet-5-5" in args
                  and args[args.index("--provider") + 1] == "claude-code" and args[args.index("--model") + 1] == "claude-sonnet-5-5",
                  "B2: --provider e --model chegam ao spawn com os valores dados")
        res.check(bool(spawns) and spawns[0]["prompt"] == PROMPT,
                  "B3: o arquivo do --prompt-file tem o prompt inteiro, byte a byte (quebras, acentos, `--` dentro)")
        arquivo = args[args.index("--prompt-file") + 1] if "--prompt-file" in args else ""
        res.check(bool(arquivo) and not Path(arquivo).exists(), "B3: o arquivo temporario do prompt some depois do spawn")
        outputs = mock.por_comando(estado, "output")
        res.check(len(outputs) >= 3 and outputs[-1].get("all") is True,
                  "B4: consulta o filho ate ele terminar e a leitura final usa --all", f"{len(outputs)} consultas")
        res.check("thread=cr_child_mock1" in err, "B5: stderr registra thread=<id> do filho", err.strip()[-100:])
        res.check(not mock.por_comando(estado, "stop") and not mock.por_comando(estado, "archive"),
                  "B6: caminho feliz nao para nem arquiva o filho (fica para conferir)")

        # prompt que comeca com `--` e e o ultimo argumento continua sendo o prompt
        codigo, out, err = rodar(env, *BASE, prompt="--top-level")
        spawns = mock.por_comando(estado, "spawn")
        res.check(codigo == 0 and len(spawns) == 2 and spawns[1]["prompt"] == "--top-level",
                  "B7: prompt que comeca com `--` e o ultimo argumento e tratado como prompt", f"exit {codigo}")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "pergunta")
        codigo, out, err = rodar(env, *BASE)
        res.check(codigo == 0 and mock.RESPOSTA_PERGUNTA in out,
                  "C1: filho que pergunta em vez de responder: exit 0 com a pergunta no stdout (quem decide e o portao)")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "longo")
        codigo, out, err = rodar(env, *BASE)
        res.check(codigo == 0 and "FIM-DA-RESPOSTA-LONGA" in out and "truncated" not in out and len(out) > 19000,
                  "C2: cenario longo: stdout traz a resposta inteira, sem aviso de corte", f"len {len(out)}")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "falha")
        codigo, out, err = rodar(env, *BASE)
        res.check(codigo == 2 and mock.ERRO_FALHA in err and not out.strip(),
                  "C3: cenario falha: exit 2, stderr cita o erro do filho, stdout vazio", f"exit {codigo}")

    for sinal, nome in ((signal.SIGTERM, "SIGTERM"), (signal.SIGINT, "SIGINT")):
        with tempfile.TemporaryDirectory() as tmp:
            estado, env = ambiente(tmp, "lento")
            p = subprocess.Popen([sys.executable, str(WRAPPER), *BASE, PROMPT], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, env=env, stdin=subprocess.DEVNULL)
            limite = time.monotonic() + 10
            while time.monotonic() < limite and not mock.por_comando(estado, "output"):
                time.sleep(0.1)
            p.send_signal(sinal)
            inicio = time.monotonic()
            try:
                _, err = p.communicate(timeout=8)
                codigo = p.returncode
            except subprocess.TimeoutExpired:
                p.kill()
                p.communicate()
                codigo, err = None, b""
            demora = time.monotonic() - inicio
            paradas = mock.por_comando(estado, "stop")
            res.check(codigo == 143 and len(paradas) == 1 and paradas[0]["id"] == "cr_child_mock1" and demora < 5,
                      f"D{1 if nome == 'SIGTERM' else 2}: filho lento + {nome}: thread stop do filho certo em ate 5 s e exit 143",
                      f"exit {codigo}, stops {len(paradas)}, {demora:.1f}s")


def testar_opcoes(res):
    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        rodar(env, *BASE, "--titulo", "titulo explicito")
        rodar(env, *BASE)
        rodar(env, *BASE, prompt="Primeira linha sem tarefa\nsegunda")
        rodar(env, *BASE, prompt=("L" * 200) + "\nresto")
        titulos = [s.get("title") or "" for s in mock.por_comando(estado, "spawn")]
        res.check(len(titulos) == 4 and titulos[0] == "titulo explicito" and titulos[1] == "loop T-019"
                  and titulos[2] == "Primeira linha sem tarefa" and titulos[3] == "L" * 80,
                  "E1: titulo: --titulo vence; sem ele `loop T-NNN`; senao a primeira linha, cortada em 80 caracteres",
                  f"{[t[:30] for t in titulos]}")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        rodar(env, *BASE, "--arquivar")
        ordem = [c["cmd"] for c in mock.chamadas(estado)]
        arquivou = "archive" in ordem and ordem.index("archive") > max(i for i, c in enumerate(ordem) if c == "output")
        rodar(env, *BASE)
        depois = [c["cmd"] for c in mock.chamadas(estado)]
        res.check(arquivou and depois.count("archive") == 1,
                  "E2: --arquivar arquiva depois da ultima leitura; a rodada sem a flag nao arquiva", f"ordem {ordem}")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "falha")
        rodar(env, *BASE, "--arquivar")
        res.check(not mock.por_comando(estado, "archive"), "E3: --arquivar nao arquiva filho que falhou (fica para conferir)")

    with tempfile.TemporaryDirectory() as tmp:
        estado, env = ambiente(tmp, "ok")
        grande = Path(tmp) / "prompt-grande.txt"
        grande.write_text("y" * (mock.LIMITE_PROMPT + 1), encoding="utf-8")
        # Argumento acima de 131072 bytes nao passa por exec no Linux: o prompt vai por arquivo e o
        # adaptador roda por runpy num subprocesso, com o argv montado la dentro.
        ponte = ("import runpy, sys\n"
                 "w, f = sys.argv[1], sys.argv[2]\n"
                 "sys.argv = [w, '--provider', 'claude-code', '--intervalo', '0.2', open(f, encoding='utf-8').read()]\n"
                 "runpy.run_path(w, run_name='__main__')\n")
        p = subprocess.run([sys.executable, "-c", ponte, str(WRAPPER), str(grande)], capture_output=True, text=True,
                           errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=60)
        res.check(p.returncode == 1 and "262144" in p.stderr and not mock.por_comando(estado, "output"),
                  "E4: prompt acima de 262144 bytes: a CLI recusa, o adaptador sai 1 com a mensagem e nao consulta nada",
                  f"exit {p.returncode}")


def testar_falhas_da_cli(res):
    casos = (
        ("recusa", 1, "quota", "spawn recusado pela CLI", ["spawn"]),
        ("sem-id", 1, "id", "spawn sem id no JSON", ["spawn"]),
        ("lixo", 1, "id", "spawn que nao devolve JSON", ["spawn"]),
        ("quebra", 2, "3 vezes", "consulta quebrada 3 vezes seguidas", ["spawn", "output", "output", "output"]),
        ("sem-reply", 2, "sem resposta", "filho que termina sem reply", ["spawn", "output", "output", "output"]),
        ("parado", 2, "stopped", "filho parado por fora", ["spawn", "output"]),
    )
    for n, (modo, esperado, trecho, nome, chamadas) in enumerate(casos, 1):
        with tempfile.TemporaryDirectory() as tmp:
            log, env = ambiente_stub(tmp, modo)
            codigo, out, err = rodar(env, *BASE)
            res.check(codigo == esperado and trecho in err and not out.strip(),
                      f"F{n}: {nome}: exit {esperado}, o erro diz o motivo e o stdout fica vazio",
                      f"exit {codigo}, stderr {err.strip()[-90:]!r}")
            res.check(chamadas_stub(log) == chamadas,
                      f"F{n}: {nome}: " + ("desiste na terceira consulta ruim, sem insistir" if modo in ("quebra", "sem-reply")
                                           else "nao consulta mais nem tenta de novo"), f"{chamadas_stub(log)}")

    with tempfile.TemporaryDirectory() as tmp:
        log, env = ambiente_stub(tmp, "alterna")
        codigo, out, err = rodar(env, *BASE, timeout=30)
        res.check(codigo == 0 and out == "FIM-ALTERNADO\n",
                  "F7: consulta ruim isolada no meio de consultas boas nao derruba o filho (so tres seguidas contam)",
                  f"exit {codigo}, {err.strip()[-80:]!r}")


def testar_loop(res):
    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        estado, env = ambiente(tmp, "escreve")
        codigo, saida, dur = rodar_loop(root, env)
        spawns = mock.por_comando(estado, "spawn")
        texto = concluidas(root)
        res.check(codigo == 0 and "T-019" in texto, "G1: loop.sh com o adaptador: filho que escreve no projeto, portao verde, exit 0 e tarefa fechada",
                  f"exit {codigo} em {dur:.1f}s; {saida.strip().splitlines()[-1][:100] if saida.strip() else ''}")
        res.check("Evidencia: tipo=comando" in texto and "cloudroom_agente.py" in texto and "agente=" in texto,
                  "G2: a evidencia registra tipo=comando e agente= citando cloudroom_agente.py")
        res.check(len(spawns) == 1 and Path(spawns[0]["cwd"]).resolve() == root.resolve(),
                  "G3: um filho so, aberto com a pasta do projeto como diretorio corrente")
        prompt = spawns[0]["prompt"] if spawns else ""
        res.check("T-019" in prompt and "bash portao.sh" in prompt and ".loop-pergunta" in prompt
                  and (spawns[0].get("title") if spawns else None) == "loop T-019",
                  "G4: o prompt do loop chega inteiro ao filho e a thread se chama `loop T-019`")
        res.check(not (root / ".loop-lock").exists() and not (root / ".loop-pergunta").exists(),
                  "G5: a rodada nao deixa lock nem .loop-pergunta")
        res.check(subprocess.run([sys.executable, str(VALIDADOR), str(root), "--strict"], capture_output=True).returncode == 0,
                  "G6: o validador --strict aceita o TASKS.md depois de fechar")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp, "echo FALTA-ARQUIVO-XYZ\nexit 1")
        estado, env = ambiente(tmp, "ok")
        antes = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        codigo, saida, dur = rodar_loop(root, env, "--tentativas", "2")
        spawns = mock.por_comando(estado, "spawn")
        res.check(codigo == 2 and len(spawns) == 2 and (root / "docs" / "TASKS.md").read_text(encoding="utf-8") == antes,
                  "H1: portao vermelho: duas tentativas, um filho por tentativa, exit 2 e TASKS.md intacto",
                  f"exit {codigo}, {len(spawns)} filhos")
        res.check(len(spawns) == 2 and "FALTA-ARQUIVO-XYZ" not in spawns[0]["prompt"] and "FALTA-ARQUIVO-XYZ" in spawns[1]["prompt"],
                  "H2: a saida da falha do portao realimenta o prompt do segundo filho")

    with tempfile.TemporaryDirectory() as tmp:
        # saida de portao maior que o limite de realimentacao do loop (64KB): o prompt do filho vai por arquivo
        root = montar(tmp, "python3 -c \"print('Z' * 70000)\"\nexit 1")
        estado, env = ambiente(tmp, "ok")
        codigo, saida, dur = rodar_loop(root, env, "--tentativas", "2")
        spawns = mock.por_comando(estado, "spawn")
        res.check(codigo == 2 and len(spawns) == 2 and spawns[1]["prompt"].count("Z") >= 65000,
                  "H3: realimentacao de 64KB do portao chega inteira ao segundo filho, por arquivo", f"exit {codigo}")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        estado, env = ambiente(tmp, "falha")
        codigo, saida, dur = rodar_loop(root, env)
        res.check(codigo == 4 and len(mock.por_comando(estado, "spawn")) == 1 and concluidas(root).count("T-019") == 0,
                  "I1: filho que falha e nao mexe em nada: exit 4 na primeira tentativa, tarefa aberta", f"exit {codigo}")
        res.check("filho" in saida and mock.ERRO_FALHA in saida,
                  "I1: o relatorio do loop mostra o erro do filho (stderr do adaptador)")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        estado, env = ambiente(tmp, "ok")
        env["PATH"] = path_seguro()  # sem room-cli nenhum
        codigo, saida, dur = rodar_loop(root, env)
        res.check(codigo == 4 and "room-cli" in saida and not mock.chamadas(estado),
                  "I2: sem room-cli no PATH o adaptador sai 1, o loop reporta exit 4 e cita room-cli", f"exit {codigo}")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        estado, env = ambiente(tmp, "pergunta")
        codigo, saida, dur = rodar_loop(root, env, "--tentativas", "1")
        texto = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        aguardando = texto.split("## Aguardando Usuario")[1].split("## Concluidas")[0]
        res.check(codigo == 2 and "T-019" not in aguardando and mock.RESPOSTA_PERGUNTA in saida,
                  "J1: filho que pergunta na resposta (sem .loop-pergunta) nao bloqueia a tarefa: o portao decide e da exit 2",
                  f"exit {codigo}")

    with tempfile.TemporaryDirectory() as tmp:
        root = montar(tmp)
        estado, env = ambiente(tmp, "lento")
        antes = (root / "docs" / "TASKS.md").read_text(encoding="utf-8")
        codigo, saida, dur = rodar_loop(root, env, "--tempo-maximo", "2")
        paradas = mock.por_comando(estado, "stop")
        res.check(codigo == 4 and dur < 30 and "tempo maximo" in saida,
                  "K1: loop.sh --tempo-maximo 2 com filho lento: exit 4 em poucos segundos e o relatorio cita o tempo maximo",
                  f"exit {codigo} em {dur:.1f}s")
        res.check(len(paradas) == 1 and len(mock.por_comando(estado, "spawn")) == 1,
                  "K2: o SIGTERM do loop vira thread stop do filho, uma vez, sem abrir outro filho", f"{len(paradas)} stops")
        res.check((root / "docs" / "TASKS.md").read_text(encoding="utf-8") == antes and not (root / ".loop-lock").exists(),
                  "K3: depois do estouro a tarefa continua aberta e o lock foi liberado")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Testa o adaptador Cloudroom com room-cli falso.")
    parser.add_argument("--verbose", action="store_true", help="Mostra tambem o que passou.")
    args = parser.parse_args(argv)

    res = Resultado(args.verbose)
    if not WRAPPER.is_file():
        res.check(False, "scripts/cloudroom_agente.py existe", "arquivo ausente")
    else:
        testar_uso(res)
        testar_cenarios(res)
        testar_opcoes(res)
        testar_falhas_da_cli(res)
        testar_loop(res)
    print(f"Adaptador Cloudroom: {res.total - res.falhas}/{res.total} verificacoes passaram.")
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
