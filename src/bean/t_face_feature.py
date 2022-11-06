#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# PDM: t_face_feature
# -------------------------------

class TFaceFeature :
    table_name = 't_face_feature'
    i_id = "i_id"
    s_face_id = "s_face_id"
    s_name = "s_name"
    f_feature = "f_feature"
    s_align_size = "s_align_size"
    s_mesh_image_path = "s_mesh_image_path"
    s_detection_image_path = "s_detection_image_path"
    s_alignment_image_path = "s_alignment_image_path"


    def __init__(self) :
        self.id = None
        self.face_id = None
        self.name = None
        self.feature = None
        self.align_size = None
        self.mesh_image_path = None
        self.detection_image_path = None
        self.alignment_image_path = None


    def params(self) :
        return (
            self.face_id,
            self.name,
            self.feature,
            self.align_size,
            self.mesh_image_path,
            self.detection_image_path,
            self.alignment_image_path,
        )


    def __repr__(self) :
        return '\n'.join(
            (
                '%s: {' % self.table_name,
                "    %s = %s" % (self.i_id, self.id),
                "    %s = %s" % (self.s_face_id, self.face_id),
                "    %s = %s" % (self.s_name, self.name),
                "    %s = %s" % (self.f_feature, self.feature),
                "    %s = %s" % (self.s_align_size, self.align_size),
                "    %s = %s" % (self.s_mesh_image_path, self.mesh_image_path),
                "    %s = %s" % (self.s_detection_image_path, self.detection_image_path),
                "    %s = %s" % (self.s_alignment_image_path, self.alignment_image_path),
                '}\n'
            )
        )
