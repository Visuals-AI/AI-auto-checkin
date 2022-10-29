#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
import shutil
from color_log.clog import log
from src.core._face_mediapipe import FaceMediapipe
from src.utils.upload_utils import *
from src.config import SETTINGS



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


    def input_face(self, camera=False) :
        '''
        输入人脸图像，比对特征值
        :param camera: 输入模式:  True:摄像头; False:上传图片
        :return: 库中比对成功的图像
        '''
        log.info("请%s要匹配的人脸图像 ..." % ("录制" if camera else "上传"))
        if camera == True :
            imgpath = open_camera()
        else :
            imgpath = open_select_one_window(title='请选择需要比对的照片')
        
        frame_image = self._detecte_face(imgpath)
        if frame_image is None :
            log.warn("未能识别到人脸: [%s]" % imgpath)
            return
        
        feature = self.calculate_feature(frame_image)
        if not feature :
            log.warn("计算人脸特征值失败: [%s]" % imgpath)
            return

        return
    

    def _detecte_face(self, imgpath) :
        '''
        识别图片中的人像，保存特征值
        :param imgpath: 图片路径
        :return: (方框人脸:frame_image, 人脸缓存数据:cache_data)
        '''
        log.info("开始检测图片中的人脸 ...")

        # 预处理上传/录制的图片参数
        filename = os.path.split(imgpath)[-1]
        name = os.path.splitext(filename)[0]
        suffix = os.path.splitext(filename)[-1]
        image_id = self._gen_image_id()
        original_path = "%s/%s%s" % (SETTINGS.tmp_dir, image_id, suffix)
        shutil.copyfile(imgpath, original_path)
        log.info("已接收人脸图片: %s" % original_path)

        # 从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        image = cv2.imread(original_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间
        frame_image = self._to_box_face(image)

        # 保存方框人像数据
        if frame_image is None :
            feature_path = "%s/%s%s" % (SETTINGS.tmp_dir, image_id, SETTINGS.feature_fmt)
            cv2.imwrite(feature_path, frame_image)
            log.info("检测到人脸位置，已生成特征图片: %s" % feature_path)

        os.remove(original_path)
        os.remove(feature_path)
        return frame_image


    def _compare(self, feature) :
        '''
        和特征库数据比对
        '''
        