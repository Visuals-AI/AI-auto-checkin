#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
from src.utils.image import *
from src.cache.face_cache import FACE_CACHE
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
        pass
    
    
    def handle(self, face_data) :
        '''
        对照标准脸，对输入的人脸进行仿射变换
        [params] face_data: 人脸检测得到的数据
        [return]: 人脸对齐后的图像
        '''
        warped_frame = None
        if face_data :
            try :
                face_keypoints = face_data.fkp6_coords
                trans_matrix = gen_trans_matrix(        # 计算转换矩阵
                    face_keypoints, 
                    FACE_CACHE.standard_fkp_coords
                )
                warped_frame = self._face_alignment(face_data, trans_matrix)
            except :
                log.error("人脸对齐模型异常")
        return warped_frame
        

    def _face_alignment(self, face_data, trans_matrix) :
        '''
        人脸图像仿射变换
        [params] face_data: 人脸检测得到的数据
        [params] trans_matrix: 转换矩阵
        [return]: 人脸对齐后的图像
        '''
        bgr_frame = face_data.copy_BGR()
        warped_frame = cv2.warpAffine(
            bgr_frame, 
            trans_matrix, 
            SETTINGS.alignment_resize, 
            borderValue = 0.0
        )

        # 显示变换后的图像
        if SETTINGS.show_image :
            show_frame(warped_frame)

        # 保存图像
        savepath = '%s/%s%s' % (SETTINGS.alignment_dir, face_data.image_id, SETTINGS.image_format)
        save_image(warped_frame, savepath)

        face_data.alignment_frame = warped_frame
        face_data.alignment_path = savepath
        return warped_frame

