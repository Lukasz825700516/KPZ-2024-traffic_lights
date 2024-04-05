# Training

For training four datasets have been used

- Child Elderly Adult dataset
    https://universe.roboflow.com/gist-awllb/dl-bhh3b

- Blind dataset
    https://www.kaggle.com/datasets/jangbyeonghui/visually-impairedwhitecane

- Suitcase dataset
    https://www.kaggle.com/datasets/dataclusterlabs/suitcaseluggage-dataset

- Wheelchair dataset
    https://universe.roboflow.com/obj-detection-gmggm/objectdetect-iga7u  

Before usage those datasets have been merged into one large dataset with
label class space spanning all unique classes from original datasets.


The trained model was based on the YOLOv8 architecture using the cli tool
from the `urtlanalisis` python package, and the results of training were saved in 
the `last_run` directory.


![confiusion graph](./last_run/confusion/matrix_notmalized.png "Confusion graph of trained model")

Above confusion matrix presents the results of model training.

