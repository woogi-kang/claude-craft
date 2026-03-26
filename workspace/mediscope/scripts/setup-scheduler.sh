#!/bin/bash
# Setup Cloud Scheduler for email follow-up cron
#
# Usage: bash scripts/setup-scheduler.sh

set -euo pipefail

PROJECT="memoriz-b5ba9"
REGION="asia-northeast3"
WEB_URL="https://cyh-web-124503144711.asia-northeast3.run.app"
CRON_SECRET="${CRON_SECRET:-cyh-cron-secret-$(date +%s)}"

echo "=== Enabling Cloud Scheduler API ==="
gcloud services enable cloudscheduler.googleapis.com --project "$PROJECT"

echo ""
echo "=== Creating follow-up email cron job ==="
echo "Cron secret: $CRON_SECRET"
echo "(Add CRON_SECRET=$CRON_SECRET to Cloud Run env vars)"

gcloud scheduler jobs create http cyh-followup-emails \
  --project "$PROJECT" \
  --location "$REGION" \
  --schedule "0 9 * * *" \
  --time-zone "Asia/Seoul" \
  --uri "${WEB_URL}/api/cron/follow-up" \
  --http-method POST \
  --headers "Authorization=Bearer ${CRON_SECRET},Content-Type=application/json" \
  --description "CheckYourHospital daily follow-up email cron (9 AM KST)" \
  --attempt-deadline 60s

echo ""
echo "=== Done ==="
echo "Schedule: Every day at 9:00 AM KST"
echo "Endpoint: ${WEB_URL}/api/cron/follow-up"
echo ""
echo "IMPORTANT: Add this env var to cyh-web Cloud Run service:"
echo "  CRON_SECRET=${CRON_SECRET}"
