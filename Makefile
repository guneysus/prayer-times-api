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
	docker run -itd -p 8000:8000 guneysu/prayer-times-api:latest

.PHONY: default build_whl build_egg build_docker push_docker run_docker