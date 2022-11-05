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
    image = cv2.imread('./data/input/08.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 图片转换到RGB空间

    mp_face_detection = mp.solutions.face_detection        # 导入人脸检测模块
    face_detection = mp_face_detection.FaceDetection(
        model_selection = 0, 
        min_detection_confidence = 0.5
    )
    results = face_detection.process(image)
    detection = results.detections[0]  

    # for detection in results.detections:
    #     """The enum type of the six face detection key points.
    #     RIGHT_EYE = 0
    #     LEFT_EYE = 1
    #     NOSE_TIP = 2
    #     MOUTH_CENTER = 3
    #     RIGHT_EAR_TRAGION = 4
    #     LEFT_EAR_TRAGION = 5
    #     """
    #     print(mp_face_detection.FaceKeyPoint.NOSE_TIP)
    #     print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
    #     # Nose tip:
    #     # x: 0.3519737124443054
    #     # y: 0.4148605167865753

    width, height = _get_shape_size(image) # 原图的宽高
    location_data = detection.location_data
    if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
        box = location_data.relative_bounding_box   # 得到检测到人脸位置的方框标记（坐标是归一化的）

        # 计算人脸方框的原始坐标
        left = int(box.xmin * width)
        upper = int(box.ymin * height)
        right = int((box.xmin + box.width) * width)
        down = int((box.ymin + box.height) * height)


    X = []
    for face_no, face in enumerate(results.detections):
        face_data = face.location_data
        for i in range(6):
            print(f'{mp_face_detection.FaceKeyPoint(i).name}:')
            coord = face_data.relative_keypoints[mp_face_detection.FaceKeyPoint(i).value]
            # xy = coord.split("\n")
            X.append([coord.x * width, coord.y * height])
    print(X)
    Y = [
        [204, 297], # RIGHT_EYE:
        [324, 297], # LEFT_EYE:
        [260, 381], # NOSE_TIP:
        [260, 433], # MOUTH_CENTER:
        [145, 312], # RIGHT_EAR_TRAGION:
        [389, 312]  # LEFT_EAR_TRAGION:
    ]
    
    X, Y = np.array(X), np.array(Y)
    tform = transform.SimilarityTransform()
    # 程序直接估算出转换矩阵M
    tform.estimate(X, Y)
    M = tform.params[0:2, :]
    print(M)

    annotated_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR)
    warped = cv2.warpAffine(annotated_image, M, (512, 512), borderValue=0.0)

    cv2.imshow('annotated_image', warped)              # cv2 显示图片
    cv2.waitKey(0)
    cv2.imwrite('./data/output/51.png', warped)        # 存储图片


def _get_shape_size(image) :
    '''
    获取图像的宽高
    [params] image: CV 载入的图像
    [return] (width, height)
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