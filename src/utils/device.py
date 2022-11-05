#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

import cv2
from src.config import SETTINGS
from src.utils.upload import *
from src.utils.image import *
from color_log.clog import log


EXIT_KEY = 'q'          # 退出 CV 绘制窗口的按键
SAVE_KEY = 's'          # 保存 CV 绘制窗口的按键


def open_camera() :
    imgpath = None
    capture = _init_camera()
    is_open = capture.isOpened()
    if is_open :
        log.info(f'加载摄像头的数据流成功（按 <{EXIT_KEY}> 退出，按 <{SAVE_KEY}> 保存）')
    else :
        log.info('加载摄像头的数据流失败（请确认没有其他程序在读取该数据流）')
        return imgpath

    image_id = gen_file_id()
    imgpath = "%s/%s%s" % (SETTINGS.tmp_dir, image_id, SETTINGS.image_format)
    while is_open:
        is_open, mirror_frame = capture.read()
        if not is_open:
            continue

        bgr_frame = cv2.flip(mirror_frame, 1)   # 镜像翻转画面
        is_exit, is_save = show_frame(bgr_frame, exit_key=EXIT_KEY, save_key=SAVE_KEY)
        if is_exit :
            break
        elif is_save :
            save_frame(bgr_frame, imgpath)
            break
    
    capture.release()
    return imgpath


def _init_camera() :
    log.info(f'正在打开视频设备（索引号={SETTINGS.dev_idx}） ...')
    capture = cv2.VideoCapture(SETTINGS.dev_idx)    # 初始化设备时间较长
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*SETTINGS.fourcc))
    capture.set(cv2.CAP_PROP_FPS, SETTINGS.fps)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, SETTINGS.frame_width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, SETTINGS.frame_height)

    log.info('摄像头输入参数：')
    log.info('  视频编码（fourcc/codec）= %d' % int(capture.get(cv2.CAP_PROP_FOURCC)))
    log.info('  帧速率（FPS）= %d' % int(capture.get(cv2.CAP_PROP_FPS)))
    log.info('  帧宽度（width）= %d' % int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    log.info('  帧高度（height）= %d' % int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    return capture

