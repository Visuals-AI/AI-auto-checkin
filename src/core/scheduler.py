#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------


import schedule
import time
from color_log.clog import log
from src.core.face_compare import FaceCompare
from src.utils import adb
from src.config import SETTINGS


class Scheduler :

    def __init__(self, args) :
        self.args = args
        self._set_task()


    def start(self) :
        log.info("定时任务已启动")
        while True:
            schedule.run_pending()
            time.sleep(1)
        log.info("定时任务已停止")


    def _set_task(self) :
        log.info("已设置上班自动打卡时间: ")
        log.info("范围: [%s] - [%s]" % (SETTINGS.on_begin_at, SETTINGS.on_end_at))
        log.info("循环: [%s] 分钟/次" % SETTINGS.on_interval)
        schedule.every(SETTINGS.on_interval).minutes.\
                    at(SETTINGS.on_begin_at).until(SETTINGS.on_end_at).\
                    do(self._task)

        log.info("已设置下班自动打卡时间: ")
        log.info("范围: [%s] - [%s]" % (SETTINGS.off_begin_at, SETTINGS.off_end_at))
        log.info("循环: [%s] 分钟/次" % SETTINGS.off_interval)
        schedule.every(SETTINGS.off_interval).minutes.\
                    at(SETTINGS.off_begin_at).until(SETTINGS.off_end_at).\
                    do(self._task)


    def _task(self) :
        if not self._check_task_conditions() :
            log.warn("未满足执行条件，本轮定时任务取消")
            return

        fc = FaceCompare()
        fc.input_face(self.args.camera)

        # adb.exec(SETTINGS.unlock_screen, { 'password': args.password })
        # adb.exec(SETTINGS.open_app)
        # adb.exec(SETTINGS.check_in)

    
    def _check_task_conditions(self) :
        is_Ok = True
        # 已录入特征值
        # 已连接 adb
        # 未打卡
        # 已打卡但未满 8H
        return is_Ok




# 思路：
#   1. 定时器：到达打卡时间范围（上班/下班各一）
#   2. 判断今天是否已打卡，若否继续
#   3. 打开电脑摄像头，通过 AI 人脸识别判断当前屏幕前的是否为本人，若是继续
#   4. 通过 ADB 指令解锁手机，并进入 APP 打卡
#   5. 打卡成功，标记今天已打卡，手机锁屏
#
#   备注
#       1. 上班卡: 9:00 开始，只要未打则半小时打一次
#       2. 下班卡: 18:00 开始，在 ADB 连通的情况下，每隔半小时打一次，直到 24:00
#       3. 上传人脸图片时，先做初始动作： 框取脸部位置，调整缩放图片的尺寸一致