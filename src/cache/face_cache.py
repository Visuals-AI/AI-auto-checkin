#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

from pypdm.dbc._sqlite import SqliteDBC
from pypdm.assist.num import byte_to_str
from src.dao.t_face_feature import TFaceFeatureDao
from src.cache.face_data import FaceData
from src.config import SETTINGS, CHARSET, COORD_SPLIT
from color_log.clog import log


class FaceCache :

    def __init__(self) -> None:
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()
        self.standard_fkp_coords = []
        self.id_features = {}
        self.id_names = {}


    def load(self) :
        self._load_standard_face()
        self._load_all_features()


    def _load_standard_face(self) :
        '''
        读取标准人脸的关键点地标
        '''
        filepath = '%s/%s' % (SETTINGS.standard_dir, SETTINGS.standard_face)
        log.info("正在标准脸的关键点地标到内存: %s" % filepath)
        try :

            with open(filepath, 'r', encoding=CHARSET) as file :
                for line in file.readlines() :
                    line = line.strip()
                    if not line or line.startswith("#") :
                        continue
                    coords = line.split(COORD_SPLIT)
                    x = float(coords[0])
                    y = float(coords[1])
                    self.standard_fkp_coords.append([x, y])

            log.info("加载标准脸成功: %s" % self.standard_fkp_coords)
        except :
            log.error("加载标准脸失败")


    def _load_all_features(self) :
        '''
        读取库存的人脸特征到内存
        '''
        log.info("正在加载库存的人脸特征到内存 ...")
        self.sdbc.conn()
        beans = self.dao.query_all(self.sdbc)
        self.sdbc.close()

        for bean in beans :
            self.add(bean)
        log.info("缓存人脸特征完成，共 [%d] 个" % len(beans))


    def add(self, bean) :
        '''
        添加新的人脸特征到内存
        '''
        self.id_features[bean.image_id] = self._str_to_feature(bean.feature)
        self.id_names[bean.image_id] = bean.name
    

    def _str_to_feature(self, s_feature) :
        '''
        字符串 转 特征值（复数数组）
        [params] s_feature: 特征值字符串
        [return] 特征值（复数数组）
        '''
        s_feature = byte_to_str(s_feature)
        s_floats = s_feature.split(COORD_SPLIT)
        return list(complex(v) for v in s_floats)


FACE_CACHE = FaceCache()
