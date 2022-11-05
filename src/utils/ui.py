#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

import os
import tkinter
from tkinter import filedialog


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
    [params] title: 窗口标题
    [return] 选择的文件路径
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
    [params] title: 窗口标题
    [return] 选择的文件路径
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

