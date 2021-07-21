FROM debian:bullseye-20210621

RUN apt-get -y update                           \
 && DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y install \
            apt-utils                           \
            bash                                \
            fuse3                               \
            ghostscript                         \
            less                                \
            libfuse3-dev                        \
            pandoc                              \
            preview-latex-style                 \
            procps                              \
            python3                             \
            python3-pip                         \
            python3-setuptools                  \
            python3-venv                        \
            sudo                                \
            texlive                             \
            texlive-bibtex-extra                \
            texlive-extra-utils                 \
            texlive-fonts-extra                 \
            texlive-fonts-recommended           \
            texlive-full                        \
            texlive-humanities                  \
            texlive-lang-spanish                \
            texlive-latex-base                  \
            texlive-latex-extra                 \
            texlive-latex-recommended           \
            texlive-pictures                    \
            texlive-plain-generic               \
            texlive-publishers                  \
            vim                                 \
 && apt-get clean                               \
 && rm -rf /var/lib/apt/lists/                  \
 && groupadd admin                              \
 &&  echo '%admin  ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/admin       \
 &&  chmod 0400 /etc/sudoers.d/admin                                    \
 &&  useradd -s /bin/bash -u 1000 -M -g 1000 user                       \
 &&  usermod -aG sudo user                                              \
 &&  usermod -aG admin user                                             \
 &&  mkdir -p /home/user                                                \
 &&  chown -R user /home/user

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y install \
            git                                 \
            pkg-config                          \
            build-essential                     \
 && apt-get clean                               \
 && rm -rf /var/lib/apt/lists/                  \
 && git clone git://github.com/gittup/tup.git   \
 && cd tup                                      \
 && chmod u+x ./bootstrap.sh                    \
 && CFLAGS="-g" ./build.sh                      \
 && mv build/tup /usr/bin/                      \
 && chmod a+x /usr/bin/tup                      \
 && cd ..                                       \
 && rm -R tup/

RUN pip3 install                                \
            j2cli                               \
            panflute==1.12.5


RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y install \
            graphviz                            \
 && apt-get clean                               \
 && rm -rf /var/lib/apt/lists/                  \
 && pip3 install                                \
            dot2tex

RUN pip3 install                                \
            panflute==2.1.0                     \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y install \
            wget                                \
 && apt-get clean                               \
 && rm -rf /var/lib/apt/lists/                  \
 && wget https://github.com/jgm/pandoc/releases/download/2.14.0.3/pandoc-2.14.0.3-1-amd64.deb \
 && sha256sum pandoc-2.14.0.3-1-amd64.deb | grep -q '^f1b57c63ffad059543bb7ce07eeb77a22c4f68ccabedc7e739240f15b6d8668a ' \
 && dpkg -i pandoc-2.14.0.3-1-amd64.deb    \
 && rm -f pandoc-2.14.0.3-1-amd64.deb

COPY pygmentex.sty /tmp

RUN pip3 install                                \
            pygments                            \
 && mkdir -p  /usr/share/texlive/texmf-dist/tex/latex/pygmentex             \
 && cp /tmp/pygmentex.sty /usr/share/texlive/texmf-dist/tex/latex/pygmentex \
 && cd /usr/share/texlive/texmf-dist/           \
 && mktexlsr

