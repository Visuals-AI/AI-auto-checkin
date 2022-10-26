#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

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


# 请求选择一个或多个文件
def open_select_window(title="Please select one or more files:") :
    filepaths = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        title=title,
        filetypes=FILETYPE
    )
    return filepaths
