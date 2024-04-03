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

# Setup custom MinIO Client configuration
setup_minio() {
  BUCKET_NAME="${MINIO_BUCKET_NAME:-rhombus}"
  ALIAS="rhombus"
  # Set the alias for the MinIO server
  mc alias set $ALIAS "http://${MINIO_SERVER_HOST}:9000" "${MINIO_SERVER_ACCESS_KEY}" "${MINIO_SERVER_ACCESS_SECRET_KEY}"

  # Create bucket if it does not exist
  if ! mc ls $ALIAS/$BUCKET_NAME &>/dev/null 2>&1; then
    mc mb $ALIAS/$BUCKET_NAME
    echo "Bucket $BUCKET_NAME created"
  else
    echo "Bucket $BUCKET_NAME already exists. Skipping bucket creation."
  fi

  mc anonymous set private $ALIAS/$BUCKET_NAME
  echo "Bucket $BUCKET_NAME is now private"
}

setup_minio
