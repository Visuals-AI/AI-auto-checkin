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
                self.debug = self.app.get('debug')
                self.sock = self.app.get('socket')
                self.log = self.app.get('log')

                self.ctrl = context.get('controller')
                screen = self.ctrl.get('screen')
                self.screen_width = int(screen.get('width') or _SW)
                self.screen_height = int(screen.get('height') or _SH)
                self.screen_center = (int(self.screen_width / 2), int(self.screen_height / 2))
                self.screen_zoom = int(screen.get('zoom'))
                cropping = self.ctrl.get('cropping')
                self.crop_width = cropping.get('width')
                self.crop_height = cropping.get('height')
                self.dpi = float(self.ctrl.get('mouse_dpi'))
                self.aim_mode = self.ctrl.get('aim_mode')
                windows = self.ctrl.get('windows')
                offset = windows.get('offset')
                self.offset_top = int(offset.get('top'))
                self.offset_left = int(offset.get('left'))

                device = context.get('video_capture_card')
                self.dev_idx = int(device.get('index') or 0)
                self.fourcc = list(device.get('fourcc') or 'MJPG')
                self.fps = device.get('fps')
                frame_size = device.get('frame')
                self.frame_width = frame_size.get('width')
                self.frame_height = frame_size.get('height')

                self.openpose = context.get('openpose')
                self.show_cv = self.openpose.get('show_cv')
                self.frequency = max(0, int(self.openpose.get('frequency')))
                self.model_folder = self.openpose.get('model_folder')
                self.model_pose = self.openpose.get('model_pose')
                self.part_names = self.openpose['parts'] or []


SETTINGS = Config(SETTINGS_PATH, CHARSET)

