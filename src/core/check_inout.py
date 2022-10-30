#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import time
import datetime
from pypdm.dbc._sqlite import SqliteDBC
from src.bean.t_checkin import TCheckin
from src.dao.t_checkin import TCheckinDao
from src.config import SETTINGS
from color_log.clog import log


class CheckInOut :

    def __init__(self) -> None:
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TCheckinDao()

    
    def query_today(self) :
        today = datetime.date.today()
        wheres = { TCheckin.s_date: today }

        self.sdbc.conn()
        bean = self.dao.query_one(self.sdbc, wheres)
        self.sdbc.close()
        return bean


    def update_today(self) :
        today = datetime.date.today()
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min

        bean = self.query_today()
        if bean is None :
            bean = TCheckin()
            bean.date = today
            bean.checkin_hour = -1
            bean.checkin_minute = -1
            bean.checkout_hour = -1
            bean.checkout_minute = -1
            bean.work_time = -1

        is_ok = False
        self.sdbc.conn()
        if not bean.checkin_hour :
            bean.checkin_hour = hour
            bean.checkin_minute = minute
            is_ok = self.dao.insert(self.sdbc, bean)
            log.info("更新 [%s] 上班打卡时间 [%02d:%02d] %s" % (
                today, bean.checkin_hour, bean.checkin_minute, 
                ("成功" if is_ok else "失败"))
            )

        else :
            bean.checkout_hour = hour
            bean.checkout_minute = minute
            diff_hour = bean.checkout_hour - bean.checkin_hour
            diff_minute = bean.checkout_minute - bean.checkin_minute
            bean.work_time = diff_hour * 60 + diff_minute
            is_ok = self.dao.update(self.sdbc, bean)
            log.info("更新 [%s] 下班打卡时间 [%02d:%02d] %s" % (
                today, bean.checkout_hour, bean.checkout_minute, 
                ("成功" if is_ok else "失败"))
            )

        self.sdbc.close()
        return is_ok

        