FROM foliant/foliant:full

RUN     groupadd -g 1000 user      \
    &&  useradd -s /bin/bash -u 1000 -M -g 1000 user    \
    &&  mkdir -p /home/user                             \
    &&  chown -R user /home/user

# We have to instal a version of Pandoc compatible with Panflute,
# a lib for Python to make filters for Pandoc.
# Current Foliant's Docker image is based on Ubuntu Focal (20.04)
# which has Pandoc 2.10, a not supported version for Panflute
COPY build_binaries/  /tmp
RUN     dpkg -i /tmp/pandoc-2.11.4-1-amd64.deb    \
    &&  pip3 install -r /tmp/requirements.txt
