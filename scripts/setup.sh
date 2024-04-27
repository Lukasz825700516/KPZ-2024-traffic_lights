#!/bin/sh

set -e

command -v dnf && dnf install python3 curl
command -v apt-get && apt-get install python3 python3-venv curl

python3 -m venv venv
. ./venv/bin/activate

pip install --upgrade pip
curl https://github.com/Lukasz825700516/KPZ-2024-traffic_lights/archive/refs/heads/master.zip -o master.zip
unzip ./master.zip

cd KPZ-2024-traffic_lights-master
pip install -r ./requirements.txt
sh ./scripts/download_datasets.sh
python ./scripts/merge_datasets.py ./Datasets
