#!/bin/bash
set -ex

CID=$(docker run -itd -p 8000 guneysu/prayer-times-api:latest)

HOST=$(docker port $CID | awk -F '-> ' '{ print $2 }' | sed s/0.0.0.0/127.0.0.1/g)
export API="http://${HOST}"

source helpers.sh

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
