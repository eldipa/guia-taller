#!/bin/bash
set -e
set -o pipefail

if [ "$#" != 2 ]; then
    echo "Invalid number of arguments: $#."
    echo "Usage: $0 <input file> <out file>"
    exit 1
fi

# Number each section including chapters up to 3rd level
# (number sections, subsections and subsubsections but
# not further)
#   secnumdepth = 2
# Yeup, I said "3" but secnumdepth is set to 2.

# Make the document a 'book' like with odd and even pages having
# the same format (aka "oneside")
#   classoption: oneside

# Make the links be footnotes
#   links-as-notes: true

# Set these in the included header
#    -M "title=Guía de Taller" \
#    -M "author=Martín Di Paola" \
#    -M "date=2021" \
# However due a bug the date must be set here
# and not in the header

. scripts/x/run_in_docker.sh

# This is the way that we have to communicate to Panflute's filter
# which file must log
export PANFLUTE_TRACE_FILENAME="dbg/$(basename -s .tex "$2").panflute-trace"

#run_in_docker \
pandoc \
    --standalone \
    --from=markdown+tex_math_single_backslash \
    --to=latex \
    --top-level-division=chapter \
    --number-sections \
    -F filters/magic.py3 \
    --include-in-header=main/textbook-main-header.tex \
    --listings  \
    --citeproc  \
    --bibliography=main/biblio.bib \
    --biblatex  \
    -M "secnumdepth=2" \
    -M "classoption=oneside" \
    -M "documentclass=book" \
    -M "links-as-notes=1" \
    -M "date=2021" \
    -o "$2" \
    "$1"
