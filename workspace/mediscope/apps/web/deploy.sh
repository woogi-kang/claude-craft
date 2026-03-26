#!/bin/bash
# Deploy Frontend to Google Cloud Run
#
# Usage: cd apps/web && bash deploy.sh

set -euo pipefail

SERVICE_NAME="cyh-web"
REGION="asia-northeast3"
PROJECT="memoriz-b5ba9"

echo "=== Deploying ${SERVICE_NAME} to Cloud Run (${REGION}) ==="

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60 \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 3 \
  --allow-unauthenticated \
  --project "$PROJECT" \
  --set-build-env-vars "NEXT_PUBLIC_SUPABASE_URL=${NEXT_PUBLIC_SUPABASE_URL},NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=${NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY}" \
  --set-env-vars "SUPABASE_SECRET_KEY=${SUPABASE_SECRET_KEY},WORKER_URL=${WORKER_URL},WORKER_API_KEY=${WORKER_API_KEY},RESEND_API_KEY=${RESEND_API_KEY}"

echo ""
echo "=== Deployment complete ==="
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT" --format="value(status.url)"
