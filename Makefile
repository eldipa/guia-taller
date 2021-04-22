DOCKERIMG=foli
DOCKERRUN=sudo docker run --rm -v `pwd`:/usr/src/app -w /usr/src/app --entrypoint="" 
#CHAPTERSFILE=test-chapters.yml
CHAPTERSFILE=current-chapters.yml
#CHAPTERSFILE=all-chapters.yml

.PHONY: all build-docker pdf tex shell clean _foliant_conf _install_foliant_preprocessors _pdf _tex

PNGFILES=$(shell find images/ -type f -name '*.png')
PNGTOKENS=$(patsubst %.png,.tokens/%.pngtoken,$(PNGFILES))

all:
	echo ":("
	exit 1

# Docker image used to build the PDFs. Based on Foliant (python)
# docker.
build-docker:
	sudo docker build -t ${DOCKERIMG} .

# Make targets: PDF or LaTex files
pdf: _foliant_conf preprocess
	${DOCKERRUN} -u user ${DOCKERIMG} make _pdf

tex: _foliant_conf preprocess
	${DOCKERRUN} -u user ${DOCKERIMG} make _tex

# Run an interactive shell of the docker image to play with it
shell: _foliant_conf
	${DOCKERRUN} -it ${DOCKERIMG} bash

clean:
	rm -f output/logs/*
	rm -f *.pdf *.tex

# For each *.png (images/images/xkcd/password_strength_936.png),
# compile an optimized version of it inplace and create a token .pngtoken
# (.tokens/images/xkcd/password_strength_936.pngtoken) to mark that the
# file was optimized
#
# Note: this is a Static Pattern Rules
# https://web.mit.edu/gnu/doc/html/make_toc.html#SEC37
$(PNGTOKENS): .tokens/%.pngtoken: %.png
	@mkdir -p "$(dir $@)"
	optipng -o7 --strip all "$<"
	@touch "$@"

# preprocess (outside the docker)
# NOTE: we could put this inside the docker, we just need to tweak
# the docker image and set this "preprocess" target as dependency
# of _pdf and _tex
preprocess: $(PNGTOKENS)


# create the foliant configuration file based on a base/general conf
# and a custom chapter list.
_foliant_conf:
	cat foliant-base.yml ${CHAPTERSFILE} > ._foliant_conf.yml

# Make targets to be executed *inside* the docker
_install_foliant_preprocessors:
	sudo cp fpreprocessors/*.py /usr/local/lib/python3.8/dist-packages/foliant/preprocessors/

_pdf: _install_foliant_preprocessors
	foliant make -c ._foliant_conf.yml -w pandoc --logs output/logs/ pdf

_tex: _install_foliant_preprocessors
	foliant make -c ._foliant_conf.yml  -w pandoc --logs output/logs/ -d tex
