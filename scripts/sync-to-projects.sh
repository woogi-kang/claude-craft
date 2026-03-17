#!/usr/bin/env bash
# sync-to-projects.sh — claude-craft의 .claude/ 자산을 다른 프로젝트에 동기화
#
# Usage:
#   bash scripts/sync-to-projects.sh                    # 등록된 모든 프로젝트에 동기화
#   bash scripts/sync-to-projects.sh /path/to/project   # 특정 프로젝트에만 동기화
#
# 동기화 대상: agents, commands, hooks, rules, skills (settings.json 제외)

set -euo pipefail

CRAFT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="${CRAFT_DIR}/.claude"

# 동기화할 디렉토리 목록
SYNC_DIRS=(agents commands hooks rules skills)

# 등록된 프로젝트 목록 (필요시 추가)
DEFAULT_PROJECTS=(
  "/Users/woogi/Development/memoriz"
)

# 인자가 있으면 해당 프로젝트만, 없으면 전체
if [[ $# -gt 0 ]]; then
  PROJECTS=("$@")
else
  PROJECTS=("${DEFAULT_PROJECTS[@]}")
fi

sync_project() {
  local target="$1"
  local target_claude="${target}/.claude"

  if [[ ! -d "$target" ]]; then
    echo "SKIP: $target (디렉토리 없음)"
    return
  fi

  echo "=== Syncing to: $target ==="

  # .claude 디렉토리 확보
  mkdir -p "$target_claude"

  for dir in "${SYNC_DIRS[@]}"; do
    local src="${SOURCE}/${dir}"
    local dst="${target_claude}/${dir}"

    if [[ ! -e "$src" ]]; then
      echo "  SKIP: ${dir} (소스 없음)"
      continue
    fi

    # 기존 symlink면 제거
    if [[ -L "$dst" ]]; then
      echo "  REMOVE symlink: ${dir}"
      rm "$dst"
    fi

    # rsync로 동기화 (삭제된 파일도 반영, .git 제외)
    rsync -a --delete --exclude='.git' --exclude='logs/' "${src}/" "${dst}/"
    echo "  SYNC: ${dir} ✓"
  done

  echo ""
}

echo "Source: ${SOURCE}"
echo ""

for project in "${PROJECTS[@]}"; do
  sync_project "$project"
done

echo "Done."
