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
#   ./install.sh --uninstall      # remove a skill dos destinos escolhidos
#
# Caminhos de destino:
#   Claude Code : ~/.claude/skills/   (projeto: ./.claude/skills/)
#   Codex CLI   : ~/.agents/skills/   (projeto: ./.agents/skills/)
#   Gemini CLI  : ~/.gemini/skills/   (projeto: ./.gemini/skills/)
#
# Idempotente: rodar de novo sobrescreve com seguranca.
set -euo pipefail

SKILL_NAME="ai-project-structure"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SCOPE="global"
UNINSTALL=0
DO_CLAUDE=0; DO_CODEX=0; DO_GEMINI=0; ANY_TOOL=0

for arg in "$@"; do
  case "$arg" in
    --global)    SCOPE="global" ;;
    --project)   SCOPE="project" ;;
    --uninstall) UNINSTALL=1 ;;
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

install_to() {
  local base="$1" tool="$2"
  local dest="$base/$SKILL_NAME"
  if [ "$UNINSTALL" -eq 1 ]; then
    rm -rf "$dest"
    echo "  [$tool] removido: $dest"
    return
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
[ "$DO_CLAUDE" -eq 1 ] && install_to "$CLAUDE_BASE" "Claude Code"
[ "$DO_CODEX"  -eq 1 ] && install_to "$CODEX_BASE"  "Codex CLI"
[ "$DO_GEMINI" -eq 1 ] && install_to "$GEMINI_BASE" "Gemini CLI"
echo "Concluido."
