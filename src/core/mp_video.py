#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# 绘制网格 ：https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540
# 绘制方框 ：https://blog.csdn.net/dgvv4/article/details/122054388

import cv2
import mediapipe as mp

# 导入绘图模块
mp_drawing = mp.solutions.drawing_utils

# 导入人脸识别模块
mp_face_mesh = mp.solutions.face_mesh

# 自定义人脸识别方法
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,        # False: 视频流; True: 图片
    max_num_faces=1,                # 检测人脸个数
    min_detection_confidence=0.5,   # 人脸检测模型的最小置信度值
    min_tracking_confidence=0.5     # 跟踪模型的最小置信度值（仅视频流有效）
)

# 定义线的粗细，颜色信息
drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
drawing_spec1 = mp_drawing.DrawingSpec(thickness=2, circle_radius=1,color=(255,255,255))

# 导入视频
# filepath = 'C:\\GameDownload\\Deep Learning\\face.mp4'
# cap = cv2.VideoCapture(filepath)

# 开启摄像头
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # if results.multi_face_landmarks:
    #     for face_landmarks in results.multi_face_landmarks:
    #         mp_drawing.draw_landmarks(
    #             image=image,
    #             landmark_list=face_landmarks,
    #             connections=mp_face_mesh.FACEMESH_TESSELATION,      # 连接线绘制完全网格，需要把那些坐标连接起来
    #             # connections=mp_face_mesh.FACEMESH_CONTOURS,       # 仅连接外围边框，内部点不连接
    #             landmark_drawing_spec=drawing_spec,
    #             connection_drawing_spec=drawing_spec1
    #         )
    cv2.imshow('Mediapipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
face_mesh.close()
cap.release()
