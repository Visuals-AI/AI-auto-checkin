#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 创建数据库 & pdm
# python ./tests/gen_pdm.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

from pypdm.builder import build
from pypdm.dbc._sqlite import SqliteDBC
from src.config import SETTINGS


def init() :
    sdbc = SqliteDBC(options=SETTINGS.database)
    sdbc.exec_script(SETTINGS.sqlpath)
    generate_pdm(sdbc)


def generate_pdm(sdbc) :
    paths = build(
        dbc = sdbc,
        pdm_pkg = 'src',
        table_whitelist = [ 't_face_feature' ],
        table_blacklist = [],
        to_log = True
    )



if '__main__' == __name__ :
    init()
