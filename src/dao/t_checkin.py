#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# DAO: t_checkin
# -------------------------------

from ..bean.t_checkin import TCheckin
from pypdm.dao._base import BaseDao


class TCheckinDao(BaseDao) :
    TABLE_NAME = 't_checkin'
    SQL_COUNT = 'select count(1) from t_checkin'
    SQL_TRUNCATE = 'truncate table t_checkin'
    SQL_INSERT = 'insert into t_checkin(s_date, i_checkin_hour, i_checkin_minute, i_checkout_hour, i_checkout_minute, i_work_time) values(?, ?, ?, ?, ?, ?)'
    SQL_DELETE = 'delete from t_checkin where 1 = 1 '
    SQL_UPDATE = 'update t_checkin set s_date = ?, i_checkin_hour = ?, i_checkin_minute = ?, i_checkout_hour = ?, i_checkout_minute = ?, i_work_time = ? where 1 = 1 '
    SQL_SELECT = 'select i_id, s_date, i_checkin_hour, i_checkin_minute, i_checkout_hour, i_checkout_minute, i_work_time from t_checkin where 1 = 1 '

    def __init__(self) :
        BaseDao.__init__(self)

    def _to_bean(self, row) :
        bean = None
        if row:
            bean = TCheckin()
            bean.id = self._to_val(row, 0)
            bean.date = self._to_val(row, 1)
            bean.checkin_hour = self._to_val(row, 2)
            bean.checkin_minute = self._to_val(row, 3)
            bean.checkout_hour = self._to_val(row, 4)
            bean.checkout_minute = self._to_val(row, 5)
            bean.work_time = self._to_val(row, 6)
        return bean
