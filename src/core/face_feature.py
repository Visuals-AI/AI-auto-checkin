#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import dlib
from pypdm.dbc._sqlite import SqliteDBC
from src.dao.t_face_feature import TFaceFeatureDao
from src.utils.image import get_shape_size
from src.utils.common import face_data_to_bean, to_log
from src.cache.face_feature_cache import FACE_FEATURE_CACHE
from src.config import SETTINGS
from color_log.clog import log


class FaceFeature :

    def __init__(self) :
        # 人脸检测模型
        detection_model = '%s/%s' % (SETTINGS.dlib_model_dir, SETTINGS.dlib_detection)
        self.sp = dlib.shape_predictor(detection_model)           

        # 人脸编码模型（提取特征值）
        feature_model = '%s/%s' % (SETTINGS.dlib_model_dir, SETTINGS.dlib_feature)
        self.fr = dlib.face_recognition_model_v1(feature_model)

        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()
    
    
    def handle(self, face_data, is_save=False) :
        '''
        计算人脸特征值
        [params] face_data: 人脸对齐后得到的数据
        [params] is_save: 是否保存人脸特征值
        [return]: 人脸特征值
        '''
        feature = face_data.feature
        if face_data is not None :
            try :
                alignment_frame = face_data.alignment_frame
                feature = self._calculate_feature(alignment_frame)
                face_data.feature = feature
                log.info(to_log("得到人脸特征值", feature))

                if is_save :
                    self._save_feature(face_data)
            except :
                log.error("计算人脸特征值失败")
        return feature


    def _calculate_feature(self, frame) :
        '''
        计算人脸特征值
        [params] frame: 人脸对齐的图像
        [return] 人脸特征值
        '''
        # 把 mediapipe 的地标转为 dlib.rectangle 对象
        x_end, y_end = get_shape_size(frame)
        box = dlib.rectangle(0, 0, x_end, y_end)    # 这里设定计算特征的方框范围，但因为 mediapipe 已经提取过了，所以方框圈了整个图像
        shape = self.sp(frame, box)

        # 输入 dlib 神经网络，计算 128 维人脸特征值（mediapipe 不提供特征值计算方法）
        feature = self.fr.compute_face_descriptor(frame, shape)
        return list(feature)


    def _save_feature(self, face_data) :
        '''
        保存人脸数据
        [params] face_data: 人脸对齐后得到的数据
        [return] 是否保存成功
        '''
        is_ok = True
        try :
            # 写入数据库
            self.sdbc.conn()
            bean = face_data_to_bean(face_data)
            self.dao.insert(self.sdbc, bean)
            self.sdbc.close()

            # 写入缓存
            FACE_FEATURE_CACHE.add(bean)
        except :
            is_ok = False
            log.error("保存人脸特征数据到数据库失败")
        return is_ok
        
