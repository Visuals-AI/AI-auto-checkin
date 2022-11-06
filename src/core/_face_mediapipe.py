#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import mediapipe as mp
from pypdm.dbc._sqlite import SqliteDBC
from src.dao.t_face_feature import TFaceFeatureDao
from src.config import SETTINGS


class FaceMediapipe :

    def __init__(self, args,
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        [params] args: main 入参
        [params] model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        [params] static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        [params] min_detection_confidence: 人脸检测模型的最小置信度值
        [params] min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        self.args = args
        self.MAX_NUM_FACES = 1                                      # 检测人脸个数，此场景下只取 1 个人脸
        self.mp_drawing = mp.solutions.drawing_utils                # 导入绘制辅助标记的工具（此为 mediapipe 的，不是 opencv 的）
        self.resize_face = (SETTINGS.face_width, SETTINGS.face_height)
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()

        self.mp_face_detection = mp.solutions.face_detection        # 导入人脸检测模块
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection = model_selection, 
            min_detection_confidence = min_detection_confidence
        )

        self.mp_face_mesh = mp.solutions.face_mesh                  # 导入人脸识别模块
        self.face_mesh = self.mp_face_mesh.FaceMesh(                # 定义一个 mesh 人脸检测器
            static_image_mode = static_image_mode, 
            max_num_faces = self.MAX_NUM_FACES,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )

