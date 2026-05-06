#!/usr/bin/env bash
# multica-pr-sync.sh
#
# GitHub의 머지된 PR을 multica DB와 동기화한다.
# 1) 각 repo에서 최근 머지된 PR 가져오기
# 2) PR 제목/본문에서 WOO-NNN 패턴 추출
# 3) 매칭되는 in_review 상태 multica 이슈를 done 으로 전환
# 4) multica-reqa-promoter 트리거하여 부모 QA 자동 승격
#
# 사용:
#   crontab -e
#   0 * * * * /Users/woogi/Development/claude-craft/scripts/multica-pr-sync.sh >> /tmp/multica-pr-sync.log 2>&1
#
# 환경변수:
#   MULTICA_PG_CONTAINER (기본: multica-postgres-1)
#   MULTICA_PG_USER      (기본: multica)
#   MULTICA_PG_DB        (기본: multica)
#   MULTICA_REPOS        (기본: 아래 REPOS 변수)
#   MULTICA_PR_LIMIT     (기본: 50, repo당 최근 N개 머지된 PR 스캔)

set -euo pipefail

PG_CONTAINER="${MULTICA_PG_CONTAINER:-multica-postgres-1}"
PG_USER="${MULTICA_PG_USER:-multica}"
PG_DB="${MULTICA_PG_DB:-multica}"
PR_LIMIT="${MULTICA_PR_LIMIT:-50}"
REPOS=(
    "Memoriz-KR/wedding-invitation"
    "Memoriz-KR/memoriz"
    "Memoriz-KR/CheckYourHospital"
)

ts() { date '+%Y-%m-%d %H:%M:%S'; }
echo "[$(ts)] multica-pr-sync start"

# 1+2단계: 각 repo에서 머지된 PR의 title+body를 모아 WOO 추출
WOO_FILE=$(mktemp)
trap 'rm -f "$WOO_FILE"' EXIT

for repo in "${REPOS[@]}"; do
    echo "[$(ts)] scanning $repo (limit $PR_LIMIT)"
    gh pr list --repo "$repo" --state merged --limit "$PR_LIMIT" \
        --json number,title,body --jq '.[] | "\(.title)\n\(.body)"' 2>/dev/null \
        | grep -oE 'WOO-[0-9]+' >> "$WOO_FILE" || true
done

sort -u "$WOO_FILE" -o "$WOO_FILE"
N=$(wc -l < "$WOO_FILE" | tr -d ' ')
echo "[$(ts)] extracted $N unique WOO refs from merged PRs"

if [ "$N" -eq 0 ]; then
    echo "[$(ts)] no WOO refs found, exiting"
    exit 0
fi

# WOO-NNN 형식을 정수 배열로 변환
WOO_NUMS=$(awk -F'-' '{print $2}' "$WOO_FILE" | paste -sd, -)

# 3단계: in_review 상태의 매칭 이슈를 done으로
docker exec -i "$PG_CONTAINER" psql -U "$PG_USER" -d "$PG_DB" <<SQL
BEGIN;

WITH targets AS (
    SELECT id, workspace_id, number
    FROM issue
    WHERE status = 'in_review'
      AND number IN (${WOO_NUMS})
),
upd AS (
    UPDATE issue SET status = 'done', updated_at = now()
    WHERE id IN (SELECT id FROM targets)
    RETURNING id, workspace_id, number
),
log AS (
    INSERT INTO activity_log (workspace_id, issue_id, actor_type, action, details)
    SELECT workspace_id, id, 'system', 'status_changed',
           jsonb_build_object('from','in_review','to','done','reason','multica-pr-sync: PR merged on GitHub')
    FROM upd
)
SELECT 'synced_to_done' AS metric, COUNT(*)::text AS value FROM upd;

COMMIT;
SQL

# 4단계: (deprecated) 과거에는 reqa-promoter 호출했으나 QA 워크플로 폐지로 제거됨.
# multica-reqa-promoter.sh는 deprecated.
PROMOTER=""
if false; then
    "$PROMOTER" 2>&1 | tail -5
fi

echo "[$(ts)] multica-pr-sync end"
