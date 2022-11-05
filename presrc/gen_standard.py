#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 预生成标准脸的五官坐标
# python ./presrc/gen_standard.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.utils.ui import *
from src.core.face_detection2 import FaceDetection
from src.config import SETTINGS, CHARSET, COORD_SPLIT
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='预生成标准脸的五官坐标',
        description='提前生成标准脸坐标，用于人脸对齐', 
        epilog='\r\n'.join([
            '摄像头拍摄: ', 
            '  python ./presrc/gen_standard.py -c', 
            '上传人脸图片: ', 
            '  python ./presrc/gen_standard.py', 
        ])
    )
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    return parser.parse_args()


def main(arg) :
    if arg.camera :
        pass    # FIXME
    else :
        imgpath = open_window_by_select_one(title="请选择已 PS 完成的标准脸")

    face_detection = FaceDetection()
    face_data = face_detection.handle(imgpath, True)

    width = face_data.width
    height = face_data.height
    coords = face_data.fkp6_coords
    data = KEY_POINTS_TPL % {
        'imgpath': imgpath, 'split': COORD_SPLIT, 
        'width': width, 'height': height, 
        're_x':  coords[0][0], 're_y':  coords[0][1], 
        'le_x':  coords[1][0], 'le_y':  coords[1][1], 
        'nt_x':  coords[2][0], 'nt_y':  coords[2][1], 
        'mc_x':  coords[3][0], 'mc_y':  coords[3][1], 
        'ret_x': coords[4][0], 'ret_y': coords[4][1], 
        'let_x': coords[5][0], 'let_y': coords[5][1], 
    }

    filename = '%sx%s' % (width, height)
    savepath = '%s/%s' % (SETTINGS.standard_dir, filename)

    with open(savepath, 'w+', encoding=CHARSET) as file :
        file.write(data)
    log.info("生成标准脸尺寸成功")
    log.info("  人脸来源: %s" % imgpath)
    log.info("  人脸地标: %s" % savepath)



KEY_POINTS_TPL = '''# --------------------------------------
# src image : %(imgpath)s
# image size: %(width)s x %(height)s
# --------------------------------------

# RIGHT_EYE
%(re_x)s%(split)s%(re_y)s

# LEFT_EYE
%(le_x)s%(split)s%(le_y)s

# NOSE_TIP
%(nt_x)s%(split)s%(nt_y)s

# MOUTH_CENTER
%(mc_x)s%(split)s%(mc_y)s

# RIGHT_EAR_TRAGION
%(ret_x)s%(split)s%(ret_y)s

# LEFT_EAR_TRAGION
%(let_x)s%(split)s%(let_y)s
'''



if '__main__' == __name__ :
    main(args())

