import json
import os
from pathlib import Path

import cv2
import numpy as np

Path('input').mkdir(exist_ok=True, parents=True)
Path('ocr_input').mkdir(exist_ok=True, parents=True)
Path('result').mkdir(exist_ok=True, parents=True)

os.system("python eval.py --test_folder input/")
with open('result/res_input_image.txt', 'r') as f:
    detections = f.read()
print(detections)
first_detection = detections.split('\n')[0]
try:
    coords = list(map(int, first_detection.split(',')))
except Exception as e:
    print(e)

x1, y1 = coords[0], coords[1]
x2, y2 = coords[4], coords[5]
print(x1, y1, x2, y2)

img = cv2.imread('input/input_image.jpg')
crop_img = img[y1:y2, x1:x2]
cv2.imwrite('ocr_input/crop_input_image.jpg', crop_img)
os.chdir('deep_text_recognition')
out = os.system("python3 demo.py \
            --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction CTC \
            --image_folder ../ocr_input \
            --saved_model TPS-ResNet-BiLSTM-CTC.pth")

print(out)
os.chdir('..')
with open('result/ocr_results.json') as f:
    ocr_result = json.load(f)

ocr_result['detection'] = coords
os.chdir('result')
os.system("rm -r *")
os.chdir('../ocr_input')
os.system("rm -r *")
os.chdir('../input')
os.system("rm -r *")
print(ocr_result)
