DOCKERIMG=foli
DOCKERRUN=sudo docker run --rm -v `pwd`:/usr/src/app -w /usr/src/app --entrypoint="" 
#CHAPTERSFILE=test-chapters.yml
CHAPTERSFILE=current-chapters.yml
#CHAPTERSFILE=all-chapters.yml

.PHONY: all build-docker pdf tex shell clean _foliant_conf _install_foliant_preprocessors _pdf _tex

all:
	echo ":("
	exit 1

build-docker:
	sudo docker build -t ${DOCKERIMG} .

pdf: _foliant_conf
	${DOCKERRUN} -u user ${DOCKERIMG} make _pdf

tex: _foliant_conf
	${DOCKERRUN} -u user ${DOCKERIMG} make _tex

shell: _foliant_conf
	${DOCKERRUN} -it ${DOCKERIMG} bash

clean:
	rm -f output/logs/*
	rm -f *.pdf *.tex

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
