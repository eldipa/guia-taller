#!/bin/bash

set -e
set -o pipefail

run_in_docker() {
    local wd="/home/user/proj/guia-taller"
    local img=latex-env
    local user="1000:1000"
    docker run                                  \
        --device /dev/fuse                      \
        --cap-add SYS_ADMIN                     \
        --security-opt apparmor:unconfined      \
        --rm                                    \
        -u "$user"                              \
        -v "$wd":/mnt                           \
        -w /mnt                                 \
        $EXTRA "$img" "$@"
}
