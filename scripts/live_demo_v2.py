import sys

import torch
import cv2
import ultralytics
import time

def main():
    if not len(sys.argv) == 3:
        print("missing arguments: <weights> <source>")
        exit()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1])
    model = model.to(device)
    
    if (sys.argv[2] == "0"):
        cap = cv2.VideoCapture(0) # 0 - camera / PATH to source
    else:
        cap = cv2.VideoCapture(sys.argv[2])
    
    
    prev_frame_time = 0
    new_frame_time = 0
  
    while cap.isOpened():
        res, frame = cap.read()
        results = model(frame)
        annotated_frame = results[0].plot()
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
        new_frame_time = time.time() 
    
        # Calculating the fps 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 
        fps = int(fps) 
        fps = str(fps) 
        cv2.putText(annotated_frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 
        
        if res:
            cv2.imshow("DEMO", annotated_frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        # time.sleep(0.05)
        
if __name__ == "__main__":
    main()
