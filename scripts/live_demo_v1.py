import sys

import torch
import ultralytics

def main():
    if not len(sys.argv) > 1:
        print("missing arguments weights")
        exit()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = ultralytics.YOLO(sys.argv[1])
    model = model.to(device)
    
    if (sys.argv[2] == "0"):
        source_in = 0
    else:
        source_in = sys.argv[2]
        
    while True:
        results = model(source=source_in, show=True)

if __name__ == "__main__":
    main()
