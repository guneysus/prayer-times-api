#!/bin/bash

function download() {
	mkdir -p _data/api/$1
	curl ${API}/api/$1/daily -o _data/api/$1/daily.json
}