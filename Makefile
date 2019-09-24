default:

build_whl:
	python.exe setup.py bdist_wheel

build_egg:
	python.exe setup.py bdist_egg

build_docker: build_whl
	docker build -t guneysu/prayer-times-api:latest .

push_docker:
	docker push guneysu/prayer-times-api:latest

run_docker:
	bash run_docker.sh

install:
	python setup.py install

test_simple:
	python -c "import prayer_times.lib as l; print(l.api.daily_by_name('istanbul'))"

stop_all:
	docker ps --no-trunc -q | xargs docker stop
	
.PHONY: default build_whl build_egg build_docker push_docker run_docker install test_simple stop_all