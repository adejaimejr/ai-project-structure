#!/usr/bin/env python3
"""Prova a integridade deste repositorio (o meta-projeto da skill).

Uso:
    python3 docs/skills/ai-project-structure/evals/verify_repository.py [--verbose]

Confere, em um comando so:

1. a raiz passa em `validate_structure.py --strict`;
2. cada fixture de `evals/` bate com o oracle declarado dela: modo, exit code
   e o conjunto **exato** de diagnosticos (codigo, arquivo e sujeito), com
   diagnostico a mais reprovando tanto quanto diagnostico a menos;
3. os blocos gerenciados da raiz continuam identicos aos de `assets/`
   (bloco core, bloco specs e as duas pontes);
4. os templates de `TASKS.md` e `CONSENSUS.md` carregam as convencoes da
   versao atual, e o dogfood da raiz adotou as mesmas;
4b. o aviso do ponto cego cabe no orcamento de linhas do bloco core;
5. a versao e a mesma no `SKILL.md`, nos marcadores e no `CHANGELOG.md`;
6. `evals.json` tem a estrutura esperada e os `files` resolvem;
6b. os scripts distribuidos compilam, e a bateria do modulo de loop passa;
7. nenhum travessao (U+2014) em arquivo versionado;
8. `install.sh` em destino temporario produz tres destinos identicos entre si
   e identicos a fonte canonica, tirando o que nao e distribuido.

Nunca escreve no repositorio nem nas instalacoes reais da skill: o passo 8 roda
`install.sh --project` com o diretorio de trabalho em uma pasta temporaria, e os
scripts sao conferidos com `ast.parse` e `PYTHONDONTWRITEBYTECODE`, porque
`py_compile` gravava `scripts/__pycache__` na fonte e ele ia parar nos destinos.

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

# A bateria do loop tinha 58 verificacoes em 2026-09-03. Menos que isso e teste que
# sumiu; ao acrescentar testes, suba o piso junto.
LOOP_TESTES_MINIMO = 58

# Criterio de aceite da spec 0005: o aviso do ponto cego e permanente no bloco
# core, entao todo projeto paga a leitura dele. Quatro linhas e o teto.
AVISO_PONTO_CEGO_MAX_LINHAS = 4
AVISO_PONTO_CEGO_RE = re.compile(
    r"^### Ponto Cego Da Validacao Cruzada\s*$(.*?)(?=^#{2,3} |\Z)",
    re.MULTILINE | re.DOTALL,
)

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

# Oracle por fixture. Exit code sozinho nao prova nada, e essa foi a licao do
# achado `0005-A1`: um par cujos dois lados saem 0 fica verde sem exercitar
# nada, e um par com exit codes diferentes tambem engana quando o 1 vem de um
# erro alheio ao comportamento testado. Entao cada fixture declara:
#
#   strict        modo em que ela roda;
#   exit          exit code esperado naquele modo;
#   diagnosticos  o CONJUNTO EXATO de diagnosticos, no formato estavel do
#                 `--codigos` do validador: NIVEL|CODIGO|ARQUIVO|SUJEITO.
#
# A comparacao e exata nos dois sentidos: diagnostico a menos reprova, e
# diagnostico a mais tambem. Um aviso que passe a cair na entrada errada muda o
# SUJEITO e quebra o portao, que era o buraco que a contagem de linhas deixava.
# Fixture sem a chave `diagnosticos` e recusada: oracle ausente nao vira
# aprovacao silenciosa.
FIXTURES = {
    "broken-project": {
        "strict": False,
        "exit": 1,
        "diagnosticos": [
            "ERRO|TASK-ID-DUPLICADO|docs/TASKS.md|T-001",
            "ERRO|SPEC-STATUS-INVALIDO|docs/specs/0001-login.md|0001-login.md",
        ],
    },
    "v1-project": {
        "strict": False,
        "exit": 0,
        "diagnosticos": [
            "INFO|ESTRUTURA-V1|AGENTS.md|",
            "INFO|TASKS-FORMATO-V1|docs/TASKS.md|",
        ],
    },
    # Controle do criterio "projeto que nunca registra achado nao recebe aviso
    # novo": consenso de verdade, nenhum achado, e nenhum diagnostico esperado.
    # Conjunto vazio nao e teste fraco aqui, porque a comparacao e nos dois
    # sentidos: qualquer diagnostico que apareca reprova.
    "debate-project": {"strict": True, "exit": 0, "diagnosticos": []},
    "aguardando-project/valido": {"strict": True, "exit": 0, "diagnosticos": []},
    "aguardando-project/invalido": {
        "strict": False,
        "exit": 1,
        "diagnosticos": ["ERRO|AGUARDANDO-SEM-PERGUNTA|docs/TASKS.md|T-002"],
    },
    # Os checks de achado sao AVISO, nao ERRO: sem --strict os dois lados saem 0.
    "achado-project/valido": {"strict": True, "exit": 0, "diagnosticos": []},
    "achado-project/invalido": {
        "strict": True,
        "exit": 1,
        "diagnosticos": [
            "AVISO|ACHADO-SEM-ESCAPOU|docs/CONSENSUS.md|"
            "2026-09-03 - Achado sem declarar se escapou",
            "AVISO|CONSENSO-SEM-PENDENTE|docs/CONSENSUS.md|"
            "2026-09-03 - Achado que escapou sem dizer por que nada pegou",
            "AVISO|ACHADO-SEM-SECAO-PONTO-CEGO|docs/CONSENSUS.md|"
            "2026-09-03 - Achado que escapou sem dizer por que nada pegou",
            "AVISO|ACHADO-SEM-IDENTIFICADOR|docs/CONSENSUS.md|"
            "2026-09-03 - Achado sem identificador e com valor invalido",
            "AVISO|ACHADO-ESCAPOU-INVALIDO|docs/CONSENSUS.md|"
            "2026-09-03 - Achado sem identificador e com valor invalido",
        ],
    },
}

# Titulo da entrada de debate que abre os dois lados de achado-project. Nenhum
# diagnostico pode cita-la: e o controle do criterio "projeto que nunca registra
# achado nao recebe nenhum aviso novo". A comparacao exata acima ja reprova um
# diagnostico que caia nela; o check abaixo guarda o outro lado, que e alguem
# "consertar" a falha declarando esse diagnostico como esperado.
DEBATE_CONTROLE = "Escolha do formato de data na API"


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


def rodar_validador(caminho, strict=False, codigos=False):
    cmd = [sys.executable, str(VALIDATOR), str(caminho)]
    if strict:
        cmd.append("--strict")
    if codigos:
        cmd.append("--codigos")
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
    """Cada fixture contra o oracle declarado dela: modo, exit e conjunto exato.

    Um exit code que bate nao e evidencia de nada por si so. O que prova que a
    fixture exercitou o que devia e o conjunto de diagnosticos, comparado nos
    dois sentidos."""
    for nome, oraculo in sorted(FIXTURES.items()):
        caminho = EVALS / "fixtures" / nome
        if not caminho.is_dir():
            res.check(False, f"fixture {nome}", "diretorio nao encontrado")
            continue
        if "diagnosticos" not in oraculo:
            res.check(
                False,
                f"fixture {nome} declara oracle",
                "sem a chave 'diagnosticos'; exit code sozinho nao prova nada",
            )
            continue

        strict = oraculo.get("strict", False)
        modo = "--strict" if strict else "normal"
        esperado_exit = oraculo["exit"]
        code, out = rodar_validador(caminho, strict=strict, codigos=True)
        res.check(
            code == esperado_exit,
            f"fixture {nome} em {modo}",
            f"exit {code} (esperado {esperado_exit})",
        )

        obtidos = sorted(l for l in out.splitlines() if l.strip())
        esperados = sorted(oraculo["diagnosticos"])
        faltando = [d for d in esperados if d not in obtidos]
        sobrando = [d for d in obtidos if d not in esperados]
        detalhe = []
        if faltando:
            detalhe.append("nao saiu: " + "; ".join(faltando))
        if sobrando:
            detalhe.append("saiu sem ser esperado: " + "; ".join(sobrando))
        res.check(
            obtidos == esperados,
            f"fixture {nome} com {len(esperados)} diagnosticos exatos",
            " | ".join(detalhe),
        )
        if verbose and (detalhe or code != esperado_exit):
            print(out)


def verificar_controle_do_debate(res):
    """O oracle de achado-project nao pode declarar diagnostico na entrada de debate.

    A comparacao exata ja reprova um diagnostico que caia nela. Este check guarda
    o outro lado: alguem calar a falha declarando esse diagnostico como esperado."""
    declarados = [
        d
        for nome, oraculo in FIXTURES.items()
        if nome.startswith("achado-project/")
        for d in oraculo.get("diagnosticos", [])
        if DEBATE_CONTROLE in d
    ]
    res.check(
        not declarados,
        "oracle de achado-project nao espera diagnostico na entrada de debate",
        "; ".join(declarados),
    )


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

    m = AVISO_PONTO_CEGO_RE.search(core_template or "")
    if m is None:
        res.check(False, "aviso do ponto cego no bloco core", "secao nao encontrada")
    else:
        linhas = [l for l in m.group(1).splitlines() if l.strip()]
        res.check(
            len(linhas) <= AVISO_PONTO_CEGO_MAX_LINHAS,
            f"aviso do ponto cego em ate {AVISO_PONTO_CEGO_MAX_LINHAS} linhas",
            f"{len(linhas)} linhas",
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

    campos = ("**Metodo:**", "**Exposicao previa a outras posicoes:**", "**Rodada:**",
              "**Achado:**", "**Escapou de verificacao:**",
              "**Pendente da rodada anterior:**", "Por Que Nada Pegou Antes")
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
    # `ast.parse` em vez de `py_compile`: o segundo grava `scripts/__pycache__` na
    # fonte, e o `install.sh` copiava isso para os tres destinos (REVAL-4).
    compila = [sys.executable, "-c",
               "import ast, sys; ast.parse(open(sys.argv[1], encoding='utf-8').read(), sys.argv[1])"]
    for rel, cmd in (
        ("scripts/validate_structure.py", compila),
        ("scripts/loop_task.py", compila),
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
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(teste)], capture_output=True, text=True, env=env)
    resumo = next((l for l in p.stdout.splitlines() if "verificacoes passaram" in l), "")
    res.check(p.returncode == 0, "bateria do modulo de loop", resumo.strip())
    # Exit 0 com zero verificacoes e bateria que sumiu, nao bateria verde (REVAL-4,
    # mutacao M18: sem nenhum teste o script imprimia 0/0 e este portao aceitava).
    m = re.search(r"(\d+)/(\d+) verificacoes passaram", resumo)
    total = int(m.group(2)) if m else 0
    res.check(total >= LOOP_TESTES_MINIMO, f"bateria do loop com pelo menos {LOOP_TESTES_MINIMO} verificacoes",
              f"{total} verificacoes")
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


def verificar_sem_pycache(res):
    """Nenhum `__pycache__` dentro da skill: o `install.sh` copiava o que existisse."""
    achados = sorted(p.relative_to(SKILL).as_posix() for p in SKILL.rglob("__pycache__"))
    res.check(not achados, "nenhum __pycache__ dentro da skill", ", ".join(achados))


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
    verificar_controle_do_debate(res)
    verificar_blocos(res)
    verificar_versao(res)
    verificar_convencoes(res)
    verificar_evals_json(res)
    verificar_scripts(res, args.verbose)
    verificar_testes_do_loop(res, args.verbose)
    verificar_travessao(res)
    verificar_sem_pycache(res)
    verificar_install(res, args.verbose)
    res.print()
    return 1 if res.falhas else 0


if __name__ == "__main__":
    sys.exit(main())
