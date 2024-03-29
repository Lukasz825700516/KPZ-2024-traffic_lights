import torch
import torch.nn as nn

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model will be composed of pretrained weights except for the output layers
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', classes=5)
#     1 osoby starsze 
#     2 osoby z dziećmi
#     3 osoby z wózkiem
#     4 osoby z bagażem
#     5 grupa uczniów

# Lock weights of all layers except the last one
for layer in model.parameters():
    layer.auto_grad = False


for k, v in model.named_parameters():
    if 'model.24' in k:
        v.requires_grad = True
# ...
