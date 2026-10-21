#!/usr/bin/env python3
"""`room-cli` falso para os portoes e a bateria do adaptador Cloudroom (spec 0008).

Nao e teste. E um executavel chamado `room-cli`, posto no PATH do teste, que imita
o que a CLI real respondeu nas sondas de 2026-10-21 (cloudroom 0.1.67), sem gastar
modelo:

- `thread spawn` volta em seguida com um JSON `{"id": ..., "note": ...}` e recusa
  opcao desconhecida ("Other options are refused, not ignored").
- Filho com `--shared-sandbox` aparece em `thread list --json` e em `thread output`
  com `state`, `busy`, `error` e, no fim, `reply`. Sem `--all`, resposta longa vem
  cortada com o aviso "[... reply truncated ...]".
- Filho em sandbox propria (sem `--shared-sandbox`) ganha id `thr_...`, nunca
  aparece em `thread list`, e `thread output` devolve so a nota "Its replies arrive
  as messages when its turns end". E o que a CLI real faz, e e por isso que o
  adaptador nao serve nesse modo.
- `thread stop` e `thread archive` sao aceitos e registrados.

Estado em `$MOCK_ROOM_DIR/estado.json`; cenario em `$MOCK_ROOM_CENARIO`:
`ok` (responde na terceira consulta), `longo` (resposta de 20000 caracteres),
`falha` (termina com `error` e `state=failed`), `lento` (so termina quando recebe
`stop`), `pergunta` (responde com uma pergunta, state idle) e `escreve` (como `ok`,
mas grava `trabalho-do-filho.txt` na pasta corrente ao nascer, imitando um agente
de loop que mexeu no projeto). `$MOCK_ROOM_RESPOSTA` troca o texto da resposta.

Uso como modulo: `instalar(tmp, cenario)` cria o executavel e devolve o ambiente;
`chamadas(estado_dir)` devolve a lista do que o adaptador pediu a CLI.

Somente biblioteca padrao. Vive em `evals/`, nao e distribuido.
"""

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

LIMITE_PROMPT = 262144
NOTA_SHARED = ("Started in this sandbox and folder. Keep working: Cloudroom sends you a "
               "message each time it finishes a turn.")
NOTA_PROPRIA = ("Started in its own sandbox with a copy of your code (commits and uncommitted "
                "changes), on its own branch. It doesn't see your later edits; share work "
                "through Git. Use this ID with tell, stop and archive.")
NOTA_OUTPUT_PROPRIA = "This child runs in its own sandbox. Its replies arrive as messages when its turns end."
ERRO_FALHA = "Child task failed or its outcome is uncertain"
FLAGS_COM_VALOR = {"--provider", "--model", "--reasoning-level", "--service-tier", "--title",
                   "--prompt", "--prompt-file", "--request-id"}
FLAGS_SEM_VALOR = {"--shared-sandbox", "--top-level"}
RESPOSTA_PADRAO = "RESPOSTA-DO-FILHO TOKEN-MOCK-ROOM"
RESPOSTA_PERGUNTA = "Antes de seguir preciso saber: qual dos dois formatos voce quer? Nao vou inferir."


# --- lado do executavel ------------------------------------------------------

def _estado_path():
    base = os.environ.get("MOCK_ROOM_DIR")
    if not base:
        print("mock room-cli: MOCK_ROOM_DIR nao definido", file=sys.stderr)
        sys.exit(70)
    return Path(base) / "estado.json"


def _ler():
    p = _estado_path()
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"filhos": {}, "chamadas": [], "proximo": 1}


def _gravar(estado):
    p = _estado_path()
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(str(tmp), str(p))


def _cenario():
    return os.environ.get("MOCK_ROOM_CENARIO", "ok")


def _resposta():
    if _cenario() == "longo":
        return ("LINHA-LONGA " * 10) .strip() + "\n" + ("x" * 19000) + "\nFIM-DA-RESPOSTA-LONGA"
    if _cenario() == "pergunta":
        return RESPOSTA_PERGUNTA
    return os.environ.get("MOCK_ROOM_RESPOSTA", RESPOSTA_PADRAO)


def _spawn(args, estado):
    opcoes = {}
    i = 0
    while i < len(args):
        a = args[i]
        if a in FLAGS_SEM_VALOR:
            opcoes[a] = True
            i += 1
        elif a in FLAGS_COM_VALOR:
            if i + 1 >= len(args):
                print("missing value for %s" % a, file=sys.stderr)
                return 1
            opcoes[a] = args[i + 1]
            i += 2
        else:
            print("unknown option %s. Other options are refused, not ignored." % a, file=sys.stderr)
            return 1
    if "--provider" not in opcoes:
        print("--provider is required", file=sys.stderr)
        return 1
    if "--shared-sandbox" in opcoes and "--top-level" in opcoes:
        print("A top-level thread gets a sandbox of its own. Omit --shared-sandbox.", file=sys.stderr)
        return 1
    if ("--prompt" in opcoes) == ("--prompt-file" in opcoes):
        print("Use exactly one of --prompt TEXT or --prompt-file PATH", file=sys.stderr)
        return 1
    if "--prompt-file" in opcoes:
        try:
            prompt = Path(opcoes["--prompt-file"]).read_bytes()
        except OSError as erro:
            print("cannot read --prompt-file: %s" % erro, file=sys.stderr)
            return 1
    else:
        prompt = opcoes["--prompt"].encode("utf-8")
    if not 1 <= len(prompt) <= LIMITE_PROMPT:
        print("Use a prompt of 1-%d bytes" % LIMITE_PROMPT, file=sys.stderr)
        return 1
    n = estado["proximo"]
    estado["proximo"] = n + 1
    compartilhado = "--shared-sandbox" in opcoes
    ident = ("cr_child_mock%d" if compartilhado else "thr_mock%d") % n
    estado["filhos"][ident] = {
        "compartilhado": compartilhado,
        "provider": opcoes["--provider"],
        "model": opcoes.get("--model"),
        "title": opcoes.get("--title", "sem titulo"),
        "consultas": 0,
        "parado": False,
        "arquivado": False,
    }
    estado["chamadas"].append({
        "cmd": "spawn", "id": ident, "args": list(args), "cwd": os.getcwd(),
        "prompt": prompt.decode("utf-8", "replace"), "title": opcoes.get("--title"),
    })
    if _cenario() == "escreve" and compartilhado:
        Path("trabalho-do-filho.txt").write_text("feito pelo filho falso\n", encoding="utf-8")
    if compartilhado:
        print(json.dumps({"harness": opcoes["--provider"], "id": ident,
                          "model": opcoes.get("--model"), "note": NOTA_SHARED}))
    else:
        print(json.dumps({"id": ident, "note": NOTA_PROPRIA}))
    return 0


def _registro(ident, filho, com_reply):
    base = {"archived": filho["arquivado"], "busy": False, "error": None, "harness": filho["provider"],
            "id": ident, "model": filho["model"], "parent": "cr_mock_parent", "state": "idle",
            "title": filho["title"]}
    cenario = _cenario()
    if filho["parado"]:
        base["state"] = "stopped"
        return base
    if filho["consultas"] < 3:
        base["busy"] = True
        base["state"] = "pending" if filho["consultas"] < 2 else "running"
        return base
    if cenario == "lento":
        base["busy"] = True
        base["state"] = "running"
        return base
    if cenario == "falha":
        base["state"] = "failed"
        base["error"] = ERRO_FALHA
        return base
    if com_reply:
        base["reply"] = _resposta()
    return base


def _output(args, estado):
    if not args:
        print("room-cli thread output CHILD_ID [--all]", file=sys.stderr)
        return 1
    ident = args[0]
    todo = "--all" in args[1:]
    filho = estado["filhos"].get(ident)
    if filho is None:
        print("not a child thread of this thread")
        return 1
    estado["chamadas"].append({"cmd": "output", "id": ident, "all": todo})
    if not filho["compartilhado"]:
        print(json.dumps({"id": ident, "note": NOTA_OUTPUT_PROPRIA}))
        return 0
    filho["consultas"] += 1
    registro = _registro(ident, filho, com_reply=True)
    if "reply" in registro and not todo and len(registro["reply"]) > 2000:
        registro["reply"] = (registro["reply"][:2000]
                             + "\n[... reply truncated. Read all of it with `room-cli thread output %s --all`]" % ident)
    print(json.dumps(registro, ensure_ascii=False))
    return 0


def _list(args, estado):
    incluir = "--include-archived" in args
    filhos = []
    for ident, filho in estado["filhos"].items():
        if not filho["compartilhado"]:
            continue
        if filho["arquivado"] and not incluir:
            continue
        filhos.append(_registro(ident, filho, com_reply=False))
    estado["chamadas"].append({"cmd": "list", "args": list(args)})
    print(json.dumps({"children": filhos}))
    return 0


def _stop(args, estado):
    ident = args[0] if args else ""
    filho = estado["filhos"].get(ident)
    if filho is None:
        print("not a child thread of this thread")
        return 1
    filho["parado"] = True
    estado["chamadas"].append({"cmd": "stop", "id": ident})
    print(json.dumps({"id": ident, "state": "accepted"}))
    return 0


def _archive(args, estado):
    ident = args[0] if args else ""
    filho = estado["filhos"].get(ident)
    if filho is None:
        print("not a child thread of this thread")
        return 1
    filho["arquivado"] = True
    filho["parado"] = True
    estado["chamadas"].append({"cmd": "archive", "id": ident})
    print(json.dumps({"archived": True, "id": ident}))
    return 0


USO = """room-cli thread spawn --provider codex|claude-code|pi|opencode|hermes|devin|fx|openclaw [--model MODEL] [--reasoning-level LEVEL] [--service-tier default|fast] [--title TITLE] [--shared-sandbox|--top-level] --prompt TEXT|--prompt-file PATH
room-cli thread list [--include-archived]
room-cli thread output CHILD_ID [--all]
room-cli thread tell CHILD_ID TEXT
room-cli thread stop CHILD_ID
room-cli thread archive CHILD_ID"""


def main_cli(argv):
    if not argv or argv[0] in ("--help", "-h"):
        print("Commands: room-cli thread, automation (loop), mac, secret, files, preview, computer-use, feedback.")
        return 0
    if argv[0] != "thread":
        print("Unknown command %s." % argv[0])
        return 1
    sub = argv[1] if len(argv) > 1 else "--help"
    resto = [a for a in argv[2:] if a != "--json"]
    if sub in ("--help", "-h"):
        print(USO)
        return 0
    estado = _ler()
    if sub == "spawn":
        codigo = _spawn(resto, estado)
    elif sub == "output":
        codigo = _output(resto, estado)
    elif sub == "list":
        codigo = _list(resto, estado)
    elif sub == "stop":
        codigo = _stop(resto, estado)
    elif sub == "archive":
        codigo = _archive(resto, estado)
    else:
        print(USO, file=sys.stderr)
        return 1
    _gravar(estado)
    return codigo


# --- lado do teste -------------------------------------------------------------

def instalar(tmp, cenario="ok", resposta=None, nome="room-cli"):
    """Cria `<tmp>/bin/room-cli` apontando para este arquivo e devolve (bin_dir, estado_dir, env)."""
    tmp = Path(tmp)
    bin_dir = tmp / "bin"
    estado_dir = tmp / "estado-room"
    bin_dir.mkdir(parents=True, exist_ok=True)
    estado_dir.mkdir(parents=True, exist_ok=True)
    exe = bin_dir / nome
    exe.write_text("#!/usr/bin/env bash\nexec %s -I %s \"$@\"\n" % (_quote(sys.executable), _quote(str(Path(__file__).resolve()))),
                   encoding="utf-8")
    exe.chmod(0o755)
    env = dict(os.environ, PATH="%s%s%s" % (bin_dir, os.pathsep, os.environ.get("PATH", "")),
               PYTHONDONTWRITEBYTECODE="1", MOCK_ROOM_DIR=str(estado_dir), MOCK_ROOM_CENARIO=cenario)
    if resposta is not None:
        env["MOCK_ROOM_RESPOSTA"] = resposta
    return bin_dir, estado_dir, env


def _quote(texto):
    return "'" + texto.replace("'", "'\\''") + "'"


def chamadas(estado_dir):
    p = Path(estado_dir) / "estado.json"
    if not p.is_file():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("chamadas", [])


def por_comando(estado_dir, cmd):
    return [c for c in chamadas(estado_dir) if c.get("cmd") == cmd]


if __name__ == "__main__":
    sys.exit(main_cli(sys.argv[1:]))
