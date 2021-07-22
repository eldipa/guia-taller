#!/bin/bash

set -e
set -o pipefail

if [ "$#" != 2 ]; then
    echo "Invalid number of arguments: $#."
    echo "Usage: $0 <input file> <out dir>"
    exit 1
fi

. scripts/run_in_docker.sh

# Note: we use stdin to pipe the file instead of letting clang
# to read it because otherwise clang will user file's folder to search
# for the style config file instead the current directory (which
# by the way, we change to where the .clang-format file is)
cat "$1" | ( cd scripts/x/ ; clang-format -style=file ) > "$2"
