#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试绘制五官关键点地标
# python ./tests/test_camera.py -r -c
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import cv2
import mediapipe as mp
from src.utils.ui import open_window_by_select_one, show_image, save_image
from src.utils.upload import upload
from src.config import SETTINGS


def main() :

    # 导入绘图模块
    mp_drawing = mp.solutions.drawing_utils

    # 导入人脸检测模块
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection = 0, 
        min_detection_confidence = 0.5
    )

    # 上传并读取图片
    imgpath = open_window_by_select_one()
    name, suffix, fileid, tmppath = upload(imgpath)

    bgr_frame = cv2.imread(tmppath)                         # 原图（彩色）
    rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)  # 图片转换到 RGB 空间（反色）
    
    # 人脸检测，得到关键点
    results = face_detection.process(rgb_frame)             # 图像检测
    for detection_id, detection in enumerate(results.detections):   # 枚举从图像中检测到的每一个人脸
        handle(detection, fileid, detection_id)

    os.remove(tmppath)



def handle(detection, fileid, detection_id) :
    location_data = detection.location_data
    if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
        box = location_data.relative_bounding_box   # 得到检测到人脸位置的方框标记（坐标是归一化的）

        # 计算人脸方框的原始坐标
        left = int(box.xmin * width)
        upper = int(box.ymin * height)
        right = int((box.xmin + box.width) * width)
        down = int((box.ymin + box.height) * height)

        for i in range(6):  # 枚举 6 个关键点
            print(f'{mp_face_detection.FaceKeyPoint(i).name}:')
            coord = face_data.relative_keypoints[mp_face_detection.FaceKeyPoint(i).value]
            # xy = coord.split("\n")
            X.append([coord.x * width, coord.y * height])


        # 在原图标注关键点
        annotated_frame = bgr_frame.copy()                      # 复制原图
        mp_drawing.draw_detection(annotated_frame, detection)   # 在原图绘制标注

        # 显示并保存图像
        show_image(annotated_frame)
        save_image(annotated_frame, SETTINGS.detection_dir + "/" + fileid + "-" + detection_id + SETTINGS.feature_fmt)


if '__main__' == __name__ :
    main()
