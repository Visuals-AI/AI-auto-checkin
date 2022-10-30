#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
import shutil
from color_log.clog import log
from src.bean.t_face_feature import TFaceFeature
from src.core._face_mediapipe import FaceMediapipe
from src.cache.face_cache import FACE_FEATURE_CACHE
from src.config import SETTINGS


class FaceDetection(FaceMediapipe) :

    def __init__(self, args, 
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        :param args: main 入参
        :param model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        :param static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        :param min_detection_confidence: 人脸检测模型的最小置信度值
        :param min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        FaceMediapipe.__init__(self, args, 
            model_selection, static_image_mode, 
            min_detection_confidence, min_tracking_confidence
        )

    
    def input_face(self) :
        '''
        录入人脸图像，计算特征值
        :return: 录入成功的人脸数
        '''
        cnt = 0
        log.info("请%s人脸图像，用于生成特征值 ..." % ("录制" if self.args.camera else "上传"))
        if self.args.camera :
            imgpaths = self._open_camera()
        else :
            imgpaths = self._open_select_multi_window(title='请选择需要录入特征库的照片')
        if not imgpaths :
            log.warn("%s的图像异常 : %s" % (("录制" if self.args.camera else "上传"), imgpath))
            return cnt
        
        for imgpath in imgpaths :
            if not imgpath :
                log.warn("图片异常: [%s]" % imgpath)
                continue

            frame_image, cache_data = self._detecte_face(imgpath)
            if frame_image is None :
                log.warn("未能识别到人脸，请重新录入: [%s]" % imgpath)
                continue
            
            feature = self.calculate_feature(frame_image)
            if not feature :
                log.warn("计算人脸特征值失败: [%s]" % imgpath)
                continue

            else :
                cnt += 1
                self._save_feature(feature, cache_data)
                self._log("已保存特征值", feature)

        log.info("成功录入 [%d/%d] 张人脸数据" % (cnt, len(imgpaths)))
        return cnt
        

    def _detecte_face(self, imgpath) :
        '''
        识别图片中的人像，保存特征值
        :param imgpath: 图片路径
        :return: (方框人脸:frame_image, 人脸缓存数据:cache_data)
        '''
        log.info("开始检测图片中的人脸 ...")

        # 预处理上传/录制的图片参数
        name, suffix, image_id = self._gen_image_params(imgpath)
        original_path = "%s/%s%s" % (SETTINGS.upload_dir, image_id, suffix)
        shutil.copyfile(imgpath, original_path)
        log.info("已接收人脸图片: %s" % original_path)

        # 从图像中检测人脸，并框选裁剪、统一缩放到相同的尺寸
        image = cv2.imread(original_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间
        frame_image = self._to_alignment(image)

        # 保存方框人像数据
        if frame_image is not None :
            feature_path = "%s/%s%s" % (SETTINGS.feature_dir, image_id, SETTINGS.feature_fmt)
            cv2.imwrite(feature_path, frame_image)
            cache_data = self._save_face(name, image_id, original_path, feature_path)
            log.info("检测到人脸位置，已生成特征图片: %s" % feature_path)
        return (frame_image, cache_data)


    def _save_face(self, name, image_id, original_image_path, feature_image_path) :
        '''
        缓存人脸数据
        :param name: 图像名称（默认为文件名）
        :param image_id: 图像 ID（默认自动分配）
        :param original_image_path: 原始上传/录制的图片路径
        :param feature_image_path: 方框检测到、并裁剪缩放后的人脸图片
        :return: TFaceFeature
        '''
        bean = TFaceFeature()
        bean.name = name
        bean.image_id = image_id
        bean.original_image_path = original_image_path
        bean.feature_image_path = feature_image_path
        return bean


    def _save_feature(self, feature, cache_data) :
        '''
        保存人脸数据
        :param feature: 人脸特征值
        :param cache_data: 人脸缓存数据
        :return: 是否保存成功
        '''
        is_ok = True
        try :
            # 添加到数据库
            self.sdbc.conn()
            cache_data.feature = self._feature_to_str(feature)
            self.dao.insert(self.sdbc, cache_data)
            self.sdbc.close()

            # 添加到缓存
            FACE_FEATURE_CACHE.add(cache_data)

        except :
            is_ok = False
            log.error("保存人脸特征数据到数据库失败")
        return is_ok
        
