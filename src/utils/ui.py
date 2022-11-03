#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

import os
import cv2
import tkinter
from tkinter import filedialog
from color_log.clog import log


FILETYPE = [            # 设置文件对话框会显示的文件类型
    ('all files', '.*'), 
    ('image files', '.jpg'), 
    ('image files', '.jpeg'), 
    ('image files', '.png'), 
    ('image files', '.bpm')
]


def open_window_by_select_one(title="Please select one file:") :
    '''
    打开系统选择文件窗口（选择一个文件）
    [param] title: 窗口标题
    :return: 选择的文件路径
    '''
    tk = tkinter.Tk()
    tk.withdraw()     # 隐藏 tk 窗体
    filepath = filedialog.askopenfilename(
        initialdir = os.getcwd(),
        title = title,
        filetypes = FILETYPE
    )
    tk.destroy()      # 销毁 tk 窗体
    return filepath


def open_window_by_select_multi(title="Please select one or more files:") :
    '''
    打开系统选择文件窗口（选择多个文件）
    [param] title: 窗口标题
    :return: 选择的文件路径
    '''
    tk = tkinter.Tk()
    tk.withdraw()     # 隐藏 tk 窗体
    filepaths = filedialog.askopenfilenames(
        initialdir = os.getcwd(),
        title = title,
        filetypes = FILETYPE
    )
    tk.destroy()      # 销毁 tk 窗体
    return filepaths


def show_image(image, exit_key='q', title='Preview Image') :
    '''
    绘制图像
    （此方法不能用于视频流中绘制帧，因为判断按键时会强制卡死在同一帧）
    [param] image: 要绘制的图像
    [param] exit_key: 退出绘制的按键（默认为 'q'）
    [param] title: 显示窗体的标题
    :return: 无
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
    [param] frame: 要绘制的帧
    [param] exit_key: 退出绘制的按键（默认为 'q'）
    [param] save_key: 保存当前帧的按键（默认为 's'）
    [param] title: 显示窗体的标题
    :return: (是否退出绘制, 是否保存当前帧)
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


def save_image(image, savepath) :
    '''
    保存图像到文件
    [param] image: 要保存的图像
    [param] savepath: 保存位置
    :return: 是否保存成功
    '''
    return save_frame(image, savepath)


def save_frame(frame, savepath) :
    '''
    保存视频流的某一帧到图像文件
    [param] frame: 要保存的帧
    [param] savepath: 保存位置
    :return: 是否保存成功
    '''
    is_ok = False
    try :
        cv2.imwrite(savepath, frame)
        is_ok = True
    except :
        log.warn("保存图像失败")
    return is_ok

