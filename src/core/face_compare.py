#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import numpy as np
from color_log.clog import log
from src.utils.common import to_log
from src.cache.face_feature_cache import FACE_FEATURE_CACHE
from src.config import SETTINGS


class FaceCompare :

    def __init__(self) :
        pass


    def handle(self, feature) :
        '''
        匹配人脸特征值
        [params] feature: 要匹配的特征值
        [return]: (匹配人脸ID:matched_face_id, 匹配相似度:sim)
        '''
        matched_face_id = None
        sim = 0
        try :
            matched_face_id, sim = self._compare(feature, SETTINGS.match_min_sim)
            if matched_face_id :
                log.info("人脸匹配成功: ")
                log.info(f"  匹配人脸: {matched_face_id}")
                log.info(f"  相似度: {sim}")
            else :
                log.warn("人脸匹配失败")
        except :
            log.error("人脸匹配异常")
        return (matched_face_id, sim)


    def _compare(self, feature, min_sim) :
        '''
        和特征库数据比对，返回相似度最大的图像
        [params] feature: 当前人脸特征值
        [return] (匹配人脸ID:matched_face_id, 匹配相似度:sim)
        '''
        max_sim = 0
        face_id = ""
        for id, lib_feature in FACE_FEATURE_CACHE.id_features.items() :
            sim = self._euclidean_distance(lib_feature, feature)
            if sim >= min_sim and max_sim < sim :
                max_sim = sim
                face_id = id
        return (face_id, max_sim)


    def _euclidean_distance(self, lib_feature, judge_feature) :
        '''
        利用 欧式距离 计算两个特征相似度
        [params] lib_feature: 库存的人脸特征值
        [params] judge_feature: 正在判断的人脸特征值
        [return] 欧式距离（相似度）
        '''
        log.debug("------------------")
        log.debug(to_log("库存的特征值", lib_feature))
        log.debug(to_log("被判断特征值", judge_feature))

        A = np.array(lib_feature)
        B = np.array(judge_feature)
        dist = np.linalg.norm(A - B)    # 欧式距离
        sim = 1.0 / (1.0 + dist)        # 归一化

        log.debug(f'相似度: {sim}')
        return sim
