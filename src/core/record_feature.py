#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import cv2
import mediapipe as mp
import numpy as np
from src.utils.math import c_feature



class RecordFace :

    def __init__(self) -> None:
        pass




def get_feature() :

    # 导入人脸识别模块
    mp_face_mesh = mp.solutions.face_mesh

    # 静态图片: 定义一个人脸检测器与人脸mesh器
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,         # False: 视频流; True: 图片
        max_num_faces=1,                # 检测人脸个数
        min_detection_confidence=0.5    # 人脸检测模型的最小置信度值
    )


    # 读取图片
    image = cv2.imread('./data/input/03.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到RGB空间
    results = face_mesh.process(image)      # 使用process方法对图片进行检测，此方法返回所有的人脸468个点的坐标
    return c_feature(results)


get_feature()
