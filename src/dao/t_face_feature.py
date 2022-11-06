#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# DAO: t_face_feature
# -------------------------------

from ..bean.t_face_feature import TFaceFeature
from pypdm.dao._base import BaseDao


class TFaceFeatureDao(BaseDao) :
    TABLE_NAME = 't_face_feature'
    SQL_COUNT = 'select count(1) from t_face_feature'
    SQL_TRUNCATE = 'truncate table t_face_feature'
    SQL_INSERT = 'insert into t_face_feature(s_image_id, s_name, f_feature, s_align_size, s_mesh_image_path, s_alignment_image_path, s_detection_image_path) values(?, ?, ?, ?, ?, ?, ?)'
    SQL_DELETE = 'delete from t_face_feature where 1 = 1 '
    SQL_UPDATE = 'update t_face_feature set s_image_id = ?, s_name = ?, f_feature = ?, s_align_size = ?, s_mesh_image_path = ?, s_alignment_image_path = ?, s_detection_image_path = ? where 1 = 1 '
    SQL_SELECT = 'select i_id, s_image_id, s_name, f_feature, s_align_size, s_mesh_image_path, s_alignment_image_path, s_detection_image_path from t_face_feature where 1 = 1 '

    def __init__(self) :
        BaseDao.__init__(self)

    def _to_bean(self, row) :
        bean = None
        if row:
            bean = TFaceFeature()
            bean.id = self._to_val(row, 0)
            bean.image_id = self._to_val(row, 1)
            bean.name = self._to_val(row, 2)
            bean.feature = self._to_val(row, 3)
            bean.align_size = self._to_val(row, 4)
            bean.mesh_image_path = self._to_val(row, 5)
            bean.alignment_image_path = self._to_val(row, 6)
            bean.detection_image_path = self._to_val(row, 7)
        return bean
