#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

from src.bean.t_face_feature import TFaceFeature
from src.utils.device import open_camera
from src.utils.ui import open_window_by_select_one
from pypdm.assist.num import byte_to_str
from src.config import SETTINGS, COORD_SPLIT


def input_face(camera, is_face_detection=True, is_face_mesh=False, title="请选择需要检测的人脸") :
    '''
    输入人脸
    [params] camera: True 摄像头输入; False 图片上传
    [params] is_face_detection: 是否启用人脸检测初筛（仅摄像头模式有效）
    [params] is_face_mesh: 是否启用人脸网格初筛（仅摄像头模式有效）
    [params] title: 窗体标题（仅图片上传模式有效）
    [return] (width, height)
    '''
    imgpath = open_camera(is_face_detection, is_face_mesh) \
                if camera else \
              open_window_by_select_one(title)
    return imgpath


def feature_to_str(feature) :
    '''
    特征值（浮点数组）转 字符串
    [params] feature: 特征值
    [return] 字符串
    '''
    return COORD_SPLIT.join(str(v) for v in feature)


def str_to_feature(s_feature) :
    '''
    字符串 转 特征值（浮点数组）
    [params] s_feature: 特征值字符串
    [return] 特征值（浮点数组）
    '''
    s_feature = byte_to_str(s_feature)
    s_floats = s_feature.split(COORD_SPLIT)
    return list(float(v) for v in s_floats)


def face_data_to_bean(face_data) :
    '''
    把人脸缓存数据转换为数据表的 bean
    [params] face_data: 人脸缓存数据
    [return] 数据表的 bean
    '''
    bean = TFaceFeature()
    bean.name = face_data.name
    bean.image_id = face_data.image_id
    bean.feature = feature_to_str(face_data.feature)
    bean.align_size = SETTINGS.standard_face
    bean.mesh_image_path = face_data.mesh_path
    bean.detection_image_path = face_data.detection_path
    bean.alignment_image_path = face_data.alignment_path
    return bean


def to_log(desc, array) :
    '''
    把列表内容转换为日志格式（若长度 > 2 则省略中间部分）
    [params] desc: 日志描述
    [params] array: 列表
    [return] 日志内容
    '''
    size = len(array)
    msg = f"{desc}: []"
    if size == 1 :
        msg = f"{desc}: [{array[0]}]"
    elif size >= 2 :
        msg = f"{desc}: [{array[0]} ... {array[-1]}]"
    return msg
