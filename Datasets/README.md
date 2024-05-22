# Getting datasets

While in main directory: `scripts/download_datasets.sh path_to_dataset_version`,
then `python scripts/merge_datasets.py Datasets`.

# Dataset versions

Directory `./versions` contains dataset_version .csv files: dataset_ID_INFO.csv

`dataset_ID_INFO.csv` format:

```
dataset_dir;dataset_link
dataset_dir1;dataset_link1
dataset_dir2;dataset_link2

```

**_ALWAYS ADD NEW LINE AT THE END!_**

Example:

```
dataset_dir;dataset_link
Blind;https://universe.roboflow.com/ds/Kl4NM4lIXU?key=zGmHdmdyxO
Stroller;https://universe.roboflow.com/ds/rrhgYOwewJ?key=S80EUFU8ME

```

# Datasets:

1. https://universe.roboflow.com/jacob0501/wheelchairs-ia21y - No divide into test/valid/train
2. _On_the_road_ - https://universe.roboflow.com/myspace-7yu4s/on-the-roadv4 - All items with people (crutch,wheelchair,cane,stroller)
3. _Mtpwheelchair_multi_ - https://universe.roboflow.com/cup-dataset-ffunj/mtpwheelchair_multi - Wheelchairs without people in label
4. _Wheelchairs_1puaq_ - https://universe.roboflow.com/mrsaixa-nwonm/wheelchairs-1puaq - Usually wheelchairs without people in label
5. _Wheelchair_chaudhari_ - https://universe.roboflow.com/manasi-chaudhari-ilink-systems-com/wheelchair-yy3bm - Wheelchairs and people separately
6. _Mobility_ - https://universe.roboflow.com/lmao/mobility-aids-dioog - Various things, people with wheelchairs/cane/crutch in same label, bicycles (there is people with walking frame but only 1000 images with same person)
7. _MobilityDetection_ - https://universe.roboflow.com/mobilityaids/wheelchair-detection-hh3io - Various things, people with wheelchairs/cane/crutch in same label, stroller separately, people with walking frame (but 50% is with human in label, and other 50% is without human)
8. _BikeOnly_ - https://universe.roboflow.com/usthinternship/bike-only - bicycles
9. _BicycleSet_ - https://universe.roboflow.com/my-workplace-1x5io/bicycle-hbmem - bicycles
10. _ElectricScooter_ - https://universe.roboflow.com/tetra/electric-scooter-oezqo - electric scooter
11. _ElectricScooter2_ - https://universe.roboflow.com/delivery/trott - electric scooter
12. _Suitcase_ - https://universe.roboflow.com/roboflow-madi/airport-luggage - luggage
13. _Stroller_ - https://universe.roboflow.com/kpz3/stroller-tdpar - strollers wihout people in label
14. _Blind_ - https://universe.roboflow.com/kpz1/blind-vecl4 - Canes without people in label
15. _Wheelchair_ - https://universe.roboflow.com/kpz2/wheelchair-grmuz - Mostly wheelchairs without people in label
16. _Child_Adult_Ederly_ - https://universe.roboflow.com/kpz2/child-adult-elderly - Detecting all people as **_Adult in Dataset2/3/4_**

#

Labels for datasets were created in YOLOv8 .txt format  
(more here: https://roboflow.com/formats/yolov8-pytorch-txt)

Datasets are divided to train/vaild/test sets (70%/20%/10%)

![Test script](../scripts/test_import_datasets.py)
