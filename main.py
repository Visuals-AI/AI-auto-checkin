#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import argparse
from pypdm.dbc._sqlite import SqliteDBC
from src.core.scheduler import Scheduler
from src.cache.face_cache import FACE_FEATURE_CACHE
from src.core.face_detection import FaceDetection
from src.config import SETTINGS
from color_log.clog import log


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='AI 自动签到',
        description='到达打卡时间点时，通过 AI 识别人脸为本人，通过 ADB 自动解锁手机签到打卡', 
        epilog='\r\n'.join([
            '示例: ', 
            '',
            '....'
        ])
    )
    parser.add_argument('-r', '--record', dest='record', action='store_true', default=False, help='录入模式: 用于录入人脸特征点; 默认为匹配模式')
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='仅[录入模式]有效: 摄像头录入方式; 默认为图片录入方式')
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
    fd = FaceDetection()
    fd.input_face(args.camera)


def recognise(args) :
    '''
    匹配模式
    '''
    log.info("程序启动模式: [人脸匹配模式]")
    FACE_FEATURE_CACHE.load_all()
    scheduler = Scheduler(args)
    scheduler.start()
    

def init() :
    sdbc = SqliteDBC(options=SETTINGS.database)
    sdbc.exec_script(SETTINGS.sqlpath)


if '__main__' == __name__ :
    init()
    main(args())

