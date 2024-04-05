"""Script with configuration of model that will be used in the project"""

import os
import time
import tempfile
import itertools
import typing
import dotenv

import PIL
import torch
from torch import nn
import torchvision
from torchvision.transforms import v2 as transforms_v2
from torchvision import datasets
import ultralytics

import roboflow

dotenv.load_dotenv()

rf = roboflow.Roboflow(api_key=os.environ['ROBOFLOW_KEY'])

project = rf.workspace("obj-detection-gmggm").project("objectdetect-iga7u")
version = project.version(4)
datasetWheelchair = version.download("yolov8")

project = rf.workspace("gist-awllb").project("dl-bhh3b")
version = project.version(4)
datasetChildrenElderyAdults = version.download("yolov8")


BATCH_SIZE=32

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Model will be composed of pretrained weights except for the output layers
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', classes=5)
#     1 osoby starsze
#     2 osoby z dziećmi
#     3 osoby z wózkiem
#     4 osoby z bagażem
#     5 grupa uczniów

# Lock weights of all layers except the last one
for k, v in model.named_parameters():
    v.requires_grad = False

PHASE_TRAIN = 'train'
PHASE_TEST = 'test'
phases = [PHASE_TRAIN, PHASE_TEST]


# data_sets = {
    # klass: {
        # purpose: datasets.ImageFolder(os.path.join(path, purpose))
        # for purpose in phases
    # } for klass, path in data_dirs.items()
# }
# data_loaders = {
    # klass: {
        # purpose: torch.utils.data.DataLoader(
            # data_sets[klass][purpose],
            # batch_size=BATCH_SIZE,
            # shuffle=True,
            # num_workers=4,
            # collate_fn=lambda batch: tuple(zip(*batch)),
        # ) for purpose in phases
    # } for klass in data_dirs
# }
# data_sizes = {
    # klass: {
        # purpose: len(data_loaders[purpose])
        # for purpose in phases
    # } for klass in data_dirs
# }
# # 


class NamespaceStuff:
    def __init__(self):
        self.imgsz = 640
        self.fraction = 0.4
        self.scale = 1
        self.fliplr = False
        self.flipud = False
        self.cache = True
        self.auto_augument = True
        self.hsv_h = False
        self.hsv_s = False
        self.hsv_v = False
        self.crop_fraction = 0.1

dataset = ultralytics.data.dataset.ClassificationDataset('Datasets', NamespaceStuff())
dataset_loader = torch.utils.data.DataLoader(dataset)


def train_model(
        model,
        criterion,
        optimizer: torch.optim.Optimizer,
        scheduler: torch.optim.lr_scheduler.LRScheduler,
        num_epochs=25
):
    """Function provided in
    https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html"""


    since = time.time()

    # Create a temporary directory to save training checkpoints
    with tempfile.TemporaryDirectory() as tempdir:
        best_model_params_path = os.path.join(tempdir, 'best_model_params.pt')

        torch.save(model.state_dict(), best_model_params_path)
        best_acc = 0.0

        for epoch in range(num_epochs):
            print(f'Epoch {epoch}/{num_epochs - 1}')
            print('-' * 10)

            # Each epoch has a training and validation phase
            for phase in phases:
                if phase == PHASE_TRAIN:
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode

                running_loss = 0.0
                running_corrects = 0

                # Iterate over data.
                for inputs, labels in dataset_loader:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    # zero the parameter gradients
                    optimizer.zero_grad()

                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == PHASE_TRAIN):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        # backward + optimize only if in training phase
                        if phase == PHASE_TRAIN:
                            loss.backward()
                            optimizer.step()

                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()

                epoch_loss = running_loss / len(dataset_loader.imgs)
                epoch_acc = float(running_corrects) / len(dataset_loader.imgs)

                print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

                # deep copy the model
                if phase == PHASE_TEST and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    torch.save(model.state_dict(), best_model_params_path)

            print()

        time_elapsed = time.time() - since
        print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
        print(f'Best val Acc: {best_acc:4f}')

        # load best model weights
        model.load_state_dict(torch.load(best_model_params_path))
    return model


# ...
