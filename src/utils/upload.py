#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

import os
import uuid
import shutil
from src.config import SETTINGS


def upload(filepath) :
    '''
    上传文件到临时目录
    [param] filepath: 文件原始路径
    :return: (文件名, 文件后缀, 分配的文件ID, 临时上传路径)
    '''
    name, suffix = _gen_file_params(filepath)
    fileid = _gen_file_id()
    tmppath = "%s/%s%s" % (SETTINGS.tmp_dir, fileid, suffix)
    shutil.copyfile(filepath, tmppath)
    return (name, suffix, fileid, tmppath)


def _gen_file_params(filepath) :
    '''
    提取文件路径信息
    [param] filepath: 文件原始路径
    :return: (文件名, 文件后缀, 分配的文件ID)
    '''
    filename = os.path.split(filepath)[-1]
    name = os.path.splitext(filename)[0]
    suffix = os.path.splitext(filename)[-1]
    return (name, suffix)


def _gen_file_id() :
    '''
    生成文件的唯一 ID
    :return: 文件 ID
    '''
    return uuid.uuid1().hex
