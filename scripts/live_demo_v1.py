import sys

import torch
import ultralytics
import time

def main():
    count_frames = 0
    
    label_avg_dict = {
        0 : 0.0,
        1 : 0.0,
        2 : 0.0,
        3 : 0.0,
        4 : 0.0,
        5 : 0.0,
        6 : 0.0
    }
    
    label_count_dict = {
        0 : 0,
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0
    }
    
    if not len(sys.argv) >= 3:
        print("missing arguments: <weights> <source> <delay>=0.0")
        exit()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1])
    model = model.to(device)
    
    if (sys.argv[2] == "0"):
        source_in = 0
    else:
        source_in = sys.argv[2]
    
    delay = 0.0
    
    if len(sys.argv) == 4:
        delay = float(sys.argv[3])
    
    while True:
        results = model(source=source_in, show=True)
        
        # Count average to light green light
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for i in range (len(boxes.cls)):
                label_avg_dict[int(boxes.cls[i])] += boxes.conf[i]
                label_count_dict[int(boxes.cls[i])] += 1

        if count_frames <= 10:
            count_frames += 1
        else:
            for i in range (len(label_avg_dict)):
                if label_count_dict[i]:
                    label_avg_dict[i] /= label_count_dict[i]
                if label_avg_dict[i] > 0.6:
                    print("GREEN LIGHT FOR LABEL: " + str(i))
                label_count_dict[i] = 0
                label_avg_dict[i] = 0.0
                
        time.sleep(delay)

if __name__ == "__main__":
    main()
