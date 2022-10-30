#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# PDM: t_checkin
# -------------------------------

class TCheckin :
    table_name = 't_checkin'
    i_id = "i_id"
    s_date = "s_date"
    i_checkin_hour = "i_checkin_hour"
    i_checkin_minute = "i_checkin_minute"
    i_checkout_hour = "i_checkout_hour"
    i_checkout_minute = "i_checkout_minute"
    i_work_time = "i_work_time"


    def __init__(self) :
        self.id = None
        self.date = None
        self.checkin_hour = None
        self.checkin_minute = None
        self.checkout_hour = None
        self.checkout_minute = None
        self.work_time = None


    def params(self) :
        return (
            self.date,
            self.checkin_hour,
            self.checkin_minute,
            self.checkout_hour,
            self.checkout_minute,
            self.work_time,
        )


    def __repr__(self) :
        return '\n'.join(
            (
                '%s: {' % self.table_name,
                "    %s = %s" % (self.i_id, self.id),
                "    %s = %s" % (self.s_date, self.date),
                "    %s = %s" % (self.i_checkin_hour, self.checkin_hour),
                "    %s = %s" % (self.i_checkin_minute, self.checkin_minute),
                "    %s = %s" % (self.i_checkout_hour, self.checkout_hour),
                "    %s = %s" % (self.i_checkout_minute, self.checkout_minute),
                "    %s = %s" % (self.i_work_time, self.work_time),
                '}\n'
            )
        )
