#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.163.com/dy/article/GD24HMAN0531PF2O.html
# https://blog.csdn.net/woshicver/article/details/123059410
# pip install mediapipe
# pip install opencv-python

import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils



image_stream_1 = cv2.imread('./input/01.jpg')
image_stream_2 = cv2.imread('./input/02.jpg')


import cv2
import math
import numpy as np

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

def resize_and_show(image):
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    cv2.imshow('win1', img)
 

# 预览图片.
short_range_images = {name: cv2.imread(name) for name in uploaded_short_range.keys()}
for name, image in short_range_images.items():
    print(name)   
    resize_and_show(image)


full_range_images = {name: cv2.imread(name) for name in uploaded_full_range.keys()}
for name, image in full_range_images.items():
    print(name)   
    resize_and_show(image)