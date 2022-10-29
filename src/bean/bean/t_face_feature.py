#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# PDM: t_face_feature
# -------------------------------

class TFaceFeature :
    table_name = 't_face_feature'
    i_id = "i_id"
    s_name = "s_name"
    f_feature = "f_feature"
    s_original_image_path = "s_original_image_path"
    s_feature_image_path = "s_feature_image_path"


    def __init__(self) :
        self.id = None
        self.name = None
        self.feature = None
        self.original_image_path = None
        self.feature_image_path = None


    def params(self) :
        return (
            self.name,
            self.feature,
            self.original_image_path,
            self.feature_image_path,
        )


    def __repr__(self) :
        return '\n'.join(
            (
                '%s: {' % self.table_name,
                "    %s = %s" % (self.i_id, self.id),
                "    %s = %s" % (self.s_name, self.name),
                "    %s = %s" % (self.f_feature, self.feature),
                "    %s = %s" % (self.s_original_image_path, self.original_image_path),
                "    %s = %s" % (self.s_feature_image_path, self.feature_image_path),
                '}\n'
            )
        )
