
DL - v2 2023-05-22 6:19pm
==============================

This dataset was exported via roboflow.com on March 27, 2024 at 3:49 PM GMT

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand and search unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

For state of the art Computer Vision training notebooks you can use with this dataset,
visit https://github.com/roboflow/notebooks

To find over 100k other datasets and pre-trained models, visit https://universe.roboflow.com

The dataset includes 3751 images.
Human are annotated in YOLO v7 PyTorch format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 640x360 (Stretch)

The following augmentation was applied to create 3 versions of each source image:
* Random brigthness adjustment of between -30 and +30 percent
* Salt and pepper noise was applied to 5 percent of pixels


