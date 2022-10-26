#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.toutiao.com/article/6913754944206258696/?app=news_article&timestamp=1666621808&use_new_style=1&req_id=202210242230080102121621361C58653B&group_id=6913754944206258696&wxshare_count=1&tt_from=weixin&utm_source=weixin&utm_medium=toutiao_android&utm_campaign=client_share&share_token=2903d457-7d99-47f1-bce3-1787abde8660&source=m_redirect&wid=1666629121540

import cv2
import mediapipe as mp
import numpy as np
from src.utils.math import c_feature



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



# 坐标计算欧式距离（n维向量，特征值）
def c_feature(results) :
    # ---- 转换为 (x,y,z) 标准坐标数组 ------
    coords = np.array(results.multi_face_landmarks[0].landmark)
    # print(coords)
    #分别获取关键点XYZ坐标
    points_x = np.array(list(map(get_x, coords)))
    # print(points_x)
    points_y = np.array(list(map(get_y, coords)))
    # print(points_y)
    points_z = np.array(list(map(get_z, coords)))
    # print(points_z)
    #将三个方向坐标合并
    points = np.vstack((points_x, points_y, points_z)).T
    return c_dist(points)


#汇总所有点的XYZ坐标
def get_x(each):
    return each.x

def get_y(each):
    return each.y

def get_z(each):
    return each.z


def c_dist(coord) :
    size = len(coord)
    dist = []
    for i in range(size - 1) :
        a = coord[i]
        b = coord[i + 1]
        d = np.linalg.norm(a - b)
        dist.append(d)

    # a = coord[size - 1]
    # b = coord[0]
    # d = np.linalg.norm(a - b)
    # dist.append(d)
    return np.array(dist)


get_feature()
