#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import os
import cv2
import mediapipe as mp
import numpy as np
import shutil
from src.utils.upload import open_camera, open_select_window
from src.utils.math import c_feature



class RecordFace :

    def __init__(self, 
        model_selection=0, 
        static_image_mode=False, max_num_faces=1, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        :param model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        :param static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        :param max_num_faces: 检测人脸个数
        :param min_detection_confidence: 人脸检测模型的最小置信度值
        :param min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        self.mp_face_detection = mp.solutions.face_detection         # 导入人脸检测模块
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection = model_selection, 
            min_detection_confidence = min_detection_confidence
        )

        self.mp_face_mesh = mp.solutions.face_mesh                   # 导入人脸识别模块
        self.face_mesh = self.mp_face_mesh.FaceMesh(                 # 定义一个 mesh 人脸检测器
            static_image_mode = static_image_mode,         
            max_num_faces = max_num_faces,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )

        self.mp_drawing = mp.solutions.drawing_utils

    
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
        
        for srcpath in imgpaths :
            # 复制图片并重命名到临时目录，避免中文问题
            root_dir, filename = os.path.split(srcpath)
            snkpath = './data/tmp/' + filename
            shutil.copyfile(srcpath, snkpath)
            self._save_features(snkpath)
            os.remove(snkpath)


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
        # self.calculate_features(resize_image)


    def _frame_face(self, image) :
        '''
        识别图像，框取人脸，按统一尺寸裁剪、缩放图像到人脸范围
        :param image: 原始图片对象
        :return: 统一尺寸的人脸图片对象
        '''
        size = image.shape
        w = size[1] #宽度
        h = size[0] #高度
        print(w)
        print(h)

        results = self.face_detection.process(image)
        if not results.detections:
            return
        annotated_image = image.copy()
        for detection in results.detections:
            # print("============")
            # print(detection)
            
            location_data = detection.location_data
            if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
                bb = location_data.relative_bounding_box
                bb_box = [bb.xmin, bb.ymin, bb.width, bb.height]
                print(f"RBBox: {bb_box}")

                left = int(bb.xmin * w)
                upper = int(bb.ymin * h)
                right = int((bb.xmin + bb.width) * w)
                down = int((bb.ymin + bb.height) * h)
                print(left)
                print(upper)
                print(right)
                print(down)
                corp = annotated_image[upper:down, left:right]


                annotated_image = cv2.resize(corp, (512, 512), interpolation=cv2.INTER_CUBIC)
                size = annotated_image.shape
                w = size[1] #宽度
                h = size[0] #高度
                print(w)
                print(h)

            """The enum type of the six face detection key points.
            RIGHT_EYE = 0
            LEFT_EYE = 1
            NOSE_TIP = 2
            MOUTH_CENTER = 3
            RIGHT_EAR_TRAGION = 4
            LEFT_EAR_TRAGION = 5
            """
            # print('Nose tip:')
            # print(self.mp_face_detection.get_key_point(detection, self.mp_face_detection.FaceKeyPoint.NOSE_TIP))
            # Nose tip:
            # x: 0.3519737124443054
            # y: 0.4148605167865753
            # self.mp_drawing.draw_detection(annotated_image, detection)
        cv2.imwrite('./data/tmp/annotated_image.png', annotated_image)
        return image


    def calculate_features(self, image) :
        '''
        计算并保存特征值，建立 特征值 -> 图片名 的关系
        :param image: 统一尺寸的人脸图片对象
        :return: 特征值 -> 图片名
        '''
        results = self.face_mesh.process(image) # 使用process方法对图片进行检测，此方法返回所有的人脸468个点的坐标
        return c_feature(results)

