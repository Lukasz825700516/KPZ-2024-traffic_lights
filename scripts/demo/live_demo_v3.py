import sys
import torch
import cv2
import ultralytics
import time
import os

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
    
def print_light(count_down):
    
    os.system("clear")
    if count_down > 0:
        print("\033[32m\u25CF\033[0m", f"Timer: {count_down}")
    else:
        print("\033[31m\u25CF\033[0m", "Time is up!")



def main():
    minimal_detection_confidence = 0.5
    green_light_duration = 15 # in seconds
    time_increment = { # in seconds
        "Elderly" : 9,
        "Child" : 9,
        "Adult" : 0,
        "Wheelchair" : 15,
        "Blind" : 15,
        "Suitcase" : 12,
    }


    input_source, frame_duration = validate_arguments()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1])
    model = model.to(device)  

    count_down = green_light_duration
    classes = ['Elderly', 'Child', 'Adult', 'Wheelchair', 'Blind', 'Suitcase', 'Stroller']
    already_detected = {
        "Elderly" : False,
        "Child" : False,
        "Adult" : False,
        "Wheelchair" : False,
        "Blind" : False,
        "Suitcase" : False,
        "Stroller" : False,
    }

    cap = cv2.VideoCapture(input_source)

    while cap.isOpened():
        start_time = time.time()

        frame_returned, frame = cap.read()
        if not frame_returned:  
            break

        predictions = model(frame, verbose=False)
        annotated_frame = predictions[0].plot()
        cv2.imshow("Smart Pedestrian Crossing", annotated_frame)


        for prediction in predictions[0]:
            if prediction.boxes.conf > minimal_detection_confidence:
                class_name = classes[ int(prediction.boxes.cls) ]

                if not already_detected[ class_name ]:
                    already_detected[ class_name ] = True
                    count_down += time_increment[ class_name ]

                # prediction_confidence = round(prediction[0].cpu().boxes.conf.item(), 3)
                # print(f"Class {class_name}: {prediction_confidence}")



        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time < frame_duration:
            time.sleep(frame_duration - elapsed_time)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        count_down -= frame_duration
        print_light( round(count_down, 0))


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
