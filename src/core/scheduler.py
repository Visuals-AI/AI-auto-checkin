#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------


from tabnanny import check
import time
from apscheduler.schedulers.background import BackgroundScheduler
from src.cache.face_cache import FACE_FEATURE_CACHE
from src.core.face_compare import FaceCompare
from src.core.check_inout import CheckInOut
from src.core.adb import ADB_CLIENT, adb
from src.config import SETTINGS
from color_log.clog import log


class Scheduler :

    def __init__(self, args) :
        self.args = args
        self.scheduler = BackgroundScheduler()
        self.trigger = 'cron'
        self._set_task()

        self.fc = FaceCompare(args)
        self.cio = CheckInOut()


    def start(self) :
        log.info("定时任务已启动")
        self.scheduler.start()
        while True :
            time.sleep(60)


    def _set_task(self) :
        log.info("已设置【ADB 保活】定时任务: ")
        log.debug("循环: [%s] 秒/次" % SETTINGS.keep_live)
        self.scheduler.add_job(
            ADB_CLIENT.keep_live,
            trigger = self.trigger,
            second = str(SETTINGS.keep_live)
        )

        log.info("已设置【每天上班】自动打卡时间: ")
        log.debug("范围: [%02d:00] - [%02d:00]" % (SETTINGS.on_begin_at, SETTINGS.on_end_at))
        log.debug("循环: [%s] 分钟/次" % SETTINGS.on_interval)
        self.scheduler.add_job(
            self._task,
            trigger = self.trigger,
            second = '0',
            minute = '*/%d' % SETTINGS.on_interval,
            hour = '%d-%d' % (SETTINGS.on_begin_at, SETTINGS.on_end_at)
        )

        log.info("已设置【每天下班】自动打卡时间: ")
        log.debug("范围: [%02d:00] - [%02d:00]" % (SETTINGS.off_begin_at, SETTINGS.off_end_at))
        log.debug("循环: [%s] 分钟/次" % SETTINGS.off_interval)
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
        image_id = self.fc.input_face()
        if not image_id :
            log.warn("[取消打卡] 不是本人")
            return

        # 执行预设 adb 指令
        adb(self.args)

        # 更新打卡时间
        self.cio.update_today()


    def _check_task_conditions(self) :
        if len(FACE_FEATURE_CACHE.id_names) <= 0 :
            log.warn("[取消打卡] 库存中未录入任何人脸特征值")
            return False

        if not ADB_CLIENT.test_conn() :
            log.warn("[取消打卡] 未连接 adb 设备")
            return False

        work = self.cio.query_today()
        if work.checkin_hour >= 0 :
            hour = time.localtime().tm_hour
            minute = time.localtime().tm_min
            diff_hour = hour - work.checkin_hour
            diff_minute = minute - work.checkin_minute
            work_time = diff_hour * 60 + diff_minute
            if work_time < SETTINGS.work_time :
                log.warn("[取消打卡] 上班时长不够，目前仅工作 [%d] 分钟" % work_time)
                return False

        if work.work_time >= SETTINGS.work_time :
            log.warn("[取消打卡] 今天工作 [%d] 分钟，已满足最低工作时长" % work_time)
            return False

        return True
