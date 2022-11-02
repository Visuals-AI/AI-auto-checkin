#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import re
import time
from color_log.clog import log
from src.config import SETTINGS


class ADBClient :

    def __init__(self) -> None:
        self.WAIT_CMD = 'wait '
        self.WAIT_RGX = r'wait (\d+)'
        self.PLACEHOLD = "<%s>"
        self.CMD_TESTCONN = "adb devices"
        self.CMD_LIVENESS = "adb shell pwd"


    def test_conn(self) :
        is_conn = False
        rst = self._syscall(self.CMD_TESTCONN)
        if 'no devices' in rst :
            return is_conn
        
        lines = rst.split("\n")
        if len(lines) > 1 and 'device' in lines[-1] :
            is_conn = True
        return is_conn

    
    def keep_live(self) :
        self._syscall(self.CMD_LIVENESS)


    def exec(self, cmd_list, params={}) :
        for cmd in cmd_list :
            if cmd.startswith(self.WAIT_CMD) :
                interval = self._take_time(cmd)
                log.debug("等待 %d 秒 ..." % interval)
                time.sleep(interval)
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
        # log.debug('执行结果: %s' % rst)
        return rst



ADB_CLIENT = ADBClient()


def adb(args) :
    log.info("根据预设步骤执行 adb 指令 ...")
    log.info("解锁手机 ...")
    ADB_CLIENT.exec(SETTINGS.unlock_screen, { 'password': args.password })
    log.info("打开目标 APP [%s] ..." % SETTINGS.app_name)
    ADB_CLIENT.exec(SETTINGS.open_app)
    log.info("签到 ...")
    ADB_CLIENT.exec(SETTINGS.check_in)
    log.info("锁屏 ...")
    ADB_CLIENT.exec(SETTINGS.lock_screen)
    log.info("执行 adb 指令完成")

