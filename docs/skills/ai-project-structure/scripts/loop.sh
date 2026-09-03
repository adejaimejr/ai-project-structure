#!/usr/bin/env bash
# loop.sh - executa UMA tarefa verificavel de um projeto que usa a estrutura
# ai-project-structure, ate o portao passar ou as tentativas acabarem.
#
# Este script so orquestra. Toda edicao de docs/TASKS.md passa por
# loop_task.py, que reusa o parser do validador: um parser so no projeto.
#
# Uso:
#   loop.sh --tarefa T-042 --agente "claude -p"
#   loop.sh --tarefa T-042 --agente "codex exec" --tentativas 5
#   loop.sh --tarefa T-042 --agente "gemini -p" --projeto /caminho/do/projeto
#
# Opcoes:
#   --tarefa T-NNN      obrigatorio. A tarefa a trabalhar.
#   --agente "CMD"      obrigatorio. Comando headless da sua ferramenta. O
#                       prompt entra como ultimo argumento. Argumentos com
#                       espaco dentro de aspas nao sao suportados.
#   --tentativas N      padrao 3.
#   --projeto DIR       padrao: diretorio atual.
#   --seco              nao chama o agente; util para testar o ciclo.
#
# Exit codes:
#   0  portao passou e a tarefa foi fechada com evidencia
#   1  erro de uso, ou tarefa nao elegivel (sem `(verifica:)`, ja concluida, inexistente)
#   2  portao falhou em todas as tentativas; nada foi movido, nada foi escrito
#   3  o agente sinalizou falta de contexto; a tarefa foi para "Aguardando Usuario"
#   4  o agente falhou e nao mexeu em nada; provavelmente esta mal configurado
#
# O que este script NUNCA faz: escolher a tarefa sozinho, fechar tarefa sem
# comando declarado, escrever evidencia de tipo nao comprovado por comando, ou
# tocar SESSION.md, MEMORY.md, DECISIONS.md, AGENTS.md e specs.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPER="$SCRIPT_DIR/loop_task.py"
ARQUIVO_PERGUNTA=".loop-pergunta"

TAREFA=""; AGENTE=""; TENTATIVAS=3; PROJETO="$PWD"; SECO=0

uso() { sed -n 's/^# \{0,1\}//p' "$0" | sed '/^!/d'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --tarefa)     TAREFA="${2:-}"; shift 2 ;;
    --agente)     AGENTE="${2:-}"; shift 2 ;;
    --tentativas) TENTATIVAS="${2:-}"; shift 2 ;;
    --projeto)    PROJETO="${2:-}"; shift 2 ;;
    --seco)       SECO=1; shift ;;
    -h|--help)    uso; exit 0 ;;
    *) echo "Argumento desconhecido: $1" >&2; exit 1 ;;
  esac
done

erro() { echo "[ERRO] $*" >&2; exit 1; }

[ -n "$TAREFA" ] || erro "--tarefa e obrigatorio (ex: --tarefa T-042)."
[ "$SECO" -eq 1 ] || [ -n "$AGENTE" ] || erro "--agente e obrigatorio (ex: --agente \"claude -p\")."
[ -d "$PROJETO" ] || erro "projeto nao encontrado: $PROJETO"
[ -f "$PROJETO/docs/TASKS.md" ] || erro "$PROJETO nao parece usar a estrutura: docs/TASKS.md ausente."
case "$TENTATIVAS" in
  ''|*[!0-9]*) erro "--tentativas precisa ser um inteiro positivo." ;;
  0) erro "--tentativas precisa ser maior que zero." ;;
esac

PROJETO="$(cd "$PROJETO" && pwd)"

if [ "$SECO" -eq 0 ]; then
  read -r -a AGENTE_ARGS <<< "$AGENTE"
  command -v "${AGENTE_ARGS[0]}" >/dev/null 2>&1 \
    || erro "agente nao encontrado no PATH: ${AGENTE_ARGS[0]}"
fi

# Elegibilidade primeiro: sem portao declarado, nem chamamos o agente.
COMANDO="$(python3 "$HELPER" check "$PROJETO" "$TAREFA")" || exit 1
echo "Tarefa:  $TAREFA"
echo "Projeto: $PROJETO"
echo "Portao:  $COMANDO"
echo "Limite:  $TENTATIVAS tentativa(s)"

SINAL="$PROJETO/$ARQUIVO_PERGUNTA"
if [ -f "$SINAL" ]; then
  echo "[AVISO] $ARQUIVO_PERGUNTA de uma rodada anterior encontrado; removendo."
  rm -f "$SINAL"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
FALHA_ANTERIOR=""

for (( n=1; n<=TENTATIVAS; n++ )); do
  echo
  echo "=== Tentativa $n de $TENTATIVAS ==="

  PROMPT="Voce esta trabalhando no projeto em $PROJETO, que usa a estrutura
ai-project-structure. Leia AGENTS.md antes de mexer em qualquer arquivo e
respeite o bloco de loop que esta la.

Sua tarefa e a $TAREFA, descrita em docs/TASKS.md. Trabalhe apenas nela.

O portao desta tarefa e o comando abaixo, que sera executado depois que voce
terminar. Ele decide se o trabalho vale:

    $COMANDO

Nao mova a tarefa em docs/TASKS.md e nao escreva evidencia: quem faz isso e o
loop, depois de rodar o portao.

Se faltar contexto obrigatorio para decidir alguma coisa, NAO invente e NAO
escolha por inferencia plausivel. Escreva a pergunta, em uma frase, no arquivo
$PROJETO/$ARQUIVO_PERGUNTA e pare imediatamente."

  if [ -n "$FALHA_ANTERIOR" ]; then
    PROMPT="$PROMPT

A tentativa anterior falhou no portao. Esta e a saida real do comando; use-a
para corrigir em vez de tentar de novo do zero:

$FALHA_ANTERIOR"
  fi

  if [ "$SECO" -eq 1 ]; then
    echo "(modo seco: agente nao chamado)"
  else
    MARCA="$TMP/marca-$n"; : > "$MARCA"
    AGENTE_CODIGO=0
    ( cd "$PROJETO" && "${AGENTE_ARGS[@]}" "$PROMPT" ) || AGENTE_CODIGO=$?
    # Agente que falhou E nao mexeu em nada nunca rodou de verdade. Insistir
    # so queima tentativa e portao; o problema esta no comando, nao na tarefa.
    if [ "$AGENTE_CODIGO" -ne 0 ]; then
      MEXEU="$(find "$PROJETO" -type f -newer "$MARCA" -not -path '*/.git/*' -print -quit 2>/dev/null)"
      if [ -z "$MEXEU" ]; then
        echo
        echo "[ERRO] o agente saiu com codigo $AGENTE_CODIGO e nao alterou nenhum arquivo." >&2
        echo "Provavelmente o comando de --agente esta incompleto para uso nao" >&2
        echo "supervisionado. Veja a tabela de comandos por ferramenta em" >&2
        echo "references/loop.md. Parando antes de queimar as outras tentativas." >&2
        exit 4
      fi
      echo "[AVISO] o agente saiu com codigo $AGENTE_CODIGO, mas alterou arquivos; o portao decide."
    fi
  fi

  if [ -f "$SINAL" ]; then
    echo
    echo "O agente sinalizou falta de contexto. Registrando a pergunta e parando."
    python3 "$HELPER" bloquear "$PROJETO" "$TAREFA" --pergunta "$SINAL" || exit 1
    rm -f "$SINAL"
    exit 3
  fi

  echo "--- portao: $COMANDO"
  set +e
  ( cd "$PROJETO" && bash -c "$COMANDO" ) > "$TMP/saida.txt" 2>&1
  CODIGO=$?
  set -e
  cat "$TMP/saida.txt"
  echo "--- portao saiu com codigo $CODIGO"

  if [ "$CODIGO" -eq 0 ]; then
    python3 "$HELPER" fechar "$PROJETO" "$TAREFA" --saida "$TMP/saida.txt" --codigo 0 || exit 1
    echo
    echo "Portao verde na tentativa $n. Tarefa fechada com evidencia de comando."
    echo "A entrada de SESSION.md continua sendo sua: o loop nao escreve la."
    exit 0
  fi

  FALHA_ANTERIOR="$(cat "$TMP/saida.txt")"
done

echo
echo "Portao falhou nas $TENTATIVAS tentativas. Nada foi movido e nenhuma"
echo "evidencia foi escrita: a tarefa continua aberta, como estava."
exit 2
