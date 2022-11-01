#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import cv2
import mediapipe as mp
import numpy as np
import numpy as np
from skimage import transform

def main() :
    # 导入绘图模块
    mp_drawing = mp.solutions.drawing_utils

    # 导入人脸识别模块
    mp_face_mesh = mp.solutions.face_mesh

    # 静态图片: 定义一个人脸检测器与人脸mesh器
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=True,         # False: 视频流; True: 图片
        max_num_faces=1,                # 检测人脸个数
        min_detection_confidence=0.5    # 人脸检测模型的最小置信度值
    )

    # 定义线的粗细，颜色信息
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    drawing_spec1 = mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))


    # 读取图片
    image = cv2.imread('./data/input/10.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到RGB空间

    mp_face_detection = mp.solutions.face_detection        # 导入人脸检测模块
    face_detection = mp_face_detection.FaceDetection(
        model_selection = 0, 
        min_detection_confidence = 0.5
    )
    results = face_detection.process(image)
    detection = results.detections[0]  

    annotated_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR) # 恢复彩色通道
    mp_drawing.draw_detection(annotated_image, detection)

    cv2.imshow('annotated_image', annotated_image)              # cv2 显示图片
    cv2.waitKey(0)
    cv2.imwrite('./data/output/60.png', annotated_image)        # 存储图片


def _get_shape_size(image) :
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


if '__main__' == __name__ :
    main()