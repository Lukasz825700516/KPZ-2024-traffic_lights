"""Script with configuration of model that will be used in the project"""
import sys

import numpy
import torch
import cv2
import ultralytics

def main():
    if not len(sys.argv) > 1:
        print("missing arguments weights")
        exit()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1])
    model = model.to(device)
    model.eval()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to revieve frame")
            break

        frame = cv2.resize(frame, dsize=(640, 640), interpolation=cv2.INTER_LINEAR)
        frame = numpy.asarray(frame)
        frame = torch.from_numpy(frame)
        frame.to(device)

        result, _ = model(frame)

if __name__ == "__main__":
    main()
