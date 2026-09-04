#!/usr/bin/env python3
"""Portao da T-070: os dez checks de nivel AVISO decididos em T-059.

Mesmo molde de `portao_t069.py`: cobra comportamento, nao nome de codigo. Cada
caso monta um projeto minimo a partir de `assets/`, injeta o defeito e exige
que `validate_structure.py --strict` saia 1 com pelo menos um AVISO no arquivo
certo (e nenhum ERRO, porque o nivel decidido e AVISO). Um projeto limpo montado
do mesmo jeito continua limpo em `--strict`. No fim, o bump de versao que a
tarefa declara e o verificador geral em exit 0.

Casos:

1. evidencia sem os tres campos (`tipo=`, `procedimento=`, `resultado=`);
2. evidencia com os tres campos presentes e `resultado=` vazio;
3. tarefa em "Aguardando Usuario" com Pergunta, sem Resposta e sem marcador bloqueada;
4. entrada de consenso na rodada 2 com exposicao previa `nao`;
5. entrada de consenso aberta com `**Proximo passo:**` vazio;
6. cerca de codigo aberta ate o fim de `docs/TASKS.md`;
7. spec Concluida com a secao "Evidencia De Conclusao" vazia;
8. status de tarefa escrito dentro da spec;
9. ID fora de tres digitos na propria linha da tarefa (`T-1`);
10. marcador bloqueada em tarefa fora de "Aguardando Usuario";
11. marcador de adocao ainda com o placeholder `AAAA-MM-DD` (hoje INFO; passa a AVISO).

Vive em `evals/`, nao e distribuido. Somente biblioteca padrao.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SKILL = EVALS.parent
ASSETS = SKILL / "assets"
VALIDATOR = SKILL / "scripts" / "validate_structure.py"
NUCLEO = ["README.md", "PROJECT_CONTEXT.md", "SESSION.md", "MEMORY.md",
          "CONSENSUS.md", "TASKS.md", "DECISIONS.md", "QUALITY.md", "CHANGELOG.md"]
VERSAO_ANTES = "2.6.0"

falhas = []


def check(ok, titulo, detalhe=""):
    if not ok:
        falhas.append(titulo)
    print(f"[{'OK  ' if ok else 'FALHA'}] {titulo}" + (f": {detalhe}" if detalhe else ""))


def montar(tmp, nome, data="2026-09-01"):
    r = Path(tmp) / nome
    (r / "docs" / "archive").mkdir(parents=True)
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md"):
        shutil.copy(ASSETS / f, r / f)
    for f in NUCLEO:
        shutil.copy(ASSETS / "docs" / f, r / "docs" / f)
    shutil.copy(ASSETS / "docs" / "archive" / "README.md", r / "docs" / "archive" / "README.md")
    tasks = r / "docs" / "TASKS.md"
    tasks.write_text(tasks.read_text(encoding="utf-8").replace(
        "(convencoes-2-2-0-desde: AAAA-MM-DD)", f"(convencoes-2-2-0-desde: {data})"),
        encoding="utf-8")
    return r


def validar(r):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(r), "--strict", "--codigos"],
                       capture_output=True, text=True)
    return p.returncode, [l for l in p.stdout.splitlines() if l.strip()]


def aviso_em(linhas, arquivo):
    return [l for l in linhas if l.startswith("AVISO|") and l.split("|")[2] == arquivo]


def sem_erro(linhas):
    return not any(l.startswith("ERRO|") for l in linhas)


def caso(n, titulo, r, arquivo):
    code, out = validar(r)
    check(code == 1 and aviso_em(out, arquivo) and sem_erro(out),
          f"{n}. {titulo} e AVISO em {arquivo}, sem ERRO", "; ".join(out)[:220])


def concluir(r, linha):
    t = (r / "docs" / "TASKS.md").read_text(encoding="utf-8")
    (r / "docs" / "TASKS.md").write_text(
        t.replace("- (Vazio. Ao concluir", linha + "\n- (Vazio. Ao concluir"), encoding="utf-8")


def em_secao(r, secao, linha):
    t = (r / "docs" / "TASKS.md").read_text(encoding="utf-8")
    alvo = f"## {secao}\n\n"
    assert t.count(alvo) == 1, secao
    (r / "docs" / "TASKS.md").write_text(t.replace(alvo, alvo + linha + "\n", 1), encoding="utf-8")


def consenso(r, corpo):
    c = r / "docs" / "CONSENSUS.md"
    c.write_text(c.read_text(encoding="utf-8") + "\n" + corpo, encoding="utf-8")


def spec(r, nome, corpo):
    (r / "docs" / "specs").mkdir(exist_ok=True)
    (r / "docs" / "specs" / nome).write_text(corpo, encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        r = montar(tmp, "limpo")
        code, out = validar(r)
        check(code == 0 and not out, "controle: projeto limpo montado de assets passa em --strict",
              "; ".join(out)[:200])

        r = montar(tmp, "c1")
        concluir(r, "- 2026-09-03 T-009: Trabalho.\n  - Evidencia: copiei um texto qualquer.")
        caso(1, "evidencia sem tipo/procedimento/resultado", r, "docs/TASKS.md")

        r = montar(tmp, "c2")
        concluir(r, "- 2026-09-03 T-009: Trabalho.\n  - Evidencia: tipo=conferencia; procedimento=li; resultado=")
        caso(2, "evidencia com resultado= vazio", r, "docs/TASKS.md")

        r = montar(tmp, "c3")
        em_secao(r, "Aguardando Usuario", "- T-009: Escolher gateway.\n  - **Pergunta:** Stripe ou Pagar.me?")
        caso(3, "Aguardando sem Resposta e sem marcador bloqueada", r, "docs/TASKS.md")

        r = montar(tmp, "c4")
        consenso(r, "## 2026-09-02 - Fila\n\n**Status:** resolvido\n\n**Metodo:** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n\n**Rodada:** 2 de 2\n")
        caso(4, "rodada 2 com exposicao previa nao", r, "docs/CONSENSUS.md")

        r = montar(tmp, "c5")
        consenso(r, "## 2026-09-02 - Fila\n\n**Status:** aberto\n\n**Proximo passo:**\n\n**Metodo:** pareceres-independentes\n\n**Exposicao previa a outras posicoes:** nao\n\n**Rodada:** 1 de 1\n")
        caso(5, "entrada aberta com Proximo passo vazio", r, "docs/CONSENSUS.md")

        r = montar(tmp, "c6")
        t = (r / "docs" / "TASKS.md")
        t.write_text(t.read_text(encoding="utf-8") + "\n```md\n- T-099: escondida.\n", encoding="utf-8")
        caso(6, "cerca aberta ate o fim de TASKS.md", r, "docs/TASKS.md")

        r = montar(tmp, "c7")
        spec(r, "0001-x.md", "# Spec 0001\n\n**Status:** Concluida\n\n## Tarefas\n\n## Evidencia De Conclusao\n")
        caso(7, "spec Concluida com evidencia vazia", r, "docs/specs/0001-x.md")

        r = montar(tmp, "c8")
        spec(r, "0001-x.md", "# Spec 0001\n\n**Status:** Rascunho\n\n## Tarefas\n\n- T-001: tarefa (status: concluida)\n")
        caso(8, "status de tarefa dentro da spec", r, "docs/specs/0001-x.md")

        r = montar(tmp, "c9")
        em_secao(r, "Em Andamento", "- T-1: ID curto.")
        caso(9, "ID T-1 na propria linha", r, "docs/TASKS.md")

        r = montar(tmp, "c10")
        em_secao(r, "Em Andamento", "- T-009: Fora de lugar. (bloqueada: 2026-09-01)")
        caso(10, "marcador bloqueada fora de Aguardando", r, "docs/TASKS.md")

        r = montar(tmp, "c11", data="AAAA-MM-DD")
        caso(11, "marcador de adocao com placeholder", r, "docs/TASKS.md")

    fm = re.search(r'^version:\s*"?([\d.]+)"?', (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.M)
    versao = fm.group(1) if fm else "?"
    check(tuple(int(x) for x in versao.split(".")) > tuple(int(x) for x in VERSAO_ANTES.split(".")),
          f"SKILL.md com versao acima de {VERSAO_ANTES}", f"encontrada {versao}")

    p = subprocess.run([sys.executable, str(EVALS / "verify_repository.py")], capture_output=True, text=True)
    resumo = next((l for l in p.stdout.splitlines() if l.startswith("Resumo")), "")
    check(p.returncode == 0, "verify_repository.py exit 0", resumo)

    total = 14
    print(f"\nPortao T-070: {total - len(falhas)}/{total}.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
