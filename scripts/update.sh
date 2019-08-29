#!/bin/bash
set -ex

download() {
	mkdir -p _data/api/$1
	curl http://localhost:8000/api/$1/daily -o _data/api/$1/daily.json
}

download istanbul
download ankara
download bursa
download erzurum
download eskisehir
download gaziantep
download izmir
download kayseri
download konya
download sakarya
