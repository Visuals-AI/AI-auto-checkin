#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import cv2
import mediapipe as mp
import numpy as np
from src.utils.upload import open_camera, open_select_window
from src.utils.math import c_feature


class RecordFace :

    def __init__(self, 
        static_image_mode=False, max_num_faces=1, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        :param static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        :param max_num_faces: 检测人脸个数
        :param min_detection_confidence: 人脸检测模型的最小置信度值
        :param min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        mp_face_mesh = mp.solutions.face_mesh       # 导入人脸识别模块
        self.face_mesh = mp_face_mesh.FaceMesh(     # 定义一个 mesh 人脸检测器
            static_image_mode = static_image_mode,         
            max_num_faces = max_num_faces,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )

    
    def input_face(self, camera=False) :
        '''
        录入人脸图片，计算特征值
        :param camera: 录入模式:  True:摄像头; False:上传图片
        :return: 是否录入成功
        '''
        if camera == True :
            imgpaths = open_camera()
        else :
            imgpaths = open_select_window(title='请选择个人特征照片')
        
        for imgpath in imgpaths :
            self._save_features(imgpath)


    def _save_features(self, imgpath) :
        '''
        识别图片中的人像，保存特征值
        :param imgpath: 图片路径
        :return: 
        '''
        # 识别图像，框取人脸
        # 裁剪、缩放图像，按一致大小保留人脸图片
        # 重新识别图像，计算特征值 -> 图片名 关系
        image = cv2.imread(imgpath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间
        resize_image = self._frame_face(image)
        self.calculate_features(resize_image)


    def _frame_face(self, image) :
        '''
        识别图像，框取人脸，按统一尺寸裁剪、缩放图像到人脸范围
        :param image: 原始图片对象
        :return: 统一尺寸的人脸图片对象
        '''
        results = self.face_mesh.process(image)      # 使用process方法对图片进行检测，此方法返回所有的人脸468个点的坐标
        # TODO
        return image


    def calculate_features(self, image) :
        '''
        计算并保存特征值，建立 特征值 -> 图片名 的关系
        :param image: 统一尺寸的人脸图片对象
        :return: 特征值 -> 图片名
        '''
        results = self.face_mesh.process(image)
        return c_feature(results)

