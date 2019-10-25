SETUP_CMD=python setup.py
BUILD_CMD=docker build
PUSH_CMD=docker push
ARGS=-t
IMAGE=guneysu/prayer-times-api
VERSION := $(shell cat VERSION)
PACKAGE=build_python
BUILD=build

default: $(BUILD)

$(PACKAGE):
	$(SETUP_CMD) bdist_wheel

$(BUILD): $(PACKAGE)
	$(BUILD_CMD) $(ARGS) $(IMAGE):$(VERSION) .
	$(BUILD_CMD) $(ARGS) $(IMAGE):latest .

push: $(BUILD)
	$(PUSH_CMD) $(IMAGE):$(VERSION)
	$(PUSH_CMD) $(IMAGE):latest

run:
	bash run_docker.sh

install:
	$(SETUP_CMD) install

test:
	python -c "import prayer_times.lib as l; print(l.api.daily_by_name('istanbul'))"

stop:
	docker ps --no-trunc -q | xargs docker stop

debug:
	echo $(VERSION)
	
.PHONY: default build_python build push run install test stop debug
