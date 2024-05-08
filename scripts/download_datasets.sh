#!/bin/sh 

DATASET_VERSION_FILE=${1:?"Path to dataset version file not provided: download_dataset.sh path_to_dataset_version_file"}

if ! [ -f "$DATASET_VERSION_FILE" ]; then
    echo "Dataset version file doesn't exist!"
    exit
fi

dataset_path="Datasets"

temporary_file=$dataset_path/tmp.zip

i=1
(cat "$DATASET_VERSION_FILE") | while IFS=";" read -r dataset_dir dataset_link
do
    if [ $i -gt 1 ]; then
        echo "DIR: $dataset_dir"
        echo "LINK: $dataset_link"
        curl -L "$dataset_link" > "$temporary_file"
        unzip -n "$temporary_file" -d "$dataset_path/$dataset_dir"
    fi
    i=$((i+1))
done

rm "$temporary_file"
rm README.dataset.txt README.roboflow.txt -f

echo "Successfully downloaded all datasets!"
