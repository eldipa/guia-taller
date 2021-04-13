DOCKERIMG=foli


all:
	echo ":("
	exit 1

build-docker:
	sudo docker build -t ${DOCKERIMG} .

pdf:
	sudo docker run --rm -u user  -v `pwd`:/usr/src/app -w /usr/src/app ${DOCKERIMG} make -w pandoc --logs output/logs/ pdf

tex:
	sudo docker run --rm -u user  -v `pwd`:/usr/src/app -w /usr/src/app ${DOCKERIMG} make -w pandoc --logs output/logs/ tex

shell:
	sudo docker run --rm -it  -v `pwd`:/usr/src/app -w /usr/src/app --entrypoint="" ${DOCKERIMG} bash

clean:
	rm -f output/logs/*
