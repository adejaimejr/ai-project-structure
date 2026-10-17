#!/usr/bin/env python3
"""Base comum dos portoes da spec 0006 (portao_t075.py a portao_t083.py).

Nao e teste. E o molde de `portao_t058.py` (montar dos assets, check, versao
coerente, verificador) mais o que os portoes da automacao do consenso repetem:
agente falso em shell, chamada de `scripts/consenso.py`, leitura do sidecar em
`docs/consensus/` e da entrada escrita em `docs/CONSENSUS.md`.

Vive em `evals/`, nao e distribuido, e nunca grava bytecode: `__pycache__`
dentro da skill derruba o verificador.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ROOT = SKILL.parents[2]
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
CONSENSO = SKILL / "scripts" / "consenso.py"
BATERIA = EVALS / "test_consenso.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]

falhas = []
total = 0


def check(ok, titulo, detalhe=""):
    global total
    total += 1
    ok = bool(ok)
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))
    return ok


def resumo(nome):
    print(f"\nPortao {nome}: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()


def ler(caminho):
    return Path(caminho).read_text(encoding="utf-8", errors="replace")


def sha256(caminho):
    return hashlib.sha256(Path(caminho).read_bytes()).hexdigest()


def montar(tmp, nome, data="2026-09-01"):
    """Projeto limpo montado dos assets, com a data de adocao preenchida."""
    r = Path(tmp) / nome
    (r / "docs" / "archive").mkdir(parents=True)
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / f, r / f)
    for f in NUCLEO:
        shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
    t = r / "docs" / "TASKS.md"
    t.write_text(t.read_text(encoding="utf-8").replace("(convencoes-2-2-0-desde: AAAA-MM-DD)", f"(convencoes-2-2-0-desde: {data})"), encoding="utf-8")
    return r


def validar(r, *flags):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(r), *flags], capture_output=True, text=True, errors="replace")
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()], p.stderr


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
    return versao, ok_acima and prosa == {versao} and marcadores == {versao} and recente.startswith(versao), recente, f"versao={versao} prosa={sorted(prosa)} marcadores={sorted(marcadores)}"


def verify_ok():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True, errors="replace", env=env)
    return p.returncode == 0, next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), p.stdout.strip()[-160:])


def bateria_minimo(piso):
    """A bateria `test_consenso.py` passa e imprime `N/N verificacoes passaram` com N >= piso."""
    if not BATERIA.is_file():
        return False, "evals/test_consenso.py ausente"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(BATERIA)], capture_output=True, text=True, errors="replace", env=env)
    m = re.search(r"(\d+)/(\d+) verificacoes passaram", p.stdout)
    n = int(m.group(2)) if m else 0
    return p.returncode == 0 and n >= piso, f"exit {p.returncode}; {n} verificacoes (piso {piso})"


# --- agente falso e chamada do orquestrador ---------------------------------

REGISTRA_PROMPT = 'printf \'%s\\n=====\\n\' "${@: -1}" >> "${LOG_PROMPT:-/dev/null}"\n'


def agente(tmp, nome, corpo):
    """Shell script no PATH do teste. O prompt chega como ultimo argumento."""
    caminho = Path(tmp) / nome
    caminho.write_text("#!/usr/bin/env bash\n" + REGISTRA_PROMPT + corpo, encoding="utf-8")
    caminho.chmod(0o755)
    return caminho


def ambiente(tmp, **extra):
    env = dict(os.environ, PATH=f"{tmp}{os.pathsep}{os.environ['PATH']}", PYTHONDONTWRITEBYTECODE="1")
    env.update({k: str(v) for k, v in extra.items()})
    return env


def prompts(log):
    log = Path(log)
    if not log.exists():
        return []
    return [p for p in ler(log).split("=====") if p.strip()]


def consenso(args, env, timeout=180):
    """(exit, saida). exit None quando o script nao existe ou estoura o tempo."""
    if not CONSENSO.is_file():
        return None, "scripts/consenso.py ausente"
    try:
        p = subprocess.run([sys.executable, str(CONSENSO), *args], capture_output=True, text=True,
                           errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"consenso.py estourou {timeout}s"
    return p.returncode, p.stdout + p.stderr


def consenso_popen(args, env):
    """Processo em segundo plano, para lock e interrupcao. None se o script nao existe."""
    if not CONSENSO.is_file():
        return None
    return subprocess.Popen([sys.executable, str(CONSENSO), *args], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, errors="replace", env=env,
                            stdin=subprocess.DEVNULL)


# --- sidecar e entrada -----------------------------------------------------

def rodadas(r):
    base = Path(r) / "docs" / "consensus"
    return sorted(p for p in base.iterdir() if p.is_dir()) if base.is_dir() else []


def manifesto(run):
    try:
        return json.loads((Path(run) / "manifesto.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def participante(m, pid):
    for p in m.get("participantes", []) if isinstance(m, dict) else []:
        if isinstance(p, dict) and p.get("id") == pid:
            return p
    return {}


def entradas(texto):
    return re.findall(r"^## (\d{4}-\d{2}-\d{2}.*)$", texto, re.M)


def corpo_da_entrada(texto, titulo):
    m = re.search(r"^## " + re.escape(titulo) + r"\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    return m.group(0) if m else None


def campo(corpo, rotulo):
    alvo = norm(rotulo)
    for linha in (corpo or "").splitlines():
        if linha.startswith("**"):
            fim = linha.find(":**", 2)
            if fim != -1 and norm(linha[2:fim]) == alvo:
                return linha[fim + 3:].strip()
    return None


def secao(corpo, titulo):
    m = re.search(r"^### " + re.escape(titulo) + r"\s*$(.*?)(?=^### |^## |\Z)", corpo or "", re.M | re.S)
    return m.group(1) if m else None


def citado(sec, token):
    """O token aparece numa linha de citacao (`> `) da secao."""
    return any(l.startswith("> ") and token in l for l in (sec or "").splitlines())


def arvore(r, ignorar=("docs/consensus", "docs/CONSENSUS.md")):
    """{caminho relativo: sha256} do projeto, fora do que a operacao pode escrever."""
    saida = {}
    for p in sorted(Path(r).rglob("*")):
        rel = p.relative_to(r).as_posix()
        if any(rel == i or rel.startswith(i + "/") for i in ignorar) or ".git" in p.parts or "__pycache__" in p.parts:
            continue
        if p.is_file():
            saida[rel] = sha256(p)
    return saida


def entrada_de_debate(data, titulo, status="resolvido", extra=""):
    """Entrada manual minima que passa limpa nos checks de hoje."""
    proximo = "\n**Proximo passo:** usuario decide\n" if status == "aberto" else ""
    return (f"\n## {data} - {titulo}\n\n**Status:** {status}\n{proximo}\n**Metodo:** pareceres-independentes\n\n"
            f"**Exposicao previa a outras posicoes:** nao\n\n**Rodada:** 1 de 1\n{extra}\n### Contexto\n\n- contexto.\n")


def autoteste(regex, exemplo, contra=None):
    """Regex de portao testada contra texto de exemplo antes de valer (regra de MEMORY.md)."""
    if not regex.search(exemplo):
        print(f"[ERRO] autoteste do portao: {regex.pattern!r} nao casa o exemplo {exemplo!r}")
        sys.exit(2)
    if contra is not None and regex.search(contra):
        print(f"[ERRO] autoteste do portao: {regex.pattern!r} casa o contraexemplo {contra!r}")
        sys.exit(2)
