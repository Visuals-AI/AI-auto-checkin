#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import cv2
import shutil
import numpy as np
from color_log.clog import log
from src.core._face_mediapipe import FaceMediapipe
from src.cache.face_cache import FACE_FEATURE_CACHE
from src.config import SETTINGS


class FaceCompare(FaceMediapipe) :

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
        FaceMediapipe.__init__(self, args, 
            model_selection, static_image_mode, 
            min_detection_confidence, min_tracking_confidence
        )


    def input_face(self) :
        '''
        输入人脸图像，比对特征值
        [params] camera: 输入模式:  True:摄像头; False:上传图片
        [return] 库中相似度最高的图像 ID
        '''
        matched_image_id = ""
        log.info("请%s要匹配的人脸图像 ..." % ("录制" if self.args.camera else "上传"))
        if self.args.camera :
            imgpaths = self._open_camera()
            imgpath = None if not imgpaths else imgpaths[0]
        else :
            imgpath = self._open_select_one_window(title='请选择需要比对的照片')
        if not imgpath :
            log.warn("%s的图像异常 : %s" % (("录制" if self.args.camera else "上传"), imgpath))
            return matched_image_id

        log.info("开始对齐人脸 ...")
        frame_image = self._detecte_face(imgpath)
        if frame_image is None :
            log.warn("未能识别到人脸: [%s]" % imgpath)
            return matched_image_id
        
        log.info("正在计算人脸特征值 ...")
        feature = self.calculate_feature(frame_image)
        if not feature :
            log.warn("计算人脸特征值失败: [%s]" % imgpath)
            return matched_image_id

        log.info("正在比对特征相似度 ...")
        matched_image_id, sim = self._compare(feature)
        if matched_image_id :
            log.info("从特征库匹配人脸成功: ")
            log.info("匹配人脸: %s" % matched_image_id)
            log.info("相似度: %s" % sim)
        else :
            log.warn("从特征库匹配人脸失败")
        return matched_image_id
    

    def _detecte_face(self, imgpath) :
        '''
        识别图片中的人像，保存特征值
        [params] imgpath: 图片路径
        [return] (方框人脸:frame_image, 人脸缓存数据:cache_data)
        '''
        log.info("开始检测图片中的人脸 ...")

        # 预处理上传/录制的图片参数
        name, suffix, image_id = self._gen_image_params(imgpath)
        original_path = "%s/%s%s" % (SETTINGS.tmp_dir, image_id, suffix)
        shutil.copyfile(imgpath, original_path)
        log.info("已接收人脸图片: %s" % original_path)

        # 从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        image = cv2.imread(original_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间
        frame_image = self._to_alignment(image)

        os.remove(original_path)
        return frame_image


    def _compare(self, feature, min_sim=SETTINGS.match_min_sim) :
        '''
        和特征库数据比对，返回相似度最大的图像
        [params] feature: 当前人脸特征值
        [return] (匹配人脸ID:matched_image_id, 匹配相似度:sim)
        '''
        max_sim = 0
        image_id = ""
        for id, lib_feature in FACE_FEATURE_CACHE.id_features.items() :
            sim = self._euclidean_distance(lib_feature, feature)
            if sim >= min_sim and max_sim < sim :
                max_sim = sim
                image_id = id
        return (image_id, max_sim)


    def _euclidean_distance(self, lib_feature, judge_feature) :
        '''
        利用 欧式距离 计算两个特征相似度
        [params] lib_feature: 库存的人脸特征值
        [params] judge_feature: 正在判断的人脸特征值
        [return] 欧式距离（相似度）
        '''
        log.debug("------------------")
        self._log("库存的特征值", lib_feature, debug=True)
        self._log("被判断特征值", judge_feature, debug=True)

        A = np.array(lib_feature)
        B = np.array(judge_feature)
        dist = np.linalg.norm(A - B)    # 欧式距离
        sim = 1.0 / (1.0 + dist)        # 归一化

        log.debug(sim)
        return sim
