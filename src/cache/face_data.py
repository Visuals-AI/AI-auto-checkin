#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------


class FaceData :

    def __init__(self) -> None:
        self.name = None                            # 图像文件名
        self.image_id = None                        # 分配的图像 ID
        self.imgpath = None                         # 加工后的图片存储位置
        self.annotated_frame = None                 # 标注人脸地标的图像数据
        self.frame = None                           # 原始图像数据
        self.width = 0                              # 图像宽度
        self.height = 0                             # 图像高度
        self.normalized_box_coords = []             # 人脸边界框地标（归一化坐标）
        self.normalized_face_keypoints_coords = []  # 人脸关键点地标（归一化坐标）
        self.box_coords = []                        # 人脸边界框地标（原始比例坐标）
        self.face_keypoints_coords = []             # 人脸关键点地标（原始比例坐标）
        