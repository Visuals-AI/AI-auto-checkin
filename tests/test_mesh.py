#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试绘制人脸网格关键点-468 地标
# python ./tests/test_mesh.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

from src.utils.ui import *
from src.core.face_mesh import FaceMesh
from color_log.clog import log

def main() :
    imgpath = open_window_by_select_one()
    face_mesh = FaceMesh()
    face_data = face_mesh.handle(imgpath, True)
    log.info(face_data)


if '__main__' == __name__ :
    main()
