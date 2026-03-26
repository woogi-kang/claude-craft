#!/bin/bash
# Deploy Worker to Google Cloud Run
#
# Prerequisites:
#   gcloud auth login
#   gcloud config set project memoriz-b5ba9
#
# Usage:
#   cd apps/worker && bash deploy.sh

set -euo pipefail

SERVICE_NAME="cyh-worker"
REGION="asia-northeast3"
PROJECT="memoriz-b5ba9"

echo "=== Deploying ${SERVICE_NAME} to Cloud Run (${REGION}) ==="

gcloud run deploy "$SERVICE_NAME" \
  --source . \
  --region "$REGION" \
  --platform managed \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 5 \
  --min-instances 0 \
  --max-instances 3 \
  --allow-unauthenticated \
  --project "$PROJECT"

echo ""
echo "=== Deployment complete ==="
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT" --format="value(status.url)"
