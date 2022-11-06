#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试计算人脸特征
# python ./tests/test_feature.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from main import record


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试计算人脸特征',
        description='通过 dlib 模型计算人脸 128 维特征', 
        epilog='\r\n'.join([
            '摄像头拍摄: ', 
            '  python ./tests/test_feature.py -c', 
            '上传人脸图片: ', 
            '  python ./tests/test_feature.py', 
        ])
    )
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    return parser.parse_args()


if '__main__' == __name__ :
    record(args())
