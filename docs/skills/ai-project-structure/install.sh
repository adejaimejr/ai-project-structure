#!/usr/bin/env bash
# install.sh - instala a skill ai-project-structure nas ferramentas de IA que
# adotam o Agent Skills Open Standard (Claude Code, Codex CLI, Gemini CLI).
#
# O mesmo SKILL.md serve para as tres ferramentas; este script so copia a pasta
# da skill para o diretorio que cada uma le.
#
# Uso:
#   ./install.sh                  # global, nas tres ferramentas (padrao)
#   ./install.sh --project        # instala no diretorio atual (.claude/.agents/.gemini)
#   ./install.sh --claude         # so Claude Code
#   ./install.sh --codex          # so Codex CLI
#   ./install.sh --gemini         # so Gemini CLI
#   ./install.sh --project --gemini
#   ./install.sh --all            # mesmo que sem argumento: as tres ferramentas
#   ./install.sh --sim             # confirma destinos divergentes sem perguntar
#   ./install.sh --uninstall      # remove a skill dos destinos escolhidos
#
# Caminhos de destino:
#   Claude Code : ~/.claude/skills/   (projeto: ./.claude/skills/)
#   Codex CLI   : ~/.agents/skills/   (projeto: ./.agents/skills/)
#   Gemini CLI  : ~/.gemini/skills/   (projeto: ./.gemini/skills/)
#
# Destino identico: rodar de novo instala sem pergunta. Destino divergente:
# lista as diferencas e pede confirmacao [s/N]; use --sim em automacoes.
set -euo pipefail

SKILL_NAME="ai-project-structure"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SCOPE="global"
UNINSTALL=0
SIM=0
DO_CLAUDE=0; DO_CODEX=0; DO_GEMINI=0; ANY_TOOL=0

for arg in "$@"; do
  case "$arg" in
    --global)    SCOPE="global" ;;
    --project)   SCOPE="project" ;;
    --uninstall) UNINSTALL=1 ;;
    --sim)       SIM=1 ;;
    --claude)    DO_CLAUDE=1; ANY_TOOL=1 ;;
    --codex)     DO_CODEX=1;  ANY_TOOL=1 ;;
    --gemini)    DO_GEMINI=1; ANY_TOOL=1 ;;
    --all)       DO_CLAUDE=1; DO_CODEX=1; DO_GEMINI=1; ANY_TOOL=1 ;;
    -h|--help)   sed -n 's/^# \{0,1\}//p' "$0" | sed '/^!/d'; exit 0 ;;
    *) echo "Argumento desconhecido: $arg" >&2; exit 2 ;;
  esac
done

# Nenhuma ferramenta citada => todas.
if [ "$ANY_TOOL" -eq 0 ]; then DO_CLAUDE=1; DO_CODEX=1; DO_GEMINI=1; fi

if [ "$SCOPE" = "global" ]; then
  CLAUDE_BASE="$HOME/.claude/skills"
  CODEX_BASE="$HOME/.agents/skills"
  GEMINI_BASE="$HOME/.gemini/skills"
else
  CLAUDE_BASE="$PWD/.claude/skills"
  CODEX_BASE="$PWD/.agents/skills"
  GEMINI_BASE="$PWD/.gemini/skills"
fi

ignorar_arquivo() {
  local rel="$1"
  case "$rel" in
    __pycache__/*|*/__pycache__/*|.DS_Store|*/.DS_Store|evals/*|install.sh|README.md|CHANGELOG.md)
      return 0 ;;
  esac
  return 1
}

arquivos_distribuidos() {
  local raiz="$1" arquivo rel
  while IFS= read -r -d '' arquivo; do
    rel="${arquivo#"$raiz"/}"
    ignorar_arquivo "$rel" || printf '%s\n' "$rel"
  done < <(find "$raiz" -type f -print0)
}

# Preenche DIVERGENCIAS com arquivos que a instalacao alteraria ou deixaria
# sobrando. A lista usa apenas os arquivos que o instalador distribui.
comparar_destino() {
  local dest="$1" rel
  DIVERGENCIAS=()
  while IFS= read -r rel; do
    if [ ! -f "$dest/$rel" ]; then
      DIVERGENCIAS+=("faltando: $rel")
    elif ! cmp -s "$SRC_DIR/$rel" "$dest/$rel"; then
      DIVERGENCIAS+=("diferente: $rel")
    fi
  done < <(arquivos_distribuidos "$SRC_DIR")
  while IFS= read -r rel; do
    if [ ! -f "$SRC_DIR/$rel" ]; then
      DIVERGENCIAS+=("extra: $rel")
    fi
  done < <(arquivos_distribuidos "$dest")
}

confirmar_divergencias() {
  local item resposta
  echo "  Destino divergente: $dest"
  for item in "${DIVERGENCIAS[@]}"; do
    echo "    $item"
  done
  if [ "$SIM" -eq 1 ]; then
    echo "  Confirmado por --sim."
    return
  fi
  printf '  Sobrescrever os arquivos distribuidos? [s/N] ' >&2
  if ! IFS= read -r resposta; then
    echo "Instalacao recusada: destino divergente e sem confirmacao interativa; use --sim para automatizar." >&2
    return 3
  fi
  if [ "$resposta" != "s" ]; then
    echo "Instalacao cancelada: destino divergente nao foi sobrescrito." >&2
    return 3
  fi
}

install_to() {
  local base="$1" tool="$2"
  local dest="$base/$SKILL_NAME"
  if [ "$UNINSTALL" -eq 1 ]; then
    rm -rf "$dest"
    echo "  [$tool] removido: $dest"
    return
  fi
  if [ -d "$dest" ]; then
    comparar_destino "$dest"
    if [ "${#DIVERGENCIAS[@]}" -gt 0 ]; then
      confirmar_divergencias
    fi
  fi
  mkdir -p "$dest"
  # Copia o necessario em runtime: SKILL.md, assets/, agents/ (metadado Codex),
  # scripts/ (validador) e references/ (fluxos de atualizacao e specs).
  cp "$SRC_DIR/SKILL.md" "$dest/"
  rm -rf "$dest/assets"; cp -R "$SRC_DIR/assets" "$dest/assets"
  if [ -d "$SRC_DIR/agents" ]; then
    rm -rf "$dest/agents"; cp -R "$SRC_DIR/agents" "$dest/agents"
  fi
  if [ -d "$SRC_DIR/scripts" ]; then
    rm -rf "$dest/scripts"; cp -R "$SRC_DIR/scripts" "$dest/scripts"
  fi
  if [ -d "$SRC_DIR/references" ]; then
    rm -rf "$dest/references"; cp -R "$SRC_DIR/references" "$dest/references"
  fi
  # Bytecode da fonte nao e da skill: nunca vai junto.
  find "$dest" -type d -name __pycache__ -prune -exec rm -rf {} +
  echo "  [$tool] -> $dest"
}

action="Instalando"; [ "$UNINSTALL" -eq 1 ] && action="Removendo"
echo "$action skill '$SKILL_NAME' (escopo: $SCOPE)"
if [ "$DO_CLAUDE" -eq 1 ]; then install_to "$CLAUDE_BASE" "Claude Code"; fi
if [ "$DO_CODEX"  -eq 1 ]; then install_to "$CODEX_BASE"  "Codex CLI"; fi
if [ "$DO_GEMINI" -eq 1 ]; then install_to "$GEMINI_BASE" "Gemini CLI"; fi
echo "Concluido."
