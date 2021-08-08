#!/bin/bash

set -e
set -o pipefail

. scripts/x/run_in_docker.sh

# This is a hack but we must enforce a consistent environment
# so we can export to the docker the same environment and it will
# not change from run to run. This is critical to make TUP to not
# trigger a full recompilation on an environment change.
if [[ "$PATH" != *"py3env"* ]]; then
    echo "It seems that you are *not* in a python environment. You need to enter there first."
    exit 1
fi

export INDOCKER=1
EXTRA="-it --env INDOCKER --env PATH -h builder"
run_in_docker bash
