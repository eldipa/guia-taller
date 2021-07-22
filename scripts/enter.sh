#!/bin/bash

set -e
set -o pipefail

. scripts/x/run_in_docker.sh

export INDOCKER=1
EXTRA="-it --env INDOCKER --env PATH -h builder"
run_in_docker bash
