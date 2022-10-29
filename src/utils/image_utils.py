#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

def get_shape_size(cv_image) :
    '''
    获取图像的宽高
    :param cv_image: CV 载入的图像
    :return: (width, height)
    '''
    height = 0
    width = 0
    if cv_image is not None :
        size = cv_image.shape
        height = size[0]
        width = size[1]
    return (width, height)

