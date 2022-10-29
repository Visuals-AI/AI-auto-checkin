#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import os
import cv2
import mediapipe as mp
import numpy as np
import shutil
import uuid
from color_log.clog import log
from pypdm.dbc._sqlite import SqliteDBC
from src.bean.t_face_feature import TFaceFeature
from src.dao.t_face_feature import TFaceFeatureDao
from src.utils.upload_utils import *
from src.utils.image_utils import *
from src.utils.math_utils import c_feature
from src.config import SETTINGS


class RecordFace :

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
        self.MAX_NUM_FACES = 1                                      # 检测人脸个数，此场景下只取 1 个人脸
        self.mp_drawing = mp.solutions.drawing_utils                # 导入绘制辅助标记的工具（此为 mediapipe 的，不是 opencv 的）
        self.resize_face = (SETTINGS.face_width, SETTINGS.face_height)

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
            image_id, frame_image = self._detecte_face(imgpath)
            if frame_image is None :
                log.error("未能识别到人脸: [%s]" % imgpath)
                continue

            
            # self.calculate_features(frame_image)


    def _detecte_face(self, imgpath) :
        '''
        识别图片中的人像，保存特征值
        :param imgpath: 图片路径
        :return: (图像唯一ID:image_id, 方框人脸:frame_image)
        '''
        # 预处理上传/录制的图片参数
        filename = os.path.split(imgpath)[-1]
        name = os.path.splitext(filename)[0]
        suffix = os.path.splitext(filename)[-1]
        image_id = uuid.uuid1().hex     # 随机分配图像 ID
        original_path = "%s/%s%s" % (SETTINGS.upload_dir, image_id, suffix)
        shutil.copyfile(imgpath, original_path)

        # 从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        image = cv2.imread(original_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间
        frame_image = self._frame_face(image)

        # 保存方框人像数据
        feature_path = "%s/%s%s" % (SETTINGS.feature_dir, image_id, SETTINGS.feature_fmt)
        cv2.imwrite(feature_path, frame_image)
        self._save_face(name, image_id, original_path, feature_path)
        return (image_id, frame_image)
        


    def _frame_face(self, image) :
        '''
        从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        :param image: 原始图像
        :return: frame_image 统一尺寸的人脸图像; 若检测失败返回 None
        '''
        frame_image = None
        results = self.face_detection.process(image)
        if not results.detections:
            return frame_image

        detection = results.detections[0]   # 此场景下只取 1 个人脸
        location_data = detection.location_data
        if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
            box = location_data.relative_bounding_box   # 得到检测到人脸位置的方框标记（位置是归一化的）
            width, height = get_shape_size(image)         # 原图的宽高

            # 计算人脸方框的原始坐标
            left = int(box.xmin * width)
            upper = int(box.ymin * height)
            right = int((box.xmin + box.width) * width)
            down = int((box.ymin + box.height) * height)

            corp_image = image[upper:down, left:right]  # 裁剪图像，仅保留方框人脸部分
            frame_image = cv2.resize(corp_image, 
                self.resize_face, 
                interpolation=cv2.INTER_CUBIC
            )

        # 绘制检测到的人脸方框
        if SETTINGS.debug :
            annotated_image = image.copy()
            self.mp_drawing.draw_detection(annotated_image, detection)
            cv2.imshow('Preview Frame Face', annotated_image)
            cv2.waitKey(0)
        return frame_image


    def _save_face(self, name, image_id, original_image_path, feature_image_path) :
        '''
        保存人脸数据
        :param name: 图像名称（默认为文件名）
        :param image_id: 图像 ID（默认自动分配）
        :param original_image_path: 原始上传/录制的图片路径
        :param feature_image_path: 方框检测到、并裁剪缩放后的人脸图片
        :return: None
        '''
        sdbc = SqliteDBC(options=SETTINGS.database)
        sdbc.conn()
        dao = TFaceFeatureDao()
        
        bean = TFaceFeature()
        bean.name = name
        bean.image_id = image_id
        bean.original_image_path = original_image_path
        bean.feature_image_path = feature_image_path

        dao.insert(sdbc, bean)
        sdbc.close()


    def calculate_features(self, image) :
        '''
        计算并保存特征值，建立 特征值 -> 图片名 的关系
        :param image: 统一尺寸的人脸图片对象
        :return: 特征值 -> 图片名
        '''
        results = self.face_mesh.process(image) # 使用process方法对图片进行检测，此方法返回所有的人脸468个点的坐标
        return c_feature(results)

