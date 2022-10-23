#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import argparse


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='自动签到机',
        description='到达打卡时间点时，通过 AI 识别人脸为本人，通过 ADB 自动解锁手机签到打卡', 
        epilog='\r\n'.join([
            '示例: ', 
            '',
            '....'
        ])
    )
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='调试模式，用于查看 AI 识别的画面')
    parser.add_argument('-m', '--mode', dest='mode', type=str, default='alone', help='alone :单机模式; duplex :联机模式')
    parser.add_argument('-f', '--frame', dest='frame', action='store_true', default=False, help='仅单机模式下有效。true:连续帧识别; false:截屏识别（默认）')
    parser.add_argument('-r', '--role', dest='role', type=str, default='ai', help='仅联机模式下有效。ai/server:AI角色（服务端）; ct/ctrl/client:控制器角色（客户端）')
    return parser.parse_args()


def main(args) :
    # 思路：
    #   1. 定时器：到达打卡时间范围（上班/下班各一）
    #   2. 判断今天是否已打卡，若否继续
    #   3. 打开电脑摄像头，通过 AI 人脸识别判断当前屏幕前的是否为本人，若是继续
    #   4. 通过 ADB 指令唤起手机 APP 打卡
    #   5. 打卡成功，标记今天已打卡
    #
    #   备注
    #       1. 上班卡: 9:00 开始，只要未打则半小时打一次
    #       2. 下班卡: 18:00 开始，在 ADB 连通的情况下，每隔半小时打一次，直到 24:00


if '__main__' == __name__ :
    main(args())