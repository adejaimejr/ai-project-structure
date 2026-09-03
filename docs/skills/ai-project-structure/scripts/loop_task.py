#!/usr/bin/env python3
"""Cirurgia em docs/TASKS.md para o modulo de loop.

O `loop.sh` orquestra; este helper faz toda edicao do arquivo de memoria. A
razao de existir e nao ter dois parsers de `TASKS.md` no projeto: o que este
script sabe sobre secao, ID e marcador vem de `validate_structure.py`, que ja
e o validador oficial da estrutura.

Uso:
    loop_task.py check     <projeto> <T-NNN>
    loop_task.py fechar    <projeto> <T-NNN> --saida <arquivo> [--codigo N] [--agente CMD]
    loop_task.py bloquear  <projeto> <T-NNN> --pergunta <arquivo>

`check` imprime o comando declarado em `(verifica:)` e sai 0 quando a tarefa
e elegivel. `fechar` move para "## Concluidas" com a sub-linha de evidencia.
`bloquear` move para "## Aguardando Usuario" com a pergunta registrada.

Limites que este script aplica, vindos da spec 0004:

- so fecha tarefa que declarou `(verifica:)`;
- so escreve evidencia de `tipo=comando`, nunca `revisao-manual` nem `conferencia`;
- nao toca nenhum arquivo alem de `docs/TASKS.md`.

Somente biblioteca padrao (Python 3.8+). Exit code: 0 em sucesso, 1 em erro.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_structure as V  # noqa: E402  (mesmo diretorio, de proposito)

SECOES_ELEGIVEIS = ("em andamento", "proximas tarefas")
SECAO_CONCLUIDAS = "concluidas"
SECAO_AGUARDANDO = "aguardando usuario"
RESULTADO_MAX = 400


class Erro(Exception):
    pass


def linhas_com_secao(texto):
    """(indice, linha, secao normalizada) para cada linha fora de cerca ```."""
    dentro_de_cerca = False
    secao = None
    for i, linha in enumerate(texto.splitlines()):
        if linha.lstrip().startswith("```"):
            dentro_de_cerca = not dentro_de_cerca
            yield i, linha, None
            continue
        if dentro_de_cerca:
            yield i, linha, None
            continue
        m = re.match(r"^## (.+)$", linha)
        if m:
            secao = V.normalize(m.group(1))
        yield i, linha, secao


def achar_tarefa(texto, tid):
    """Retorna (inicio, fim, secao) da tarefa, fim exclusivo, sub-linhas incluidas."""
    linhas = texto.splitlines()
    achado = None
    for i, linha, secao in linhas_com_secao(texto):
        if secao is None or not linha.startswith("- "):
            continue
        m = V.TASK_OWN_ID_RE.match(linha[2:].strip())
        if m and int(m.group(1)) == int(tid):
            if achado is not None:
                raise Erro(f"T-{tid} aparece mais de uma vez em docs/TASKS.md.")
            achado = (i, secao)
    if achado is None:
        raise Erro(f"T-{tid} nao encontrada em docs/TASKS.md.")
    inicio, secao = achado
    fim = inicio + 1
    while fim < len(linhas) and re.match(r"^\s+[-*]\s+", linhas[fim]):
        fim += 1
    return inicio, fim, secao


def limites_da_secao(texto, secao_alvo):
    """(primeira_linha_de_conteudo, fim) da secao; fim exclusivo."""
    linhas = texto.splitlines()
    inicio = None
    for i, linha, secao in linhas_com_secao(texto):
        if secao is None:
            continue  # antes do primeiro heading, ou dentro de cerca ```
        if re.match(r"^## ", linha):
            if secao == secao_alvo and inicio is None:
                inicio = i + 1
                continue
            if inicio is not None:
                return inicio, i
    if inicio is None:
        raise Erro(
            f"docs/TASKS.md nao tem a secao '## {secao_alvo.title()}'. "
            "Rode o fluxo de atualizacao da skill antes de usar o loop."
        )
    return inicio, len(linhas)


def inserir_na_secao(linhas, secao_alvo, texto, novas_linhas):
    """Insere no topo da secao, substituindo o placeholder se ele for o unico item."""
    inicio, fim = limites_da_secao(texto, secao_alvo)
    conteudo = [(i, linhas[i]) for i in range(inicio, fim) if linhas[i].strip()]
    itens = [(i, l) for i, l in conteudo if l.startswith("- ")]
    if len(itens) == 1 and V.is_placeholder(itens[0][1][2:]):
        i = itens[0][0]
        return linhas[:i] + novas_linhas + linhas[i + 1:]
    ponto = inicio
    while ponto < fim and not linhas[ponto].strip():
        ponto += 1
    return linhas[:ponto] + novas_linhas + linhas[ponto:]


def comando_declarado(linha_tarefa):
    m = V.VERIFICA_RE.search(linha_tarefa)
    return V.squeeze(m.group(1)) if m else None


def resumir_saida(saida, codigo):
    """Uma linha: exit code mais a saida real, espacos colapsados.

    A evidencia e uma sub-linha; saida multi-linha precisa caber nela. Quando
    passa do limite, fica o **fim** da saida, que e onde suites de teste
    costumam imprimir o placar, e a truncagem e declarada em vez de escondida."""
    texto = V.squeeze(saida)
    if len(texto) > RESULTADO_MAX:
        cortado = len(texto) - RESULTADO_MAX
        texto = f"[...{cortado} caracteres iniciais omitidos] " + texto[-RESULTADO_MAX:]
    return f"exit {codigo}; {texto}" if texto else f"exit {codigo}; (sem saida)"


def ler(projeto):
    caminho = Path(projeto) / "docs" / "TASKS.md"
    if not caminho.is_file():
        raise Erro(f"{caminho} nao encontrado.")
    return caminho, caminho.read_text(encoding="utf-8")


def escrever(caminho, linhas, original):
    fim = "\n" if original.endswith("\n") else ""
    caminho.write_text("\n".join(linhas) + fim, encoding="utf-8")


def cmd_check(args):
    _, texto = ler(args.projeto)
    inicio, _, secao = achar_tarefa(texto, args.tarefa)
    linha = texto.splitlines()[inicio][2:].strip()
    if secao not in SECOES_ELEGIVEIS:
        raise Erro(
            f"T-{args.tarefa} esta em '{secao}'. O loop so aceita tarefa em "
            + " ou ".join(SECOES_ELEGIVEIS)
            + "."
        )
    comando = comando_declarado(linha)
    if not comando:
        raise Erro(
            f"T-{args.tarefa} nao declarou '(verifica: <comando>)'. Sem comando "
            "declarado nao ha portao, e o loop nao fecha tarefa sem portao."
        )
    print(comando)
    return 0


def cmd_fechar(args):
    caminho, texto = ler(args.projeto)
    inicio, fim, secao = achar_tarefa(texto, args.tarefa)
    linhas = texto.splitlines()
    linha = linhas[inicio][2:].strip()
    if secao not in SECOES_ELEGIVEIS:
        raise Erro(f"T-{args.tarefa} esta em '{secao}', nao em secao de trabalho aberto.")
    comando = comando_declarado(linha)
    if not comando:
        raise Erro(f"T-{args.tarefa} nao declarou '(verifica:)'; o loop nao pode fechar.")
    if args.codigo != 0:
        raise Erro(
            f"comando saiu {args.codigo}. O loop so fecha tarefa com portao verde; "
            "este helper recusa escrever evidencia de comando que falhou."
        )
    saida = Path(args.saida).read_text(encoding="utf-8") if args.saida else ""
    hoje = date.today().isoformat()
    # `agente` e fato conhecido com certeza: foi o loop que invocou aquele
    # comando. Registrar nao e alegacao sobre qualidade, e rastreabilidade de
    # quem produziu o trabalho.
    agente = f"agente={V.squeeze(args.agente)}; " if args.agente else ""
    novas = [
        f"- {hoje} {linha}",
        f"  - Evidencia: tipo=comando; {agente}procedimento={comando}; "
        f"resultado={resumir_saida(saida, args.codigo)}",
    ]
    restante = linhas[:inicio] + linhas[fim:]
    texto_restante = "\n".join(restante)
    resultado = inserir_na_secao(restante, SECAO_CONCLUIDAS, texto_restante, novas)
    escrever(caminho, resultado, texto)
    print(f"T-{args.tarefa} movida para Concluidas com evidencia de comando.")
    return 0


def cmd_bloquear(args):
    caminho, texto = ler(args.projeto)
    inicio, fim, secao = achar_tarefa(texto, args.tarefa)
    linhas = texto.splitlines()
    linha = linhas[inicio][2:].strip()
    if secao == SECAO_AGUARDANDO:
        raise Erro(f"T-{args.tarefa} ja esta em Aguardando Usuario.")
    pergunta = V.squeeze(Path(args.pergunta).read_text(encoding="utf-8"))
    if not pergunta:
        raise Erro("arquivo de pergunta vazio; nao ha o que registrar.")
    hoje = date.today().isoformat()
    if V.BLOCKED_RE.search(linha):
        linha = V.BLOCKED_RE.sub(f"(bloqueada: {hoje})", linha)
    else:
        linha = f"{linha} (bloqueada: {hoje})"
    novas = [
        f"- {linha}",
        f"  - **Pergunta:** {pergunta}",
        "  - **Resposta:** (A preencher.)",
    ]
    restante = linhas[:inicio] + linhas[fim:]
    resultado = inserir_na_secao(restante, SECAO_AGUARDANDO, "\n".join(restante), novas)
    escrever(caminho, resultado, texto)
    print(f"T-{args.tarefa} movida para Aguardando Usuario com a pergunta registrada.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Edicoes de docs/TASKS.md para o loop.")
    sub = parser.add_subparsers(dest="comando", required=True)

    p = sub.add_parser("check", help="Confere elegibilidade e imprime o comando declarado.")
    p.add_argument("projeto")
    p.add_argument("tarefa")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("fechar", help="Move para Concluidas com evidencia de comando.")
    p.add_argument("projeto")
    p.add_argument("tarefa")
    p.add_argument("--saida", help="Arquivo com a saida do comando.")
    p.add_argument("--codigo", type=int, default=0, help="Exit code do comando.")
    p.add_argument("--agente", help="Comando do agente que fez o trabalho, para rastreabilidade.")
    p.set_defaults(func=cmd_fechar)

    p = sub.add_parser("bloquear", help="Move para Aguardando Usuario com a pergunta.")
    p.add_argument("projeto")
    p.add_argument("tarefa")
    p.add_argument("--pergunta", required=True, help="Arquivo com a pergunta do agente.")
    p.set_defaults(func=cmd_bloquear)

    args = parser.parse_args(argv)
    digitos = re.sub(r"\D", "", args.tarefa)
    if not digitos:
        print(f"[ERRO] tarefa invalida: {args.tarefa!r} (esperado T-NNN).", file=sys.stderr)
        return 1
    args.tarefa = digitos
    try:
        return args.func(args)
    except Erro as exc:
        print(f"[ERRO] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
