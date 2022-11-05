#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
import numpy as np
from skimage import transform
from src.cache.face_cache import FaceCache
from src.config import SETTINGS
from color_log.clog import log


class FaceAlignment :

    def __init__(self, 
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) :
        '''
        构造函数
        [params] model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        [params] static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        [params] min_detection_confidence: 人脸检测模型的最小置信度值
        [params] min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
    
    
    def handle(self, face_keypoints) :
        '''
        对照标准脸，对输入的人脸进行仿射变换
        [params] face_keypoints: 人脸检测中获取的五官地标（非归一化）
        [return]: None
        '''
        Y = [
            [204, 297], # RIGHT_EYE
            [324, 297], # LEFT_EYE
            [260, 381], # NOSE_TIP
            [260, 433], # MOUTH_CENTER
            [145, 312], # RIGHT_EAR_TRAGION
            [389, 312]  # LEFT_EAR_TRAGION
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

