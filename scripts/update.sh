#!/bin/bash
set -ex

download() {
	http http://localhost:8000/api/$1 -d -o ../api/daily/$1.json
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
