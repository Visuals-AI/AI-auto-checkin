#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 清除所有照片
# python ./presrc/clean_images.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

from src.utils.image import *
from src.config import SETTINGS
from color_log.clog import log


def main() :
    dirs = [
        SETTINGS.tmp_dir, 
        SETTINGS.mesh_dir, 
        SETTINGS.detection_dir, 
        SETTINGS.alignment_dir
    ]

    for dir in dirs :
        log.info(f"清理目录图片: {dir}")
        del_images(dir)
    log.info("清理完成")


def del_images(imgdir) :
    files = os.listdir(imgdir)
    for filename in files :
        if filename.endswith(".md") or filename.endswith(".keep") :
            continue
        imgpath = f"{imgdir}/{filename}"
        del_image(imgpath)


if __name__ == "__main__" :
    main()
