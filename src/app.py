#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

from src.core.face_detection import FaceDetection
from src.core.face_alignment import FaceAlignment
from src.core.face_feature import FaceFeature
from src.core.face_compare import FaceCompare
from src.utils.common import input_face


def record_face_feature(args, show_video=True, save_feature=False) :
    '''
    录入人脸并计算特征值
    [params] args: main 入参
    [params] show_video: 是否在前台实时显示摄像头画面
    [params] save_feature: 是否保存特征值
    [return] 人脸特征值
    '''
    imgpath = input_face(args.camera, show_video)

    face_detection = FaceDetection()
    face_data = face_detection.handle(imgpath, True)

    face_alignment = FaceAlignment()
    face_alignment.handle(face_data)

    face_feature = FaceFeature()
    feature = face_feature.handle(face_data, save_feature)
    return feature


def match_face_feature(feature) :
    '''
    匹配人脸特征值
    [params] feature: 人脸特征值
    [return] image_id 与库中匹配度最高的人脸 ID
    '''
    matched_face_id = None
    if feature is not None :
        face_compare = FaceCompare()
        matched_face_id, sim = face_compare.handle(feature)
    return matched_face_id

