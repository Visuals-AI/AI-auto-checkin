#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试人脸对齐
# python ./tests/test_camera.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.utils.device import *
from src.utils.image import *
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试摄像头',
        description='测试摄像头初筛人脸', 
        epilog='\r\n'.join([
            '仅开启摄像头: ', 
            '  python ./tests/test_camera.py', 
            '启用人脸检测模型: ', 
            '  python ./tests/test_camera.py -d', 
            '启用人脸网格模型: ', 
            '  python ./tests/test_camera.py -m', 
        ])
    )
    parser.add_argument('-d', '--detection', dest='detection', action='store_true', default=False, help='启用人脸检测模型')
    parser.add_argument('-m', '--mesh', dest='mesh', action='store_true', default=False, help='启用人脸网格模型')
    return parser.parse_args()


def main(arg) :
    imgpath = open_camera(arg.detection, arg.mesh)
    log.info(imgpath)
    del_image(imgpath)



if '__main__' == __name__ :
    main(args())