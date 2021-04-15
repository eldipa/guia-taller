DOCKERIMG=foli
DOCKERRUN=sudo docker run --rm -v `pwd`:/usr/src/app -w /usr/src/app --entrypoint="" 


all:
	echo ":("
	exit 1

build-docker:
	sudo docker build -t ${DOCKERIMG} .

pdf:
	${DOCKERRUN} -u user ${DOCKERIMG} make _pdf

tex:
	${DOCKERRUN} -u user ${DOCKERIMG} make _tex

shell:
	${DOCKERRUN} -it ${DOCKERIMG} bash

clean:
	rm -f output/logs/*


# Make targets to be executed *inside* the docker
_install_foliant_preprocessors:
	sudo cp fpreprocessors/*.py /usr/local/lib/python3.8/dist-packages/foliant/preprocessors/

_pdf: _install_foliant_preprocessors
	foliant make -w pandoc --logs output/logs/ pdf

_tex: _install_foliant_preprocessors
	foliant make -w pandoc --logs output/logs/ -d tex
