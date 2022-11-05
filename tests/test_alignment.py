#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试人脸对齐
# python ./tests/test_alignment.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import cv2
import numpy as np
from skimage import transform
from src.utils.ui import *
from src.core.face_detection2 import FaceDetection
from src.core.face_alignment import FaceAlignment
from color_log.clog import log


def main() :

    imgpath = open_window_by_select_one()
    face_detection = FaceDetection()
    face_data = face_detection.handle(imgpath, True)
    X = face_data.fkp6_coords

    face_alignment = FaceAlignment()
    face_alignment.handle(face_data.fkp6_coords)

    print(X)
    Y = [
        [204, 297], # RIGHT_EYE:
        [324, 297], # LEFT_EYE:
        [260, 381], # NOSE_TIP:
        [260, 433], # MOUTH_CENTER:
        [145, 312], # RIGHT_EAR_TRAGION:
        [389, 312]  # LEFT_EAR_TRAGION:
    ]
    
    X, Y = np.array(X), np.array(Y)
    tform = transform.SimilarityTransform()
    # 程序直接估算出转换矩阵M
    tform.estimate(X, Y)
    M = tform.params[0:2, :]
    print(M)

    annotated_frame = face_data.copy_BGR()
    warped = cv2.warpAffine(annotated_frame, M, (512, 512), borderValue=0.0)

    cv2.imshow('annotated_image', warped)              # cv2 显示图片
    cv2.waitKey(0)
    # cv2.imwrite('./data/output/51.png', warped)        # 存储图片



if '__main__' == __name__ :
    main()