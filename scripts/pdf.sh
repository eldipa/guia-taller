#!/bin/bash

set -e
set -o pipefail

if [ "$#" != 2 ]; then
    echo "Invalid number of arguments: $#."
    echo "Usage: $0 <input file> <out dir>"
    exit 1
fi

. scripts/run_in_docker.sh

#run_in_docker \
latexmk \
    -Werror \
    -xelatex \
    -pdfxe \
    -outdir="$2" \
    "$1" > "$2/$(basename -s .tex "$1").console_log" 2>&1

