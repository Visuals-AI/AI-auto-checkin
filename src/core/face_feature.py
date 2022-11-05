#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import dlib
import numpy as np
from src.utils.image import *
from color_log.clog import log


class FaceFeature :

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
        # 人脸检测模型
        detection_model = '%s/%s' % (SETTINGS.dlib_model_dir, SETTINGS.dlib_detection)
        self.sp = dlib.shape_predictor(detection_model)           

        # 人脸编码模型（提取特征值）
        feature_model = '%s/%s' % (SETTINGS.dlib_model_dir, SETTINGS.dlib_feature)
        self.fr = dlib.face_recognition_model_v1(feature_model)
    
    
    def handle(self, warped_frame) :
        '''
        计算人脸特征值
        [params] warped_frame: 人脸对齐的图像
        [return]: 人脸特征值
        '''
        # 把 mediapipe 的地标转为 dlib.rectangle 对象
        x_end, y_end = get_shape_size(warped_frame)
        box = dlib.rectangle(0, 0, x_end, y_end)    # 这里设定计算特征的方框范围，但因为 mediapipe 已经提取过了，所以方框圈了整个图像
        shape = self.sp(warped_frame, box)

        # 输入 dlib 神经网络，计算 128 位人脸特征值（mediapipe 不提供特征值计算方法）
        face_feature = self.fr.compute_face_descriptor(warped_frame, shape)
        face_feature_matrix = np.array(face_feature)
        return face_feature_matrix

        