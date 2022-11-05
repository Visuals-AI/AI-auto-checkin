#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import cv2
import mediapipe as mp
from src.cache.face_data import FaceData
from src.utils.upload import *
from src.utils.image import *
from src.utils.ui import *
from src.config import SETTINGS
from color_log.clog import log


class FaceMesh :

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
        self.drawing_landmark = self.mp_drawing.DrawingSpec(    # 绘制地标属性
            thickness = 2, 
            circle_radius = 1, 
            color = LabelColor.RED
        )
        self.drawing_line = self.mp_drawing.DrawingSpec(        # 绘制网格连接线属性
            thickness = 2, 
            circle_radius = 1, 
            color = LabelColor.WHITE
        )

        # 导入人脸网格模块
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,         # False: 视频流; True: 图片
            max_num_faces=1,                # 检测人脸个数
            min_detection_confidence=0.5    # 人脸检测模型的最小置信度值
        )
    
    
    def handle(self, imgpath, label=False) -> FaceData :
        '''
        检测图像中所有人脸
        [params] label: 是否缓存地标坐标
                        默认不缓存，影响返回值的 *box_coords 和 *face_keypoints_coords 地标数据
                        不缓存可以加速检测，若无必要可以不取这些地标
        [return]: FaceData 缓存数据
        '''
        self._reset()
        rgb_frame = self._read_image(imgpath)
        self._faces_mesh(rgb_frame, label)
        self._clear()
        return self.fd


    def _reset(self) :
        self.fd = FaceData()
        self.tmppath = None


    def _clear(self) :
        if os.path.exists(self.tmppath) :
            os.remove(self.tmppath)


    def _read_image(self, imgpath) :
        '''
        读取图像参数
        [params] imgpath: 图像路径
        [return]: None （参数太多且需要交叉引用，临时存储到类变量 FaceData）
        '''
        self.fd.name, suffix, self.fd.image_id, self.tmppath = upload(imgpath, SETTINGS.tmp_dir)
        self.fd.frame = cv2.imread(self.tmppath)                      # 原图（彩色）
        rgb_frame = cv2.cvtColor(self.fd.frame, cv2.COLOR_BGR2RGB)    # 图片转换到 RGB 通道（反色）
        self.fd.width, self.fd.height = get_shape_size(rgb_frame)     # 图像宽高
        return rgb_frame

    
    def _faces_mesh(self, rgb_frame, label) :
        '''
        检测图像中所有人脸网格
        [params] rgb_frame: 读取的图像数据（RGB 通道）
        [params] label: 是否缓存地标坐标
        [return]: None
        '''
        results = self.face_mesh.process(rgb_frame)                                 # 图像检测
        for landmarks_id, landmarks in enumerate(results.multi_face_landmarks):     # 枚举从图像中检测到的每一个人脸
            self._face_mesh(landmarks_id, landmarks, label)


    def _face_mesh(self, landmarks_id, landmarks, label) :
        '''
        检测单个人脸网格
        [params] landmarks_id: 人脸网格编号
        [params] landmarks: 人脸网格数据
        [params] label: 是否缓存地标坐标
        [return]: None
        '''
        if label :
            # 人脸关键点-468 地标（归一化坐标）
            self.normalized_fkp468_coords = self._get_face_feature(landmarks, True)

            # 人脸关键点-468 地标
            self.fkp468_coords = self._get_face_feature(landmarks, False)

        # 保存图像
        self._save_image(landmarks_id, landmarks)


    def _get_face_feature(self, landmarks, normalized=True) :
        '''
        提取人脸网格 468 个关键点的地标
        [params] landmarks: 人脸网格数据
        [params] normalized: 是否获取归一化坐标（默认是）
        [return] 468 个关键点地标（深度不取）
            [
                [x0, y0],   
                [x1, y1], 
                ... ...
                [x467, y467],
            ]
        '''
        width = 1 if normalized else self.fd.width
        height = 1 if normalized else self.fd.height
        desc = "（归一化）" if normalized else ''

        log.debug(f'人脸网格关键点-468 地标{desc}: ')
        fkp_coords = []
        for id, lm in enumerate(landmarks.landmark) :
            x = lm.x * width
            y = lm.y * height
            # z = lm.z       # 深度不取
            fkp_coords.append([x, y])
            log.debug(f'  {id}: [{x}, {y}]')
        return fkp_coords
        

    def _save_image(self, landmarks_id, landmarks) :
        '''
        保存标注人脸边框和关键点的图像
        [params] landmarks_id: 人脸网格编号
        [params] landmarks: 人脸网格数据
        [return] 方框的左上角和右下角坐标
            [ 
                [x-left, y-upper],  
                [x-right, y-down] 
            ]
        '''
        annotated_frame = self.fd.frame.copy()                          # 复制原图
        self.mp_drawing.draw_landmarks(                                 # 绘制标注
            image = annotated_frame,                                    # 需要画图的原始图片
            landmark_list = landmarks,                                  # 检测到的人脸坐标
            connections = self.mp_face_mesh.FACEMESH_TESSELATION,       # 连接线绘制完全网格，需要把那些坐标连接起来
            # connections = self.mp_face_mesh.FACEMESH_CONTOURS,        # 仅连接外围边框，内部点不连接
            landmark_drawing_spec = self.drawing_landmark,              # 坐标的颜色，粗细
            connection_drawing_spec= self.drawing_line                  # 连接线的粗细，颜色等
        )
        show_image(annotated_frame)

        # 显示并保存图像
        savepath = '%s/%s-%s%s' % (SETTINGS.mesh_dir, self.fd.image_id, landmarks_id, SETTINGS.image_format)
        save_image(annotated_frame, savepath)

        # 缓存数据
        self.fd.detection_frame = annotated_frame
        self.fd.detection_path = savepath
