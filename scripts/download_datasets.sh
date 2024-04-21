#!/bin/bash

# Dataset directory
dataset_path=Datasets

# Do not modify below
dataset_path=`realpath $dataset_path`
temporary_file=$dataset_path/tmp.zip
rm $temporary_file -f

dataset_links=( 
    'https://universe.roboflow.com/ds/Kl4NM4lIXU?key=zGmHdmdyxO'
    'https://universe.roboflow.com/ds/veREHEjegj?key=GeS0UadfXA'
    'https://universe.roboflow.com/ds/GGOHURobzV?key=GRIyo7vDjZ'
    'https://universe.roboflow.com/ds/RFkCt0neqM?key=1cAkukn7Qu'
    'https://universe.roboflow.com/ds/g2Rulh3EIN?key=cMHsiqOBCG'
)


for dataset_link in "${dataset_links[@]}"; do
    curl -L "$dataset_link" > $temporary_file
    unzip -n $temporary_file -d "$dataset_path"
    rm $temporary_file
done

echo "Successfully downloaded all datasets!"