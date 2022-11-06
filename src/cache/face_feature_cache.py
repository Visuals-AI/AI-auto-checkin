#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------

from pypdm.dbc._sqlite import SqliteDBC
from src.utils.common import str_to_feature
from src.bean.t_face_feature import TFaceFeature
from src.dao.t_face_feature import TFaceFeatureDao
from src.config import SETTINGS, CHARSET, COORD_SPLIT
from color_log.clog import log


class FaceFeatureCache :

    def __init__(self) -> None:
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()
        self.wheres = {
            f'{TFaceFeature.s_align_size} = ': SETTINGS.standard_face
        }

        self.standard_fkp_coords = []
        self.id_features = {}
        self.id_names = {}


    def load(self) :
        is_ok = True
        is_ok &= self.load_standard_face()
        is_ok &= self.load_all_features()
        return is_ok


    def load_standard_face(self) :
        '''
        读取标准人脸的关键点地标
        '''
        is_ok = True
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

            if self.standard_fkp_coords :
                log.info("加载标准脸成功: %s" % self.standard_fkp_coords)
            else :
                log.warn(f"未设置尺寸为 [{SETTINGS.standard_face}] 的标准脸地标，请先按步骤设置标准脸:")
                log.warn(f"  网上搜索任意的标准人脸照片，大小修改为 [{SETTINGS.standard_face}]")
                log.warn("  设置当前规格的标准脸: python ./presrc/gen_standard.py")
                is_ok = False
        except :
            is_ok = False
            log.error("加载标准脸失败")
        return is_ok


    def load_all_features(self) :
        '''
        读取库存的人脸特征到内存
        '''
        is_ok = True
        log.info("正在加载库存的人脸特征到内存 ...")
        self.sdbc.conn()
        beans = self.dao.query_some(self.sdbc, self.wheres)
        self.sdbc.close()

        if len(beans) <= 0 :
            log.warn(f"库中无规格为 [{SETTINGS.standard_face}] 的人脸特征，请先按步骤录入人脸:")
            log.warn("  设置当前规格的标准脸: python ./presrc/gen_standard.py")
            log.warn("  录入用于匹配的人脸特征: python ./presrc/gen_feature.py")
            is_ok = False
        else :
            for bean in beans :
                self.add(bean)
            log.info("缓存人脸特征完成，共 [%d] 个" % len(beans))
        return is_ok
        

    def add(self, bean) :
        '''
        添加新的人脸特征到内存
        '''
        self.id_features[bean.image_id] = str_to_feature(bean.feature)
        self.id_names[bean.image_id] = bean.name
    


FACE_FEATURE_CACHE = FaceFeatureCache()
