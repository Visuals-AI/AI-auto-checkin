#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import erb.yml as yaml
PRJ_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from color_log.clog import log

CHARSET = 'utf-8'
SETTINGS_PATH = '%s/conf/settings.yml' % PRJ_DIR
FEATURE_SPLIT = ", "    # 特征值格式转换分隔符



class Config :

    def __init__(self, settings_path, charset) -> None:
        if os.path.exists(settings_path) :
            with open(settings_path, 'r', encoding=charset) as file:
                context = yaml.load(file.read())

                self.app = context.get('app')
                self.debug = self.app.get('debug')
                self.annotated = self.app.get('annotated')
                self.tmp_dir = self.app.get('tmp_dir')
                self.original_dir = self.app.get('original_dir')
                self.detection_dir = self.app.get('detection_dir')
                self.alignment_dir = self.app.get('alignment_dir')
                self.feature_fmt = self.app.get('feature_fmt')

                scheduler = context.get('scheduler')
                self.work_time = scheduler.get('work_time')
                self.checkin = scheduler.get('checkin')
                self.on_begin_at = int(self.checkin.get('begin_at') or 9)
                self.on_end_at = int(self.checkin.get('end_at') or 11)
                self.on_interval = int(self.checkin.get('interval') or 10)
                self.checkout = scheduler.get('checkout')
                self.off_begin_at = int(self.checkout.get('begin_at') or 18)
                self.off_end_at = int(self.checkout.get('end_at') or 23)
                self.off_interval = int(self.checkout.get('interval') or 10)

                self.database = context.get('database')
                self.sqlpath = self.database.get('sqlpath')

                self.mediapipe = context.get('mediapipe')
                self.show_image = self.mediapipe.get('show_image')
                self.show_video = self.mediapipe.get('show_video')
                resize_face = self.mediapipe.get('resize_face')
                self.face_width = resize_face.get('width')
                self.face_height = resize_face.get('height')
                self.match_min_sim = max(0.5, float(self.mediapipe.get('match_min_sim')))

                device = context.get('camera')
                self.dev_idx = int(device.get('index') or 0)
                self.fourcc = list(device.get('fourcc') or 'MJPG')
                self.fps = device.get('fps')
                frame_size = device.get('frame')
                self.frame_width = frame_size.get('width')
                self.frame_height = frame_size.get('height')

                self.adb = context.get('adb')
                self.keep_live = self.adb.get('keep_live')
                self.app_name = self.adb.get('app')
                self.adb_app = context.get(self.app_name)
                self.unlock_screen = self.adb_app.get('unlock_screen')
                self.open_app = self.adb_app.get('open_app')
                self.check_in = self.adb_app.get('check_in')
                self.lock_screen = self.adb_app.get('lock_screen')


SETTINGS = Config(SETTINGS_PATH, CHARSET)

