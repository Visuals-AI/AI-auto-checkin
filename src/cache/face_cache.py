#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

from pypdm.dbc._sqlite import SqliteDBC
from pypdm.assist.num import byte_to_str
from src.dao.t_face_feature import TFaceFeatureDao
from src.config import SETTINGS, FEATURE_SPLIT


class FaceCache :

    def __init__(self) -> None:
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()
        self.id_features = {}
        self.id_names = {}


    def load_all(self) :
        self.sdbc.conn()
        beans = self.dao.query_all(self.sdbc)
        self.sdbc.close()

        for bean in beans :
            self.add(bean)


    def add(self, bean) :
        self.id_features[bean.image_id] = self._str_to_feature(bean.feature)
        self.id_names[bean.image_id] = bean.name
    

    def _str_to_feature(self, s_feature) :
        '''
        字符串 转 特征值（复数数组）
        :param s_feature: 特征值字符串
        :return: 特征值（复数数组）
        '''
        s_feature = byte_to_str(s_feature)
        s_floats = s_feature.split(FEATURE_SPLIT)
        return list(complex(v) for v in s_floats)


FACE_FEATURE_CACHE = FaceCache()
