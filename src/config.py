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


class Config :

    def __init__(self, settings_path, charset) -> None:
        if os.path.exists(settings_path) :
            with open(settings_path, 'r', encoding=charset) as file:
                context = yaml.load(file.read())

                self.app = context.get('app')
                self.on_work = int(self.app.get('on_work') or 0)
                self.off_work = int(self.app.get('off_work') or 0)
                self.checkin_interval = int(self.app.get('checkin_interval') or 0)

                self.mediapipe = context.get('mediapipe')
                self.show_cv = self.mediapipe.get('show_cv')
                self.frequency = max(0, int(self.mediapipe.get('frequency')))

                device = context.get('video_capture_card')
                self.dev_idx = int(device.get('index') or 0)
                self.fourcc = list(device.get('fourcc') or 'MJPG')
                self.fps = device.get('fps')
                frame_size = device.get('frame')
                self.frame_width = frame_size.get('width')
                self.frame_height = frame_size.get('height')

                self.adb = context.get('adb')
                self.cmd_interval = self.adb.get('cmd_interval')
                self.unlock_screen = self.adb.get('unlock_screen')
                self.open_app = self.adb.get('open_app')
                self.check_in = self.adb.get('check_in')
                

SETTINGS = Config(SETTINGS_PATH, CHARSET)

