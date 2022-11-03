#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试 ADB 指令
# python ./tests/test_camera.py -r -c
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.core.face_detection import FaceDetection


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试摄像头录制',
        description='', 
        epilog='\r\n'.join([
            '示例: ', 
            'python ./tests/test_camera.py -r -c'
        ])
    )
    parser.add_argument('-r', '--record', dest='record', action='store_true', default=False, help='录入模式: 用于录入人脸特征点; 默认为匹配模式')
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    return parser.parse_args()


def test(args) :
    fd = FaceDetection(args)
    fd.input_face()


if '__main__' == __name__ :
    test(args())
