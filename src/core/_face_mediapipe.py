#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import uuid
import cv2
import mediapipe as mp
import numpy as np
from color_log.clog import log
from pypdm.dbc._sqlite import SqliteDBC
from src.dao.t_face_feature import TFaceFeatureDao
from src.utils.upload_utils import *
from src.config import SETTINGS, FEATURE_SPLIT


class FaceMediapipe :

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


    def _gen_image_id(self) :
        '''
        生成图像的唯一 ID
        :return: 图像 ID
        '''
        return uuid.uuid1().hex

    
    def _to_box_face(self, image) :
        '''
        从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        :param image: 原始图像
        :return: frame_image 统一尺寸的人脸图像; 若检测失败返回 None
        '''
        frame_image = None
        results = self.face_detection.process(image)
        if not results.detections:
            log.warn("检测人脸位置失败")
            return frame_image

        detection = results.detections[0]               # 此场景下只取 1 张人脸
        location_data = detection.location_data
        if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
            box = location_data.relative_bounding_box   # 得到检测到人脸位置的方框标记（坐标是归一化的）
            width, height = self._get_shape_size(image)       # 原图的宽高

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


    def _get_shape_size(self, image) :
        '''
        获取图像的宽高
        :param image: CV 载入的图像
        :return: (width, height)
        '''
        height = 0
        width = 0
        if image is not None :
            size = image.shape
            height = size[0]
            width = size[1]
        return (width, height)


    def calculate_feature(self, image) :
        '''
        计算人脸特征值
        :param image: 统一尺寸的人脸图片对象
        :return: 特征值
        '''
        feature = []
        log.info("开始计算人脸特征值 ...")

        # 使用 face_mesh 计算人脸 468 个点的三维地标（坐标是归一化的）
        results = self.face_mesh.process(image)
        if not results.multi_face_landmarks:
            log.warn("拟合人脸网格失败")
            return feature

        coords = self._to_coords(results.multi_face_landmarks[0].landmark)
        feature = self._to_feature(coords)
        return feature


    def _to_coords(self, landmark) :
        '''
        把 人脸特征点的地标 转换为 (x,y,z) 坐标数组
        :param landmark: 人脸特征点的地标
        :return: (x,y,z) 坐标数组（归一化）
        '''
        points = np.array(landmark)

        # 分别获取特征点 (x,y,z) 坐标
        points_x = np.array(list(p.x for p in points))
        points_y = np.array(list(p.y for p in points))
        points_z = np.array(list(p.z for p in points))

        # 将三个方向坐标合并
        coords = np.vstack((points_x, points_y, points_z)).T
        return coords


    def _to_feature(self, coords) :
        '''
        计算 坐标数组 的 特征值
        :param coords: (x,y,z) 坐标数组（归一化）
        :return: 特征值
        '''
        feature = []
        size = len(coords)
        group_num = size / 3                        # 每 3 个坐标一组，分别组成方阵
        groups = np.array_split(coords, group_num)
        for group in groups :                       # 迭代每组方阵
            eigen, vector = np.linalg.eig(group)    # 计算 特征值(1x3矩阵) 和 特征向量(3x3矩阵)
            feature.extend(eigen)                   # 串接 特征值
        return feature


    def _feature_to_str(self, feature) :
        '''
        特征值（复数数组）转 字符串
        :param feature: 特征值
        :return: 字符串
        '''
        return FEATURE_SPLIT.join(str(v) for v in feature)

