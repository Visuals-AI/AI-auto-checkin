#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------
# 测试人脸匹配
# python ./tests/test_compare.py
# -----------------------------------------------

# 把父级目录（项目根目录）添加到工作路径
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
# ----------------------------------------------------------------------

import argparse
from src.cache.face_feature_cache import FACE_FEATURE_CACHE
from src.app import record_face_feature, match_face_feature


def args() :
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog='测试人脸匹配',
        description='测试人脸匹配', 
        epilog='\r\n'.join([
            '摄像头拍摄: ', 
            '  python ./tests/test_compare.py -c', 
            '上传人脸图片: ', 
            '  python ./tests/test_compare.py', 
            '注意：', 
            '  需要至少执行一次 python ./presrc/gen_feature.py 录入预设人脸，作为特征匹配的比对基准', 
        ])
    )
    parser.add_argument('-c', '--camera', dest='camera', action='store_true', default=False, help='摄像头模式; 默认为图片上传模式')
    return parser.parse_args()


def test(args) :
    if not FACE_FEATURE_CACHE.load() :
        return
        
    feature = record_face_feature(args)
    match_face_feature(feature)



if '__main__' == __name__ :
    test(args())
