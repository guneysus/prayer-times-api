SETUP_CMD=python setup.py
PUSH_CMD=docker push
BUILD_CMD=docker build 
UPDATER=python updater.py

IMAGE=guneysu/prayer-times-api
VERSION := $(shell cat VERSION)
ARGS=--build-arg VERSION=$(VERSION) -t
PACKAGE=build_python
BUILD=build

CITIES=istanbul,ankara,bursa,erzurum,eskisehir,gaziantep,izmir,kayseri,konya,sakarya,tekirdag
HOST=http://localhost:8000

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


update_%:
	# echo $*
	$(UPDATER) -c $(CITIES) -p $* -h $(HOST)

update: update_daily # update_weekly update_monthly
	
up:
	docker-compose up -d --build

down:
	docker-compose down

# daily weekly monthly:
# 	$(UPDATER) -c $(CITIES) -p daily -h $(HOST)

.PHONY: default build_python build push run run_local install test stop up down

