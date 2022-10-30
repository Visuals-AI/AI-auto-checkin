#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试 ADB 指令
# python ./tests/test_adb.py -p [unlock_password]
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.core.adb import adb


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试 ADB 指令',
        description='', 
        epilog='\r\n'.join([
            '示例: ', 
            'python ./tests/test_adb.py'
        ])
    )
    parser.add_argument('-p', '--password', dest='password', type=str, default='123456', help='手机的锁屏密码')
    return parser.parse_args()


if '__main__' == __name__ :
    adb(args())
