#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
import mediapipe as mp
from src.cache.face_data import FaceData
from src.utils.upload import *
from src.utils.image import *
from src.config import SETTINGS
from color_log.clog import log


class FaceDetection :

    def __init__(self, 
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) :
        '''
        构造函数
        [params] model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        [params] static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        [params] min_detection_confidence: 人脸检测模型的最小置信度值
        [params] min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        # 导入绘图模块
        self.mp_drawing = mp.solutions.drawing_utils

        # 导入人脸检测模块
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection = model_selection, 
            min_detection_confidence = min_detection_confidence
        )
    
    
    def handle(self, imgpath, label=False) -> FaceData :
        '''
        检测图像中所有人脸
        [params] label: 是否缓存地标坐标
                        默认不缓存，影响返回值的 *box_coords 和 *fkp6_coords 地标数据
                        不缓存可以加速检测，若无必要可以不取这些地标
        [return]: FaceData 缓存数据; 若异常返回 None
        '''
        self.fd = None
        if imgpath :
            try :
                self.fd = FaceData()
                self._read_image(imgpath)
                self._faces_detection(label)
                del_image(self.fd.imgpath)
            except :
                log.error("人脸检测模型异常")
        return self.fd


    def _read_image(self, imgpath) :
        '''
        读取图像参数
        [params] imgpath: 图像路径
        [return]: None （参数太多且需要交叉引用，临时存储到类变量 FaceData）
        '''
        self.fd.name, suffix, self.fd.image_id, self.fd.imgpath = upload(imgpath, SETTINGS.tmp_dir)
        self.fd.bgr_frame = cv2.imread(self.fd.imgpath)                             # 原图（彩色）
        self.fd.rgb_frame = cv2.cvtColor(self.fd.bgr_frame, cv2.COLOR_BGR2RGB)      # 图片转换到 RGB 通道（反色）
        self.fd.width, self.fd.height = get_shape_size(self.fd.rgb_frame)           # 图像宽高深
        return self.fd.rgb_frame

    
    def _faces_detection(self, label) :
        '''
        检测图像中所有人脸方框
        [params] label: 是否缓存地标坐标
        [return]: None
        '''
        results = self.face_detection.process(self.fd.rgb_frame)       # 图像检测
        for detection_id, detection in enumerate(results.detections):  # 枚举从图像中检测到的每一个人脸
            self._face_detection(detection_id, detection, label)
            break   # 只取图像中的第一人，暂不支持一图多人的情况，主要 FaceData 缓存数据不好处理
        

    def _face_detection(self, detection_id, detection, label) :
        '''
        检测单个人脸方框
        [params] detection_id: 人脸检测编号
        [params] detection: 人脸检测数据
        [params] label: 是否缓存地标坐标
        [return]: None
        '''
        location_data = detection.location_data
        if location_data.format == location_data.RELATIVE_BOUNDING_BOX:

            if label :
                # 人脸边界和关键点-6 地标（归一化）
                self.fd.normalized_box_coords = self._get_bounding_box(location_data, True)
                self.fd.normalized_fkp6_coords = self._get_face_keypoints(location_data, True)
                
                # 人脸边界和关键点-6 地标
                self.fd.box_coords = self._get_bounding_box(location_data, False)
                self.fd.fkp6_coords = self._get_face_keypoints(location_data, False)

            # 保存图像
            self._save_image(detection_id, detection)
        

    def _get_bounding_box(self, location_data, normalized=True) :
        '''
        获取人脸边界框地标
        [params] location_data: 人脸坐标数据
        [params] normalized: 是否获取归一化坐标（默认是）
        [return] 方框的左上角和右下角坐标
            [ 
                [x-left, y-upper],  
                [x-right, y-down] 
            ]
        '''
        # 得到检测到人脸位置的方框标记
        box = location_data.relative_bounding_box   
        width = 1 if normalized else self.fd.width
        height = 1 if normalized else self.fd.height
        desc = "（归一化）" if normalized else ''

        # 计算人脸方框的原始坐标
        left = box.xmin * width
        upper = box.ymin * height
        right = (box.xmin + box.width) * width
        down = (box.ymin + box.height) * height
        box_coord = [
            [left, upper], 
            [right, down]
        ]

        log.debug(f'人脸边界框地标{desc}: ')
        log.debug(f'  左上角: [{left}, {upper}]')
        log.debug(f'  右下角: [{right}, {down}]')
        return box_coord


    def _get_face_keypoints(self, location_data, normalized=True) :
        '''
        获取人脸 6 个关键点地标：
            https://github.com/google/mediapipe/blob/5fd3701cfd7564b3b6de7120dfc882355675b033/mediapipe/python/solutions/face_detection.py#L46
            class FaceKeyPoint(enum.IntEnum):
                RIGHT_EYE = 0
                LEFT_EYE = 1
                NOSE_TIP = 2
                MOUTH_CENTER = 3
                RIGHT_EAR_TRAGION = 4
                LEFT_EAR_TRAGION = 5
        [params] location_data: 人脸坐标数据
        [params] normalized: 是否获取归一化坐标（默认是）
        [return] 6 个关键点地标
            [
                [x0, y0],   # RIGHT_EYE
                [x1, y1],   # LEFT_EYE
                [x2, y2],   # NOSE_TIP
                [x3, y3],   # MOUTH_CENTER
                [x4, y4],   # RIGHT_EAR_TRAGION
                [x5, y5],   # LEFT_EAR_TRAGION
            ]
        '''
        width = 1 if normalized else self.fd.width
        height = 1 if normalized else self.fd.height
        desc = "（归一化）" if normalized else ''

        log.debug(f'人脸关键点-6 地标{desc}: ')
        fkp_coords = []
        for id, keypoint in enumerate(location_data.relative_keypoints) :
            name = self.mp_face_detection.FaceKeyPoint(id).name
            x = keypoint.x * width
            y = keypoint.y * height
            fkp_coords.append([x, y])
            log.debug(f'  {name}: [{x}, {y}]')
        return fkp_coords


    def _save_image(self, detection_id, detection) :
        '''
        保存标注人脸边框和关键点的图像
        [params] detection_id: 人脸检测编号
        [params] detection: 人脸检测数据
        [return] 方框的左上角和右下角坐标
            [ 
                [x-left, y-upper],  
                [x-right, y-down] 
            ]
        '''
        # 在原图标注关键点
        annotated_frame = self.fd.copy_BGR()                            # 复制原图
        self.mp_drawing.draw_detection(annotated_frame, detection)      # 绘制标注
        if SETTINGS.show_image :
            show_image(annotated_frame)

        # 保存图像
        savepath = '%s/%s%s' % (SETTINGS.detection_dir, self.fd.image_id, SETTINGS.image_format)
        save_image(annotated_frame, savepath)

        # 缓存数据
        self.fd.detection_frame = annotated_frame
        self.fd.detection_path = savepath
