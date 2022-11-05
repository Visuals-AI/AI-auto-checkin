#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试绘制人脸关键点-6 地标
# python ./tests/test_detection.py [-c]
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.utils.device import *
from src.utils.ui import *
from src.cache.face_cache import FACE_CACHE
from src.core.face_detection import FaceDetection
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试绘制人脸关键点-6 地标',
        description='测试绘制人脸五官关键点（共 6 个）地标', 
        epilog='\r\n'.join([
            '摄像头拍摄: ', 
            '  python ./tests/test_detection.py -c', 
            '上传人脸图片: ', 
            '  python ./tests/test_detection.py', 
        ])
    )
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    return parser.parse_args()


def main(arg) :
    FACE_CACHE.load()
    if arg.camera :
        imgpath = open_camera()
    else :
        imgpath = open_window_by_select_one(title="请选择需要检测的人脸")

    face_detection = FaceDetection()
    face_data = face_detection.handle(imgpath, True)
    log.info(face_data)


if '__main__' == __name__ :
    main(args())

