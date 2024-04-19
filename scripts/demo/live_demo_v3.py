import sys
import os
import torch
import cv2
import ultralytics
import time
from TrafficLights import TrafficLights

def validate_arguments():
    if len(sys.argv) < 3:
        print("missing arguments: <weights> <source> <delay>=0.0s")
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f"File {sys.argv[1]} not found")
        exit(1)

    input_source = sys.argv[2]
    if input_source.isdigit():
        input_source = int(input_source)

    delay = 0.0
    if len(sys.argv) == 4:
        delay = float(sys.argv[3])

    return input_source, delay

def main():
    minimal_detection_confidence = 0.5

    input_source, frame_duration = validate_arguments()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1],)
    model = model.to(device)  

    traffic_lights = TrafficLights()
    traffic_lights.start()

    cap = cv2.VideoCapture(input_source)
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

        if elapsed_time < frame_duration:
            time.sleep(frame_duration - elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        detected_classes = [ int(detection.cls) for detection in predictions[0].boxes ]

        traffic_lights.update(frame_duration,  detected_classes)
        traffic_lights.display()


    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
