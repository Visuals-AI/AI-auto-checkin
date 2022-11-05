#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

import os
import enum
import cv2
import numpy as np
from src.config import SETTINGS
from color_log.clog import log

from skimage import transform
TRANS_FORM = transform.SimilarityTransform()


# 定义图像上标记的颜色
class LabelColor(enum.auto):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


def get_shape_size(frame) :
    '''
    获取图像的宽高
    [params] frame: CV 载入的图像
    [return] (width, height)
    '''
    height = 0
    width = 0
    if frame is not None :
        size = frame.shape
        height = size[0]    
        width = size[1]
        # channel = size[2]   # 通道数
    return (width, height)


def gen_trans_matrix(from_matrix, to_matrix) :
    '''
    生成从 源矩阵 到 目标矩阵 的仿射变换矩阵
    [params] from_matrix: 源矩阵
    [params] to_matrix: 目标矩阵
    [return] 仿射变换矩阵
    '''
    fm = np.array(from_matrix)
    tm = np.array(to_matrix)
    TRANS_FORM.estimate(fm, tm)
    trans_matrix = TRANS_FORM.params[0:2, :]
    return trans_matrix


def show_image(image, exit_key='q', title='Preview Image') :
    '''
    绘制图像
    （此方法不能用于视频流中绘制帧，因为判断按键时会强制卡死在同一帧）
    [params] image: 要绘制的图像
    [params] exit_key: 退出绘制的按键（默认为 'q'）
    [params] title: 显示窗体的标题
    [return] 无
    '''
    try :
        if len(exit_key) == 1 :
            win_title = 'Exit <%s>; %s' % (exit_key, title)
            cv2.imshow(win_title, image)
            while True :
                press_key = cv2.waitKey(1) & 0xFF
                if press_key == ord(exit_key) :
                    break
        else :
            win_title = 'Exit <any key>; %s' % title
            cv2.imshow(win_title, image)
            cv2.waitKey(0)
    except :
        log.warn("绘制图像失败")


def show_frame(frame, exit_key='q', save_key='s', title='Preview Image') :
    '''
    绘制视频流的某一帧（依赖外部不断迭代绘制每一帧）
    [params] frame: 要绘制的帧
    [params] exit_key: 退出绘制的按键（默认为 'q'）
    [params] save_key: 保存当前帧的按键（默认为 's'）
    [params] title: 显示窗体的标题
    [return] (是否退出绘制, 是否保存当前帧)
    '''
    is_exit = False
    is_save = False

    try :
        exit_key = 'q' if len(exit_key) != 1 else exit_key
        save_key = 's' if len(save_key) != 1 else save_key
        win_title = 'Exit <%s>; Save <%s>; %s' % (exit_key, save_key, title)
        cv2.imshow(win_title, frame)

        press_key = cv2.waitKey(1) & 0xFF
        if press_key == ord(exit_key) :
            is_exit = True
        elif press_key == ord(save_key) :
            is_save = True
    except :
        log.warn("绘制图像失败")
    return (is_exit, is_save)


def save_image(image, savepath=SETTINGS.tmp_dir) :
    '''
    保存图像到文件
    [params] image: 要保存的图像
    [params] savepath: 保存位置
    [return] 是否保存成功
    '''
    return save_frame(image, savepath)


def save_frame(frame, savepath=SETTINGS.tmp_dir) :
    '''
    保存视频流的某一帧到图像文件
    [params] frame: 要保存的帧
    [params] savepath: 保存位置
    [return] 是否保存成功
    '''
    is_ok = False
    try :
        cv2.imwrite(savepath, frame)
        is_ok = True
        log.info("保存图像成功: %s" % savepath)
    except :
        log.warn("保存图像失败: %s" % savepath)
    return is_ok


def del_image(imgpath) :
    '''
    删除图像
    [params] imgpath: 图像位置
    [return] 是否删除成功
    '''
    if imgpath is None :
        return False

    if not os.path.exists(imgpath) :
        return False

    os.remove(imgpath)
    return True
