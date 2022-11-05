#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试人脸对齐
# python ./tests/test_alignment.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

from src.utils.ui import *
from src.utils.image import *
from src.cache.face_cache import FACE_CACHE
from src.core.face_detection2 import FaceDetection
from src.core.face_alignment import FaceAlignment
from color_log.clog import log


def main() :
    FACE_CACHE.load()

    imgpath = open_window_by_select_one()
    face_detection = FaceDetection()
    face_data = face_detection.handle(imgpath, True)

    face_alignment = FaceAlignment()
    face_alignment.handle(face_data)


if '__main__' == __name__ :
    main()