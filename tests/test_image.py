#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import cv2
import mediapipe as mp
import numpy as np


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
    image = cv2.imread('./data/tmp/09.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到RGB空间
    results = face_mesh.process(image)      # 使用process方法对图片进行检测，此方法返回所有的人脸468个点的坐标

    annotated_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)

    # 遍历所有人，当 max_num_faces == 1 时，只有 1 组 face_landmarks
    for face_landmarks in results.multi_face_landmarks:

        # 每个 face_landmarks 有 468 个特征点，利用其进行人脸mesh的绘制
        # print('face_landmarks:', face_landmarks)
        mp_drawing.draw_landmarks(
            image=annotated_image,                              # 需要画图的原始图片
            landmark_list=face_landmarks,                       # 检测到的人脸坐标
            connections=mp_face_mesh.FACEMESH_TESSELATION,      # 连接线绘制完全网格，需要把那些坐标连接起来
            # connections=mp_face_mesh.FACEMESH_CONTOURS,       # 仅连接外围边框，内部点不连接
            landmark_drawing_spec=drawing_spec,                 # 坐标的颜色，粗细
            connection_drawing_spec=drawing_spec1               # 连接线的粗细，颜色等
        )

    cv2.imshow('annotated_image', annotated_image)              # cv2 显示图片
    cv2.waitKey(0)
    cv2.imwrite('./data/output/09.png', annotated_image)        # 存储图片
    face_mesh.close()



if '__main__' == __name__ :
    main()