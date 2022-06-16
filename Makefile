PROJECT_NAME ?= ybs_task
VERSION = $(shell python3 setup.py --version | tr '+' '-')


clean:
	rm -fr *.egg-info dist
	rm -r draft
	mkdir draft
	docker system prune

sdist: clean
	python3 setup.py sdist

install: sdist
	pip install --target=draft/ dist/ybs_task-0.1.0.tar.gz

docker: sdist
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .

run: docker
	docker run -p 8000:8000 $(PROJECT_NAME):$(VERSION)

upload: docker
	docker tag $(PROJECT_NAME):$(VERSION) $(PROJECT_NAME):latest
	docker push $(REGISTRY_IMAGE):latest
