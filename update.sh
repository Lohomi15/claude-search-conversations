#!/usr/bin/env bash
# Pull latest changes from GitHub and sync the skill into ~/.claude/skills/.
# Works for both symlinked and copied installs.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$REPO_DIR/skills/search-conversations"
SKILL_DEST="$HOME/.claude/skills/search-conversations"

echo "→ Pulling latest from origin..."
git -C "$REPO_DIR" pull --ff-only

if [ -L "$SKILL_DEST" ]; then
  echo "✓ $SKILL_DEST is a symlink — already up to date."
elif [ -d "$SKILL_DEST" ]; then
  echo "→ Replacing copied skill at $SKILL_DEST..."
  rm -rf "$SKILL_DEST"
  cp -r "$SKILL_SRC" "$SKILL_DEST"
  echo "✓ Updated."
else
  echo "→ Installing skill at $SKILL_DEST..."
  mkdir -p "$(dirname "$SKILL_DEST")"
  cp -r "$SKILL_SRC" "$SKILL_DEST"
  echo "✓ Installed."
fi
