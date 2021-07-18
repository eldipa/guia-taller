#!/bin/bash

set -e
set -o pipefail

docker build                                \
    -t latex-env                            \
    -f docker/latex-env.Dockerfile          \
    docker/
