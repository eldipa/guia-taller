#!/bin/bash

set -e
set -o pipefail

# Call xelatex as usual
xelatex "$@"

# If we created a snippet to pygment and it was not pygmented yet,
# do it now. The PYGMENTE_TARGET must be set by pdf.sh
if [ -z "$PYGMENTE_TARGET" ]; then
    echo "PYGMENTE_TARGET was not set!"
    exit 1
fi
if [ -f "$PYGMENTE_TARGET.snippets" -a ! -f "$PYGMENTE_TARGET.pygmented" ]; then
    ./scripts/pygmentex.py "$PYGMENTE_TARGET.snippets"
fi
