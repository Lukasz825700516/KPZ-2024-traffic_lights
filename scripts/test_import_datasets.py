import os
import random
import numpy as np
import yaml
from PIL import Image

PATH_TO_CHILD_DATASET = '../Datasets/Child_Elderly_Adult/DL.v2i.yolov7pytorch'

# Import .yaml file
with open(PATH_TO_CHILD_DATASET + '/data.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Change dir
os.chdir(PATH_TO_CHILD_DATASET)
os.chdir(data['train'])
path_train = os.getcwd()

# Choose random image
file = random.choice(os.listdir(os.getcwd()))
path_file = os.path.join(path_train, file)

# Open image
image = Image.open(path_file).convert("RGB")

# Open labels for this image
labels = path_file.replace("images", "labels").replace(".jpg", ".txt")

# Convert labels
with open(labels, "r") as file:
    annotation_list = file.read().split("\n")[:-1]
    annotation_list = [x.split(" ") for x in annotation_list]
    annotation_list = [[float(y) for y in x] for x in annotation_list]

annotations = np.array(annotation_list)

for annotation in annotations:
    print(data['names'][int(annotation[0])], end='')    # Connect corresponding name from .yaml file
    print(annotation)                                   # Show class number and box coordinates

# Show image
image.show()

