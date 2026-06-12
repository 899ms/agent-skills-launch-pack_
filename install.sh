#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$ROOT_DIR/skills"
TARGET_DIR="${AGENT_SKILLS_DIR:-$HOME/.codex/skills}"
INSTALL_ALL=false
REQUESTED_SKILLS=()

usage() {
  cat <<'EOF'
Usage:
  ./install.sh --all
  ./install.sh skill-name
  ./install.sh skill-name --target ~/.codex/skills
  AGENT_SKILLS_DIR=~/.claude/skills ./install.sh --all

Options:
  --all           Install every skill in this package.
  --list          Print available skill names.
  --target DIR    Install into DIR instead of AGENT_SKILLS_DIR or ~/.codex/skills.
  -h, --help      Show this help.
EOF
}

list_skills() {
  find "$SOURCE_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
}

install_skill() {
  local skill_name="$1"
  local source_path="$SOURCE_DIR/$skill_name"
  local target_path="$TARGET_DIR/$skill_name"

  if [[ ! -d "$source_path" ]]; then
    printf 'ERROR: unknown skill: %s\n' "$skill_name" >&2
    printf 'Available skills:\n' >&2
    list_skills >&2
    return 1
  fi

  if [[ -d "$target_path" && ! -f "$target_path/SKILL.md" ]]; then
    printf 'ERROR: target exists but does not look like a skill directory: %s\n' "$target_path" >&2
    return 1
  fi

  mkdir -p "$TARGET_DIR"
  rm -rf "$target_path"
  cp -R "$source_path" "$target_path"
  find "$target_path" -name '.DS_Store' -delete
  printf 'Installed %s -> %s\n' "$skill_name" "$target_path"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      INSTALL_ALL=true
      shift
      ;;
    --list)
      list_skills
      exit 0
      ;;
    --target)
      if [[ $# -lt 2 ]]; then
        printf 'ERROR: --target requires a directory.\n' >&2
        exit 1
      fi
      TARGET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      printf 'ERROR: unknown option: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
    *)
      REQUESTED_SKILLS+=("$1")
      shift
      ;;
  esac
done

if [[ "$INSTALL_ALL" == true && ${#REQUESTED_SKILLS[@]} -gt 0 ]]; then
  printf 'ERROR: use either --all or specific skill names, not both.\n' >&2
  exit 1
fi

if [[ "$INSTALL_ALL" == true || ${#REQUESTED_SKILLS[@]} -eq 0 ]]; then
  while IFS= read -r skill_name; do
    REQUESTED_SKILLS+=("$skill_name")
  done < <(list_skills)
fi

for skill_name in "${REQUESTED_SKILLS[@]}"; do
  install_skill "$skill_name"
done
