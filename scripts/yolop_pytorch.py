import torch
import time

# load model
model = torch.hub.load('hustvl/yolop', 'yolop', pretrained=True)

#inference
for _ in range(100):
    img = torch.randn(1,3,640,640)

    start = time.time()
    det_out, da_seg_out,ll_seg_out = model(img)
    stop = time.time()

    print(f"{stop - start}s")
