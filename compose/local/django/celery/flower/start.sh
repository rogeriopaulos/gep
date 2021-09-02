#!/bin/sh

set -o errexit
set -o nounset


celery flower \
    --app=taskapp \
    --broker="${CELERY_BROKER_URL}"
