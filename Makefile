SETUP_CMD=python setup.py
BUILD_CMD=docker build
PUSH_CMD=docker push
ARGS=-t
IMAGE=guneysu/prayer-times-api
VERSION := $(shell cat VERSION)
PACKAGE=build_python
BUILD=build

default: build

build_python:
	$(SETUP_CMD) bdist_wheel

build: build_python
	$(BUILD_CMD) $(ARGS) $(IMAGE):$(VERSION) .
	$(BUILD_CMD) $(ARGS) $(IMAGE):latest .

push: build
	$(PUSH_CMD) $(IMAGE):$(VERSION)
	$(PUSH_CMD) $(IMAGE):latest

run: build
	bash scripts/run_docker.sh

run_local:
	gunicorn prayer_times.web:app --bind=0.0.0.0:30000

install:
	$(SETUP_CMD) install

test:
	python -c "import prayer_times.lib as l; print(l.api.daily_by_name('istanbul'))"

stop:
	docker ps --no-trunc -q | xargs docker stop

debug:
	echo $(VERSION)
	
.PHONY: default build_python build push run run_local install test stop debug
