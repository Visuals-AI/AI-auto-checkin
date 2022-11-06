#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import argparse
from pypdm.dbc._sqlite import SqliteDBC
from src.core.scheduler import Scheduler
from src.app import record_face_feature
from src.cache.face_feature_cache import FACE_FEATURE_CACHE
from src.config import SETTINGS
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='AI 自动签到',
        description='到达打卡时间点时，自动打开摄像头，若 AI 识别摄像头前的为本人时，则通过 ADB 自动解锁手机签到打卡', 
        epilog='\r\n'.join([
            '录入模式: python .\main.py -r [-c]', 
            '匹配模式: python .\main.py -c -p {unlock_password}',
        ])
    )
    parser.add_argument('-r', '--record', dest='record', action='store_true', default=False, help='录入模式: 用于录入人脸特征点; 默认为匹配模式')
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    parser.add_argument('-p', '--password', dest='password', type=str, default='123456', help='仅[匹配模式]有效: 手机的锁屏密码')
    return parser.parse_args()


def main(args) :
    if (args.record) :
        record(args)

    else :
        recognise(args)


def record(args) :
    '''
    录入模式
    '''
    log.info("程序启动模式: [人脸录入模式]")
    if not FACE_FEATURE_CACHE.load_standard_face() :
        return
    record_face_feature(args)


def recognise(args) :
    '''
    匹配模式
    '''
    log.info("程序启动模式: [人脸匹配模式]")
    if not FACE_FEATURE_CACHE.load() :
        return
        
    scheduler = Scheduler(args)
    scheduler.start()
    

def init() :
    sdbc = SqliteDBC(options=SETTINGS.database)
    sdbc.exec_script(SETTINGS.sqlpath)


if '__main__' == __name__ :
    init()
    main(args())

