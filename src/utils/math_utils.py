#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import numpy as np

SPLIT = ", "


def feature_to_str(feature) :
    return SPLIT.join(str(v) for v in feature)


def str_to_feature(s_feature) :
    s_floats = s_feature.split(SPLIT)
    return list(complex(v) for v in s_floats)


def c_feature(results) :
    '''
    坐标计算欧式距离
    :param results: mediapipe 计算得到的图片特征点坐标
    :return: 这组坐标的特征向量（一组欧氏距离）
    '''
    coords = to_coords(results.multi_face_landmarks[0].landmark)
    return _feature(coords)


def to_coords(landmark) :
    '''
    转换为 (x,y,z) 标准坐标数组
    '''
    points = np.array(landmark)

    # 分别获取关键点XYZ坐标
    points_x = np.array(list(map(get_x, points)))
    points_y = np.array(list(map(get_y, points)))
    points_z = np.array(list(map(get_z, points)))

    # 将三个方向坐标合并
    coords = np.vstack((points_x, points_y, points_z)).T
    return coords


#汇总所有点的XYZ坐标
def get_x(each):
    return each.x

def get_y(each):
    return each.y

def get_z(each):
    return each.z


def _feature(coord) :
    size = len(coord)
    dist = []
    for i in range(size - 1) :
        a = coord[i]
        b = coord[i + 1]
        d = np.linalg.norm(a - b)
        dist.append(d)

    a = coord[size - 1]
    b = coord[0]
    d = np.linalg.norm(a - b)
    dist.append(d)
    return np.array(dist)