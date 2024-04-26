#!/bin/sh

dataset_path="Datasets"

dataset_links="https://universe.roboflow.com/ds/Kl4NM4lIXU?key=zGmHdmdyxO \
https://universe.roboflow.com/ds/rrhgYOwewJ?key=S80EUFU8ME \
https://universe.roboflow.com/ds/GGOHURobzV?key=GRIyo7vDjZ \
https://universe.roboflow.com/ds/RFkCt0neqM?key=1cAkukn7Qu \
https://universe.roboflow.com/ds/g2Rulh3EIN?key=cMHsiqOBCG"

dataset_dirs="Blind \
Stroller \
Child_Elderly_Adult \
Wheelchair \
Suitcase"

temporary_file=$dataset_path/tmp.zip

i=1
for link in $dataset_links; do
    directory=$(echo "$dataset_dirs" | cut -d ' ' -f "$i")
    curl -L "$link" > "$temporary_file"
    unzip -n "$temporary_file" -d "$dataset_path/$directory"
    i=$((i + 1))
done

rm "$temporary_file"
rm README.dataset.txt README.roboflow.txt -f

echo "Successfully downloaded all datasets!"
