#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import tkinter
from tkinter import filedialog
import os

# 设置文件对话框会显示的文件类型
FILETYPE = [
    ('all files', '.*'), 
    ('image files', '.jpg'), 
    ('image files', '.jpeg'), 
    ('image files', '.png'), 
    ('image files', '.bpm')
]


# 请求选择一个文件
def open_select_one_window(title="Please select one file:") :
    tk = tkinter.Tk()
    tk.withdraw()     # 隐藏 tk 窗体
    filepath = filedialog.askopenfilename(
        initialdir = os.getcwd(),
        title = title,
        filetypes = FILETYPE
    )
    tk.destroy()      # 销毁 tk 窗体
    return filepath


# 请求选择一个或多个文件
def open_select_multi_window(title="Please select one or more files:") :
    tk = tkinter.Tk()
    tk.withdraw()     # 隐藏 tk 窗体
    filepaths = filedialog.askopenfilenames(
        initialdir = os.getcwd(),
        title = title,
        filetypes = FILETYPE
    )
    tk.destroy()      # 销毁 tk 窗体
    return filepaths


def open_camera() :
    # TODO
    return []
