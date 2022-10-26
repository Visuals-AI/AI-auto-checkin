#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import argparse
from ast import arg
from src.config import SETTINGS
from src.core import adb


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
    parser.add_argument('-r', '--record', dest='record', action='store_true', default=False, help='录入模式: 用于录入人脸特征点; 默认为识别模式')
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='仅[录入模式]有效: 摄像头录入方式; 默认为图片录入方式')
    # parser.add_argument('-i', '--imagepath', dest='imagepath', type=str, default='./data/features', help='仅[录入模式]有效: 特征图片的存储位置')
    parser.add_argument('-p', '--password', dest='password', type=str, default='123456', help='仅[识别模式]有效: 手机的锁屏密码')
    return parser.parse_args()


def main(args) :
    if (args.record) :
        record(args)

    else :
        recognise(args)

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
    

def record(args) :
    '''
    录入模式
    '''
    return


def recognise(args) :
    '''
    识别模式
    '''
    adb.exec(SETTINGS.unlock_screen, { 'password': args.password })
    adb.exec(SETTINGS.open_app)
    adb.exec(SETTINGS.check_in)


if '__main__' == __name__ :
    main(args())
