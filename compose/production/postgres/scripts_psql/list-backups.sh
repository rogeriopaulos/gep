#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


echo "listando backups disponíveis"
echo "----------------------------"
ls /backups/
