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

dataset_dirs=(
    'Blind'
    'Stroller'
    'Child_Elderly_Adult'
    'Wheelchair'
    'Suitcase'
)

for (( i = 0; i < ${#dataset_links[@]}; i++ )); do
    directory=${dataset_dirs[$i]}
    dataset_link=${dataset_links[$i]}

    curl -L "$dataset_link" > $temporary_file
    unzip -n $temporary_file -d $dataset_path/$directory
    rm $temporary_file
done

rm README.dataset.txt README.roboflow.txt

echo "Successfully downloaded all datasets!"