#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------


import time
from apscheduler.schedulers.background import BackgroundScheduler
from src.cache.face_cache import FACE_FEATURE_CACHE
from src.core.face_compare import FaceCompare
from src.core.adb import adb, keep_live
from src.config import SETTINGS
from color_log.clog import log


class Scheduler :

    def __init__(self, args) :
        self.args = args
        self.scheduler = BackgroundScheduler()
        self.trigger = 'cron'
        self._set_task()


    def start(self) :
        log.info("定时任务已启动")
        self.scheduler.start()
        while True :
            time.sleep(60)


    def _set_task(self) :
        log.info("已设置【ADB 保活】定时任务: ")
        log.info("循环: [%s] 秒/次" % SETTINGS.keep_live_time)
        self.scheduler.add_job(
            keep_live,
            trigger = self.trigger,
            second = str(SETTINGS.keep_live_time)
        )

        log.info("已设置【每天上班】自动打卡时间: ")
        log.info("范围: [%02d:00] - [%02d:00]" % (SETTINGS.on_begin_at, SETTINGS.on_end_at))
        log.info("循环: [%s] 分钟/次" % SETTINGS.on_interval)
        self.scheduler.add_job(
            self._task,
            trigger = self.trigger,
            second = '0',
            minute = '*/%d' % SETTINGS.on_interval,
            hour = '%d-%d' % (SETTINGS.on_begin_at, SETTINGS.on_end_at)
        )

        log.info("已设置【每天下班】自动打卡时间: ")
        log.info("范围: [%02d:00] - [%02d:00]" % (SETTINGS.off_begin_at, SETTINGS.off_end_at))
        log.info("循环: [%s] 分钟/次" % SETTINGS.off_interval)
        self.scheduler.add_job(
            self._task,
            trigger = self.trigger,
            second = '0',
            minute = '*/%d' % SETTINGS.off_interval,
            hour = '%d-%d' % (SETTINGS.off_begin_at, SETTINGS.off_end_at)
        )


    def _task(self) :
        if not self._check_task_conditions() :
            log.warn("未满足执行条件，本轮定时任务取消")
            return

        # 拍摄人脸
        fc = FaceCompare()
        image_id = fc.input_face(self.args.camera)
        if not image_id :
            return  # 匹配失败

        # 执行预设 adb 指令
        adb(self.args)

    
    def _check_task_conditions(self) :
        if len(FACE_FEATURE_CACHE.id_names) <= 0 :
            log.warn("库存中未录入任何人脸特征值")
            return False

        # 未连接 adb
        # 截止当前时间未满 8H
        # 已打卡且已满 8H
        return True




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