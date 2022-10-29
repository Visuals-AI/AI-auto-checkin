#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

from src.core._face_mediapipe import FaceMediapipe
from src.utils.upload_utils import *


class FaceCompare(FaceMediapipe) :

    def __init__(self, 
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        :param model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        :param static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        :param min_detection_confidence: 人脸检测模型的最小置信度值
        :param min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        FaceMediapipe.__init__(self, 
            model_selection, static_image_mode, 
            min_detection_confidence, min_tracking_confidence
        )

    