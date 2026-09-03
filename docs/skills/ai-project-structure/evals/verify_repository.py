#!/usr/bin/env python3
"""Prova a integridade deste repositorio (o meta-projeto da skill).

Uso:
    python3 docs/skills/ai-project-structure/evals/verify_repository.py [--verbose]

Confere, em um comando so:

1. a raiz passa em `validate_structure.py --strict`;
2. os fixtures de `evals/` retornam os exit codes esperados;
3. os blocos gerenciados da raiz continuam identicos aos de `assets/`
   (bloco core, bloco specs e as duas pontes);
4. os templates de `TASKS.md` e `CONSENSUS.md` carregam as convencoes da
   versao atual, e o dogfood da raiz adotou as mesmas;
5. a versao e a mesma no `SKILL.md`, nos marcadores e no `CHANGELOG.md`;
6. `evals.json` tem a estrutura esperada e os `files` resolvem;
6b. os scripts distribuidos compilam, e a bateria do modulo de loop passa;
7. nenhum travessao (U+2014) em arquivo versionado;
8. `install.sh` em destino temporario produz tres destinos identicos entre si
   e identicos a fonte canonica, tirando o que nao e distribuido.

Nunca escreve no repositorio nem nas instalacoes reais da skill: o passo 8 roda
`install.sh --project` com o diretorio de trabalho em uma pasta temporaria.

Este script vive em `evals/`, que o `install.sh` nao distribui: e ferramenta de
repositorio, nao chega na maquina de quem instala a skill.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 se tudo passar, 1 se nao.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ROOT = SKILL.parents[2]
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
ASSETS = SKILL / "assets"

# Presentes apenas na fonte canonica: o install.sh nao os copia.
NAO_DISTRIBUIDO = {"evals", "install.sh", "README.md", "CHANGELOG.md"}
IGNORADOS = {"__pycache__", ".DS_Store"}

CORE_RE = re.compile(
    r"<!--\s*ai-project-structure:core:start.*?ai-project-structure:core:end\s*-->",
    re.DOTALL,
)
SPECS_RE = re.compile(
    r"<!--\s*ai-project-structure:specs:start.*?ai-project-structure:specs:end\s*-->",
    re.DOTALL,
)
LOOP_RE = re.compile(
    r"<!--\s*ai-project-structure:loop:start.*?ai-project-structure:loop:end\s*-->",
    re.DOTALL,
)
VERSION_RE = re.compile(
    r"ai-project-structure:(?:core|specs|loop):start\s+v(\d+\.\d+\.\d+)")

# Fixture -> exit code esperado. broken-project tem 2 erros conhecidos,
# v1-project e uma estrutura pre-marcadores (passa com INFO) e
# aguardando-project traz o par valido/invalido da secao "Aguardando Usuario".
FIXTURES = {
    "broken-project": 1,
    "v1-project": 0,
    "aguardando-project/valido": 0,
    "aguardando-project/invalido": 1,
}


class Resultado:
    def __init__(self):
        self.linhas = []
        self.falhas = 0

    def check(self, ok, titulo, detalhe=""):
        if not ok:
            self.falhas += 1
        marca = "OK  " if ok else "FALHA"
        sufixo = f": {detalhe}" if detalhe else ""
        self.linhas.append(f"[{marca}] {titulo}{sufixo}")
        return ok

    def print(self):
        for linha in self.linhas:
            print(linha)
        total = len(self.linhas)
        print(f"\nResumo: {total - self.falhas}/{total} verificacoes passaram.")


def read(path):
    return Path(path).read_text(encoding="utf-8")


def rodar_validador(caminho, strict=False):
    cmd = [sys.executable, str(VALIDATOR), str(caminho)]
    if strict:
        cmd.append("--strict")
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def bloco(texto, regex):
    m = regex.search(texto)
    return m.group(0) if m else None


def verificar_raiz(res, verbose):
    code, out = rodar_validador(ROOT, strict=True)
    detalhe = "exit 0, sem erro e sem aviso" if code == 0 else f"exit {code}"
    res.check(code == 0, "validate_structure.py --strict na raiz", detalhe)
    if code != 0 and verbose:
        print(out)


def verificar_fixtures(res, verbose):
    for nome, esperado in sorted(FIXTURES.items()):
        caminho = EVALS / "fixtures" / nome
        if not caminho.is_dir():
            res.check(False, f"fixture {nome}", "diretorio nao encontrado")
            continue
        code, out = rodar_validador(caminho)
        res.check(
            code == esperado,
            f"fixture {nome}",
            f"exit {code} (esperado {esperado})",
        )
        if nome == "broken-project":
            erros = out.count("[ERRO]")
            res.check(erros == 2, "fixture broken-project com 2 erros", f"{erros} erros")
        if code != esperado and verbose:
            print(out)


def verificar_blocos(res):
    raiz = read(ROOT / "AGENTS.md")
    template = read(ASSETS / "AGENTS.md")

    core_raiz, core_template = bloco(raiz, CORE_RE), bloco(template, CORE_RE)
    res.check(
        core_raiz is not None and core_raiz == core_template,
        "bloco core identico entre AGENTS.md e assets/AGENTS.md",
        f"{len(core_raiz)} bytes" if core_raiz else "bloco nao encontrado",
    )

    specs_raiz = bloco(raiz, SPECS_RE)
    specs_partial = read(ASSETS / "partials" / "AGENTS-specs-block.md").strip()
    res.check(
        specs_raiz is not None and specs_raiz.strip() == specs_partial,
        "bloco specs identico ao partial da skill",
        "" if specs_raiz else "bloco nao encontrado na raiz",
    )

    for ponte in ("CLAUDE.md", "GEMINI.md"):
        res.check(
            read(ROOT / ponte) == read(ASSETS / ponte),
            f"ponte {ponte} identica ao template",
        )

    # O modulo de loop pode nao estar ativado aqui; o partial existe de qualquer jeito.
    loop_partial = read(ASSETS / "partials" / "AGENTS-loop-block.md").strip()
    res.check(bool(LOOP_RE.search(loop_partial)), "partial do bloco loop com marcadores pareados")
    loop_raiz = bloco(raiz, LOOP_RE)
    if loop_raiz is None:
        res.check(True, "bloco loop nao ativado na raiz", "esperado enquanto T-023 nao rodar")
    else:
        res.check(loop_raiz.strip() == loop_partial,
                  "bloco loop identico ao partial da skill")


def verificar_versao(res):
    frontmatter = read(SKILL / "SKILL.md")
    m = re.search(r'^version:\s*"?([\d.]+)"?\s*$', frontmatter, re.MULTILINE)
    if not res.check(m is not None, "SKILL.md declara version no frontmatter"):
        return
    versao = m.group(1)

    marcadores = set()
    for path in (ROOT / "AGENTS.md", ASSETS / "AGENTS.md",
                 ASSETS / "partials" / "AGENTS-specs-block.md",
                 ASSETS / "partials" / "AGENTS-loop-block.md"):
        marcadores.update(VERSION_RE.findall(read(path)))
    res.check(
        marcadores == {versao},
        f"marcadores em v{versao}",
        f"encontrados: {', '.join(sorted(marcadores)) or 'nenhum'}",
    )
    res.check(
        re.search(rf"^## {re.escape(versao)}\b", read(SKILL / "CHANGELOG.md"), re.MULTILINE)
        is not None,
        f"CHANGELOG.md da skill tem a secao {versao}",
    )


def verificar_convencoes(res):
    """Templates trazem as convencoes atuais, e o dogfood da raiz adotou as mesmas."""
    tasks_template = read(ASSETS / "docs" / "TASKS.md")
    tasks_raiz = read(ROOT / "docs" / "TASKS.md")
    for rotulo, texto in (("template", tasks_template), ("raiz", tasks_raiz)):
        faltando = [
            marca
            for marca in ("## Aguardando Usuario", "Evidencia:", "(verifica:",
                          "(bloqueada:", "(convencoes-2-2-0-desde:")
            if marca not in texto
        ]
        res.check(
            not faltando,
            f"TASKS.md ({rotulo}) com as convencoes atuais",
            "faltando: " + ", ".join(faltando) if faltando else "",
        )
    res.check(
        re.search(r"\(convencoes-2-2-0-desde:\s*\d{4}-\d{2}-\d{2}\)", tasks_raiz)
        is not None,
        "TASKS.md da raiz com a data de adocao preenchida",
    )

    campos = ("**Metodo:**", "**Exposicao previa a outras posicoes:**", "**Rodada:**")
    for rotulo, path in (("template", ASSETS / "docs" / "CONSENSUS.md"),
                         ("raiz", ROOT / "docs" / "CONSENSUS.md")):
        texto = read(path)
        faltando = [c for c in campos if c not in texto]
        res.check(
            not faltando,
            f"CONSENSUS.md ({rotulo}) com os campos declarativos",
            "faltando: " + ", ".join(faltando) if faltando else "",
        )


def verificar_evals_json(res):
    caminho = EVALS / "evals.json"
    try:
        dados = json.loads(read(caminho))
    except (OSError, json.JSONDecodeError) as exc:
        res.check(False, "evals.json valido", str(exc))
        return
    res.check(dados.get("skill_name") == "ai-project-structure", "evals.json com skill_name")
    evals = dados.get("evals")
    if not res.check(isinstance(evals, list) and evals, "evals.json com lista de evals"):
        return
    problemas = []
    for i, ev in enumerate(evals, start=1):
        faltando = [c for c in ("id", "prompt", "expected_output", "files") if c not in ev]
        if faltando:
            problemas.append(f"eval {i} sem {', '.join(faltando)}")
            continue
        if ev["id"] != i:
            problemas.append(f"eval na posicao {i} com id {ev['id']}")
        for rel in ev["files"]:
            if not (EVALS / rel).exists():
                problemas.append(f"eval {ev['id']} aponta para {rel}, que nao existe")
    res.check(not problemas, f"{len(evals)} evals coerentes", "; ".join(problemas))


def verificar_scripts(res, verbose):
    """Os scripts distribuidos precisam ao menos compilar antes de sair daqui."""
    for rel, cmd in (
        ("scripts/validate_structure.py", [sys.executable, "-m", "py_compile"]),
        ("scripts/loop_task.py", [sys.executable, "-m", "py_compile"]),
        ("scripts/loop.sh", ["bash", "-n"]),
    ):
        caminho = SKILL / rel
        if not caminho.is_file():
            res.check(False, f"{rel} existe", "arquivo ausente")
            continue
        p = subprocess.run(cmd + [str(caminho)], capture_output=True, text=True)
        res.check(p.returncode == 0, f"{rel} compila", p.stderr.strip()[:120])
    executavel = os.access(SKILL / "scripts" / "loop.sh", os.X_OK)
    res.check(executavel, "loop.sh com bit de execucao")


def verificar_testes_do_loop(res, verbose):
    """Bateria do modulo de loop, com agente falso: sem chamada de modelo."""
    teste = EVALS / "test_loop.py"
    if not teste.is_file():
        res.check(False, "evals/test_loop.py existe", "arquivo ausente")
        return
    p = subprocess.run([sys.executable, str(teste)], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if "verificacoes passaram" in l), "")
    res.check(p.returncode == 0, "bateria do modulo de loop", resumo.strip())
    if p.returncode != 0 and verbose:
        print(p.stdout)


def arquivos_versionados():
    """Rastreados mais os novos ainda nao commitados, fora os ignorados."""
    p = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return [ROOT / rel for rel in p.stdout.split("\0") if rel]


def verificar_travessao(res):
    arquivos = arquivos_versionados()
    if arquivos is None:
        res.check(False, "travessao (U+2014)", "git ls-files falhou")
        return
    culpados = []
    for path in arquivos:
        try:
            # U+2014 escapado de proposito: escrito literal, este arquivo se acusaria.
            if "\u2014" in path.read_text(encoding="utf-8"):
                culpados.append(path.relative_to(ROOT).as_posix())
        except (OSError, UnicodeDecodeError):
            continue
    res.check(
        not culpados,
        f"nenhum travessao em {len(arquivos)} arquivos versionados",
        ", ".join(culpados),
    )


def hashes(base):
    """{caminho relativo: sha256} da arvore, pulando o que nao interessa."""
    saida = {}
    for path in sorted(base.rglob("*")):
        if any(parte in IGNORADOS for parte in path.parts):
            continue
        rel = path.relative_to(base).as_posix()
        if rel.split("/")[0] in NAO_DISTRIBUIDO:
            continue
        if path.is_file():
            saida[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return saida


def verificar_install(res, verbose):
    """install.sh em destino temporario; nunca toca as instalacoes reais."""
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, HOME=tmp)
        p = subprocess.run(["bash", str(SKILL / "install.sh"), "--project"],
                           cwd=tmp, env=env, capture_output=True, text=True)
        if not res.check(p.returncode == 0, "install.sh --project em destino temporario",
                         p.stderr.strip()[:120]):
            return
        destinos = {
            "Claude Code": Path(tmp) / ".claude/skills/ai-project-structure",
            "Codex CLI": Path(tmp) / ".agents/skills/ai-project-structure",
            "Gemini CLI": Path(tmp) / ".gemini/skills/ai-project-structure",
        }
        faltando = [n for n, d in destinos.items() if not d.is_dir()]
        if not res.check(not faltando, "tres destinos criados", ", ".join(faltando)):
            return

        arvores = {nome: hashes(d) for nome, d in destinos.items()}
        referencia = arvores["Claude Code"]
        divergentes = [n for n, a in arvores.items() if a != referencia]
        res.check(
            not divergentes,
            f"tres destinos identicos entre si ({len(referencia)} arquivos)",
            ", ".join(divergentes),
        )

        fonte = hashes(SKILL)
        so_na_fonte = sorted(set(fonte) - set(referencia))
        so_no_destino = sorted(set(referencia) - set(fonte))
        diferentes = sorted(k for k in set(fonte) & set(referencia)
                            if fonte[k] != referencia[k])
        detalhe = []
        if so_na_fonte:
            detalhe.append("so na fonte: " + ", ".join(so_na_fonte))
        if so_no_destino:
            detalhe.append("so no destino: " + ", ".join(so_no_destino))
        if diferentes:
            detalhe.append("conteudo diferente: " + ", ".join(diferentes))
        res.check(
            not detalhe,
            "destino identico a fonte canonica (fora o que nao e distribuido)",
            "; ".join(detalhe),
        )
        if verbose:
            print(f"  destino temporario: {tmp} ({len(referencia)} arquivos)")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verifica a integridade do repositorio da skill ai-project-structure."
    )
    parser.add_argument("--verbose", action="store_true",
                        help="Mostra a saida completa das verificacoes que falharem.")
    args = parser.parse_args(argv)

    print(f"Verificando integridade de: {ROOT}\n")
    res = Resultado()
    verificar_raiz(res, args.verbose)
    verificar_fixtures(res, args.verbose)
    verificar_blocos(res)
    verificar_versao(res)
    verificar_convencoes(res)
    verificar_evals_json(res)
    verificar_scripts(res, args.verbose)
    verificar_testes_do_loop(res, args.verbose)
    verificar_travessao(res)
    verificar_install(res, args.verbose)
    res.print()
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
