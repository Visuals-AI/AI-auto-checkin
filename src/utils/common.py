#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

from src.utils.device import open_camera
from src.utils.ui import open_window_by_select_one
from color_log.clog import log


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
