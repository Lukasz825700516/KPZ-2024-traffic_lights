import sys
import os
import torch
import cv2
import ultralytics
import time
import argparse
from TrafficLights import TrafficLights

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="traffic_lights_demo",
        description="Controls traffic lights using Deep Learning."
    )

    parser = argparse.ArgumentParser(description='Controls traffic lights using Deep Learning.')
    parser.add_argument('weights', type=str, help='File containing YOLO\'s weights and biases.')
    parser.add_argument('source', type=str, help='Source of video stream such as a camera input or a file. In case of camera, use its id (usually 0). In case of a file, use its path.')
    parser.add_argument('frame_duration', type=float, nargs='?', default=0.0, help='A duration of a frame in seconds.')

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    minimal_detection_confidence = 0.5

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1],)
    model = model.to(device)  

    traffic_lights = TrafficLights()
    traffic_lights.start()

    cap = cv2.VideoCapture(args.source)
    while cap.isOpened():
        start_time = time.time()

        frame_returned, frame = cap.read()
        if not frame_returned:  
            break

        predictions = model(frame, verbose=False, conf=minimal_detection_confidence, iou=0.5)
        annotated_frame = predictions[0].plot()
        
        cv2.imshow("Smart Pedestrian Crossing", annotated_frame)

        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time < args.frame_duration:
            time.sleep(args.frame_duration - elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        detected_classes = [ int(detection.cls) for detection in predictions[0].boxes ]

        traffic_lights.update(args.frame_duration,  detected_classes)
        traffic_lights.display()


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
