#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试人脸对齐
# python ./tests/test_video.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.utils.ui import open_window_by_select_one
from src.utils.device import open_camera
from src.utils.image import del_image
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试从视频中检测人脸',
        description='测试从视频中检测人脸', 
        epilog='\r\n'.join([
            '仅读取视频: ', 
            '  python ./tests/test_video.py', 
            '启用人脸检测模型: ', 
            '  python ./tests/test_video.py -d', 
            '启用人脸网格模型: ', 
            '  python ./tests/test_video.py -m', 
        ])
    )
    parser.add_argument('-d', '--detection', dest='detection', action='store_true', default=False, help='启用人脸检测模型')
    parser.add_argument('-m', '--mesh', dest='mesh', action='store_true', default=False, help='启用人脸网格模型')
    return parser.parse_args()


def test(args) :
    video_path = open_window_by_select_one('请选择测试视频')
    imgpath = open_camera(True, args.detection, args.mesh, video_path)
    log.info(imgpath)
    del_image(imgpath)


if '__main__' == __name__ :
    test(args())
