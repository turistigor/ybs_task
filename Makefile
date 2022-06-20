PROJECT_NAME ?= ybs_task
PROJECT_REGISTRY = igorturist
VERSION = $(shell python3 setup.py --version | tr '+' '-')


local_clean:
	rm -fr *.egg-info dist
	rm -r draft
	mkdir draft

local_sdist: local_clean
	python3 setup.py sdist

local_install: local_sdist
	pip install --target=draft/ dist/ybs_task-0.1.0.tar.gz

docker_build: local_sdist
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .

docker_rebuild: docker_clean docker_build

docker_clean:
	docker system prune

docker_run: docker_build
	docker run -it -p 80:80 $(PROJECT_NAME):$(VERSION)

docker_rerun: docker_rebuild docker_run

docker_upload: docker_rebuild
	docker tag $(PROJECT_NAME):$(VERSION) $(PROJECT_REGISTRY)/$(PROJECT_NAME):$(VERSION)
	docker push $(PROJECT_REGISTRY)/$(PROJECT_NAME):$(VERSION)

dc_up: dc_down local_sdist
	docker-compose up -d --build

dc_up_web: dc_down local_sdist
	docker-compose up -d --build web

dc_down:
	docker-compose down
