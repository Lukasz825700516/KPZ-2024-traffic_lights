# Getting datasets

While in main directory: `scripts/download_datasets.sh path_to_dataset_version`,
then `python scripts/merge_datasets.py Datasets`.

# Dataset versions

Directory `./versions` contains dataset_version .csv files: dataset_ID_INFO.csv

`dataset_ID_INFO.csv` format:

```
dataset_dir1;dataset_link1
dataset_dir2;dataset_link2

```

**_ALWAYS ADD NEW LINE AT THE END!_**

Example:

```
Blind;https://universe.roboflow.com/ds/Kl4NM4lIXU?key=zGmHdmdyxO
Stroller;https://universe.roboflow.com/ds/rrhgYOwewJ?key=S80EUFU8ME

```

# Datasets:

Child_Elderly_Adult:
https://universe.roboflow.com/gist-awllb/dl-bhh3b

Blind:
https://www.kaggle.com/datasets/jangbyeonghui/visually-impairedwhitecane

Suitcase:
https://www.kaggle.com/datasets/dataclusterlabs/suitcaseluggage-dataset

Wheelchair:
https://universe.roboflow.com/obj-detection-gmggm/objectdetect-iga7u

#

Labels for datasets were created in YOLOv7 .txt format  
(more here: https://roboflow.com/formats/yolov7-pytorch-txt)

Datasets are divided to train/vaild/test sets (70%/20%/10%)

![Test script](../scripts/test_import_datasets.py)
