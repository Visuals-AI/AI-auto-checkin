#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import re
import time
from color_log.clog import log
from src.config import SETTINGS


def adb(args) :
    log.info("根据预设步骤执行 adb 指令 ...")
    _adb = ADB()
    log.info("解锁手机 ...")
    _adb.exec(SETTINGS.unlock_screen, { 'password': args.password })
    log.info("打开目标 APP [%s] ..." % SETTINGS.app_name)
    _adb.exec(SETTINGS.open_app)
    log.info("签到 ...")
    _adb.exec(SETTINGS.check_in)
    log.info("锁屏 ...")
    _adb.exec(SETTINGS.lock_screen)
    log.info("执行 adb 指令完成")



def keep_live() :
    log.debug("adb 保活 ...")
    _adb = ADB()
    _adb.exec([SETTINGS.keep_live_cmd])



class ADB :

    def __init__(self) -> None:
        self.WAIT_CMD = 'wait '
        self.WAIT_RGX = r'wait (\d+)'
        self.PLACEHOLD = "<%s>"


    def exec(self, cmd_list, params={}) :
        for cmd in cmd_list :
            if cmd.startswith(self.WAIT_CMD) :
                time.sleep(self._take_time(cmd))
            else :
                cmd = self._fill_params(cmd, params)
                self._adb(cmd)
        
    
    def _take_time(self, cmd) :
        second = 0
        mth = re.match(self.WAIT_RGX, cmd)
        if mth :
            second = int(mth.groups(1)[0])
        return second


    def _fill_params(self, cmd, params) :
        for key, val in params.items() :
            cmd = cmd.replace(self.PLACEHOLD % key, val)
        return cmd


    def _adb(self, cmd) :
        return self._syscall('adb shell %s' % cmd)


    def _syscall(self, cmd) :
        log.debug('执行命令: %s' % cmd)
        rst = os.popen(cmd).read().strip() or ''
        log.debug('执行结果: %s' % rst)
        return rst
