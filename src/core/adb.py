#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import time
from color_log.clog import log
from src.config import SETTINGS


class ADB :

    def __init__(self) -> None:
        pass

    def exec(cmd_list, params={}, interval=SETTINGS.cmd_interval) :
        for cmd in cmd_list :
            cmd = _fill_params(cmd, params)
            _adb(cmd)
            time.sleep(interval)
        

    def _fill_params(cmd, params) :
        for key, val in params.items() :
            cmd = cmd.replace("<%s>" % key, val)
        return cmd


    def _adb(cmd) :
        return _syscall('adb shell %s' % cmd)


    def _syscall(cmd) :
        log.debug('执行命令: %s' % cmd)
        rst = os.popen(cmd).read().strip() or ''
        log.debug('执行结果: %s' % rst)
        return rst
