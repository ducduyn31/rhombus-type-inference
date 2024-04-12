#!/bin/bash

# Same content as the official Minio Dockerfile
set -o errexit
set -o nounset
set -o pipefail
#set -o xtrace

# Load libraries
. /opt/bitnami/scripts/liblog.sh
. /opt/bitnami/scripts/libos.sh
. /opt/bitnami/scripts/libminioclient.sh

# Load MinIO Client environment
. /opt/bitnami/scripts/minio-client-env.sh

BUCKET_NAME="${MINIO_BUCKET_NAME:-rhombus}"
ALIAS="rhombus"

# Setup custom MinIO Client configuration
setup_minio() {
  # Set the alias for the MinIO server
  mc alias set $ALIAS "http://${MINIO_SERVER_HOST}:9000" "${MINIO_SERVER_ACCESS_KEY}" "${MINIO_SERVER_ACCESS_SECRET_KEY}"

  echo "Setting up MinIO server"
  sleep 5

  # Create bucket if it does not exist
  retry_5_times create_bucket_if_not_exists

  retry_5_times mc anonymous set private $ALIAS/$BUCKET_NAME
  echo "Bucket $BUCKET_NAME is now private"

  if ! mc event ls $ALIAS/$BUCKET_NAME | grep -q webhook1 &>/dev/null 2>&1; then
    echo "Webhook webhook1 not set for bucket $BUCKET_NAME"
    retry_5_times mc admin config set $ALIAS notify_webhook:webhook1 endpoint="${WEBHOOK_URL}"
    mc admin service restart $ALIAS
    retry_5_times mc event add $ALIAS/$BUCKET_NAME arn:minio:sqs::webhook1:webhook --event put
    echo "Webhook $WEBHOOK_URL set for bucket $BUCKET_NAME"
  else
      echo "Webhook webhook1 already set for bucket $BUCKET_NAME"
  fi
}

create_bucket_if_not_exists() {
  if ! mc ls $ALIAS | grep $BUCKET_NAME &>/dev/null 2>&1; then
    mc mb $ALIAS/$BUCKET_NAME
    echo "Bucket $BUCKET_NAME created"
  else
    echo "Bucket $BUCKET_NAME already exists. Skipping bucket creation."
  fi
}

retry_5_times() {
  local attempts=0

  until (( attempts >= 5 )); do
    attempts=$((attempts + 1))
    if "$@"; then
      return
    fi
    echo "Command '$@' failed. Retrying (attempt $attempts)..."
    sleep 5
  done

  echo "Command '$@' failed after 5 attempts" >&2
  exit 1
}

setup_minio
