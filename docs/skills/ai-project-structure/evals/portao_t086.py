#!/usr/bin/env python3
"""Portao da T-086: bump da skill levando a secao "Passagem De Trabalho" do bloco core.

A secao entrou no bloco core em 2026-10-17 sem bump, com a 2.11.0 ja publicada em
`origin/main`. O bump precisa aparecer em todo lugar de uma vez, e o bloco core da raiz
continua identico ao dos assets.
1. `versao_coerente(NOVA)`: frontmatter em NOVA ou acima, toda prosa "versao da estrutura",
   marcadores dos assets (core, specs, loop) e secao mais recente do CHANGELOG da skill, tudo na
   mesma versao; a secao mais recente cita a secao que o bump leva.
2. Marcadores do `AGENTS.md` da raiz (core, specs, loop) na versao do frontmatter.
3. Bloco core da raiz byte a byte igual ao dos assets, com "Passagem De Trabalho" dentro.
4. T-078 a T-083 em `docs/TASKS.md` sem "a versao ja e 2.11.0"; T-078 a T-082, que carregam a
   regra "nao suba de novo", apontam para a versao nova (T-083 nunca teve a frase).
5. Raiz limpa em `--strict`; 6. verificador exit 0.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from portao_consenso_lib import ASSETS, ROOT, SKILL, autoteste, check, ler, resumo, validar, verify_ok, versao_coerente  # noqa: E402

NOVA = "2.12.0"
VELHA = "2.11.0"
SECAO = "Passagem De Trabalho"
TAREFAS = [f"T-{n:03d}" for n in range(78, 84)]
COM_REGRA = TAREFAS[:-1]  # T-083 e tarefa do agente de chat e nunca carregou "a versao ja e"

CORE_RE = re.compile(r"<!--\s*ai-project-structure:core:start.*?ai-project-structure:core:end\s*-->", re.S)
MARCADOR_RE = re.compile(r"ai-project-structure:(core|specs|loop):start\s+v(\d+\.\d+\.\d+)")
autoteste(MARCADOR_RE, "<!-- ai-project-structure:loop:start v2.11.0 -->", "<!-- ai-project-structure:loop:end -->")


def linha_da_tarefa(texto, tid):
    m = re.search(rf"^- (?:\d{{4}}-\d{{2}}-\d{{2}} )?{tid}:.*$", texto, re.M)
    return m.group(0) if m else None


def main():
    versao, ok, recente, det = versao_coerente(NOVA)
    check(ok, f"1a. versao {NOVA} ou acima, coerente em frontmatter, prosa, marcadores dos assets e CHANGELOG", det)
    check(recente.startswith(versao) and SECAO in recente, f"1b. secao mais recente do CHANGELOG da skill e a {versao} e cita \"{SECAO}\"",
          f"comeca com {recente[:12]!r}")

    raiz = ler(ROOT / "AGENTS.md")
    marcadores = dict(MARCADOR_RE.findall(raiz))
    check(set(marcadores) == {"core", "specs", "loop"} and set(marcadores.values()) == {versao},
          f"2. marcadores core, specs e loop do AGENTS.md da raiz em v{versao}",
          ", ".join(f"{k}=v{v}" for k, v in sorted(marcadores.items())) or "nenhum")

    core_raiz = CORE_RE.search(raiz)
    core_assets = CORE_RE.search(ler(ASSETS / "AGENTS.md"))
    check(core_raiz is not None and core_assets is not None and core_raiz.group(0) == core_assets.group(0),
          "3a. bloco core da raiz identico ao dos assets",
          f"{len(core_raiz.group(0))} vs {len(core_assets.group(0))} bytes" if core_raiz and core_assets else "bloco nao encontrado")
    check(core_assets is not None and f"## {SECAO}" in core_assets.group(0), f"3b. bloco core dos assets contem \"## {SECAO}\"")

    tasks = ler(ROOT / "docs" / "TASKS.md")
    problemas = []
    for tid in TAREFAS:
        linha = linha_da_tarefa(tasks, tid)
        if linha is None:
            problemas.append(f"{tid} ausente")
        elif f"a versao ja e {VELHA}" in linha:
            problemas.append(f"{tid} ainda diz {VELHA}")
        elif tid in COM_REGRA and (f"a versao ja e {versao}" not in linha or f"## {versao}" not in linha):
            problemas.append(f"{tid} nao aponta para {versao}")
    if versao == VELHA:
        problemas.append(f"frontmatter ainda em {VELHA}")
    check(not problemas, f"4. T-078 a T-083 em docs/TASKS.md sem {VELHA}; T-078 a T-082 apontam para a versao {versao}", "; ".join(problemas))

    codigo, linhas, _ = validar(ROOT, "--strict")
    check(codigo == 0, "5. raiz limpa em --strict", linhas[-1] if linhas else f"exit {codigo}")
    ok, res = verify_ok()
    check(ok, "6. verify_repository.py exit 0", res)
    return resumo("T-086")


if __name__ == "__main__":
    sys.exit(main())
