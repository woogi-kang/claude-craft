#!/bin/bash
# Deploy Worker to Google Cloud Run
#
# Prerequisites:
#   gcloud auth login
#   gcloud config set project YOUR_PROJECT_ID
#
# Usage:
#   bash deploy.sh

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
REGION="asia-northeast3"  # Seoul
SERVICE_NAME="cyh-worker"
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "=== Building Docker image ==="
gcloud builds submit --tag "$IMAGE" .

echo "=== Deploying to Cloud Run ==="
gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE" \
  --region "$REGION" \
  --platform managed \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 5 \
  --min-instances 0 \
  --max-instances 3 \
  --set-env-vars "SUPABASE_URL=${SUPABASE_URL}" \
  --set-env-vars "SUPABASE_SECRET_KEY=${SUPABASE_SECRET_KEY}" \
  --set-env-vars "WORKER_API_KEY=${WORKER_API_KEY}" \
  --set-env-vars "PAGESPEED_API_KEY=${PAGESPEED_API_KEY}" \
  --allow-unauthenticated

echo ""
echo "=== Deployment complete ==="
gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)"
