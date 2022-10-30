#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

# https://www.163.com/dy/article/GD24HMAN0531PF2O.html
# https://blog.csdn.net/woshicver/article/details/123059410
# pip install mediapipe
# pip install opencv-python

import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).seconds.do(job)
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    

# class Scheduler :

#     def __init__(self) :
        