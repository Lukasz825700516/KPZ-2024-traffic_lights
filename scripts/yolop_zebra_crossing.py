"""Script with configuration of model that will be used in the project"""
import numpy
import torch
import cv2

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to revieve frame")
            break

        frame = cv2.resize(frame, dsize=(640, 640), interpolation=cv2.INTER_CUBIC)
        frame = numpy.asarray(frame)
        frame = torch.from_numpy(frame)
        # frame.to(device)

        # model(frame)
