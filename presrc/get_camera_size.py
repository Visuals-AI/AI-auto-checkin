#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 获取摄像头参数
# python ./presrc/get_camera_size.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
import cv2


def args() :
    parser = argparse.ArgumentParser(
        prog='', # 会被 usage 覆盖
        usage='查询视频设备最大分辨率（用于配置到 settings.yml）',  
        description='视频设备包括： 摄像头、视频采集卡等 ...',  
        epilog='设备索引号可调用 list_camera_index.exe 获得'
    )
    parser.add_argument('-i', '--index', dest='index', type=int, default=0, help='Camera device index')
    return parser.parse_args()


def main(args) :
    capture = cv2.VideoCapture(args.index, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1)

    min_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    min_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)

    max_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    max_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print('视频设备分辨率范围：')
    print('  帧宽度（width）= %d ~ %d' % (min_width, max_width))
    print('  帧高度（height）= %d ~ %d' % (min_height, max_height))
    capture.release()



if __name__ == "__main__" :
    main(args())
