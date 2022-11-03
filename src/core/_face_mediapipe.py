#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------

import os
import uuid
import cv2
import mediapipe as mp
import numpy as np
import tkinter
from tkinter import filedialog
from color_log.clog import log
from pypdm.dbc._sqlite import SqliteDBC
from src.dao.t_face_feature import TFaceFeatureDao
from src.config import SETTINGS, FEATURE_SPLIT


EXIT_KEY = 'q'          # 退出 CV 绘制窗口的按键
SAVE_KEY = 's'          # 保存 CV 绘制窗口的按键
FILETYPE = [            # 设置文件对话框会显示的文件类型
    ('all files', '.*'), 
    ('image files', '.jpg'), 
    ('image files', '.jpeg'), 
    ('image files', '.png'), 
    ('image files', '.bpm')
]


class FaceMediapipe :

    def __init__(self, args,
        model_selection=0, static_image_mode=False, 
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) -> None:
        '''
        构造函数
        [param] args: main 入参
        [param] model_selection: 距离模型:  0:短距离模式，适用于 2 米内的人脸; 1:全距离模型，适用于 5 米内的人脸
        [param] static_image_mode: 人脸识别场景:  True:静态图片; False:视频流
        [param] min_detection_confidence: 人脸检测模型的最小置信度值
        [param] min_tracking_confidence: 跟踪模型的最小置信度值（仅视频流有效）
        '''
        self.args = args
        self.MAX_NUM_FACES = 1                                      # 检测人脸个数，此场景下只取 1 个人脸
        self.mp_drawing = mp.solutions.drawing_utils                # 导入绘制辅助标记的工具（此为 mediapipe 的，不是 opencv 的）
        self.resize_face = (SETTINGS.face_width, SETTINGS.face_height)
        self.sdbc = SqliteDBC(options=SETTINGS.database)
        self.dao = TFaceFeatureDao()

        self.mp_face_detection = mp.solutions.face_detection        # 导入人脸检测模块
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection = model_selection, 
            min_detection_confidence = min_detection_confidence
        )

        self.mp_face_mesh = mp.solutions.face_mesh                  # 导入人脸识别模块
        self.face_mesh = self.mp_face_mesh.FaceMesh(                # 定义一个 mesh 人脸检测器
            static_image_mode = static_image_mode,         
            max_num_faces = self.MAX_NUM_FACES,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )


    def _open_select_one_window(self, title="Please select one file:") :
        '''
        打开系统选择文件窗口（选择一个文件）
        [param] title: 窗口标题
        :return: 选择的文件路径
        '''
        tk = tkinter.Tk()
        tk.withdraw()     # 隐藏 tk 窗体
        filepath = filedialog.askopenfilename(
            initialdir = os.getcwd(),
            title = title,
            filetypes = FILETYPE
        )
        tk.destroy()      # 销毁 tk 窗体
        return filepath


    def _open_select_multi_window(self, title="Please select one or more files:") :
        '''
        打开系统选择文件窗口（选择多个文件）
        [param] title: 窗口标题
        :return: 选择的文件路径
        '''
        tk = tkinter.Tk()
        tk.withdraw()     # 隐藏 tk 窗体
        filepaths = filedialog.askopenfilenames(
            initialdir = os.getcwd(),
            title = title,
            filetypes = FILETYPE
        )
        tk.destroy()      # 销毁 tk 窗体
        return filepaths


    def _gen_image_params(self, imgpath) :
        filename = os.path.split(imgpath)[-1]
        name = os.path.splitext(filename)[0]
        suffix = os.path.splitext(filename)[-1]
        image_id = self._gen_image_id()
        return (name, suffix, image_id)


    def _gen_image_id(self) :
        '''
        生成图像的唯一 ID
        :return: 图像 ID
        '''
        return uuid.uuid1().hex

    
    def _open_camera(self) :
        image_id = self._gen_image_id()
        imgpath = "%s/%s%s" % (SETTINGS.original_dir, image_id, SETTINGS.feature_fmt)

        capture = self._init_camera()
        is_open = capture.isOpened()
        if is_open :
            log.info('加载摄像头的数据流成功（按 <%s> 退出，按 <%s> 确认）' % (EXIT_KEY, SAVE_KEY))
        else :
            imgpath = None
            log.info('加载摄像头的数据流失败（请确认没有其他程序在读取该数据流）')
        while is_open:
            is_open, input_frame_data = capture.read()
            if not is_open:
                continue

            mirror_frame_data = cv2.flip(input_frame_data, 1)   # 镜像翻转画面
            frame_data = cv2.cvtColor(mirror_frame_data, cv2.COLOR_BGR2RGB)

            results = self.face_detection.process(frame_data)
            if not results.detections:
                log.warn("检测人脸位置失败")
                continue

            detection = results.detections[0]   # 此场景下只取 1 张人脸
            image = cv2.cvtColor(frame_data.copy(), cv2.COLOR_RGB2BGR)  # 恢复彩色通道

            if self.args.record or SETTINGS.show_video :
                annotated_image = image.copy()
                self.mp_drawing.draw_detection(annotated_image, detection)        # 添加 mediapipe 的标注
                cv2.imshow('Preview Frame Face; Exit <q>; Save <s>', annotated_image)

                press = cv2.waitKey(1) & 0xFF
                if press == ord(SAVE_KEY) :
                    cv2.imwrite(imgpath, image)
                    break
                elif press == ord(EXIT_KEY) :
                    imgpath = None
                    break
            else :
                cv2.imwrite(imgpath, image)
                break
        
        capture.release()   # 释放视频设备句柄
        return [ imgpath ]


    def _init_camera(self) :
        log.info('正在打开视频设备（索引号=%d） ...' % SETTINGS.dev_idx)
        capture = cv2.VideoCapture(SETTINGS.dev_idx)    # 初始化设备时间较长
        capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*SETTINGS.fourcc))
        capture.set(cv2.CAP_PROP_FPS, SETTINGS.fps)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, SETTINGS.frame_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, SETTINGS.frame_height)

        log.info('摄像头输入参数：')
        log.info('  视频编码（fourcc/codec）= %d' % int(capture.get(cv2.CAP_PROP_FOURCC)))
        log.info('  帧速率（FPS）= %d' % int(capture.get(cv2.CAP_PROP_FPS)))
        log.info('  帧宽度（width）= %d' % int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
        log.info('  帧高度（height）= %d' % int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return capture


    def _to_alignment(self, image) :
        '''
        人脸对齐：从图像中检测人脸，映射/旋转/缩放/裁剪关键点到特定位置和相同尺寸
        [param] image: 原始图像
        :return: frame_image 对齐的人脸图像; 若检测失败返回 None
        '''
        frame_image = None
        results = self.face_detection.process(image)
        if not results.detections:
            log.warn("检测人脸位置失败")
            return frame_image

        detection = results.detections[0]               # 此场景下只取 1 张人脸
        location_data = detection.location_data
        if location_data.format == location_data.RELATIVE_BOUNDING_BOX:
            box = location_data.relative_bounding_box   # 得到检测到人脸位置的方框标记（坐标是归一化的）
            width, height = self._get_shape_size(image) # 原图的宽高

            # 计算人脸方框的原始坐标
            left = int(box.xmin * width)
            upper = int(box.ymin * height)
            right = int((box.xmin + box.width) * width)
            down = int((box.ymin + box.height) * height)

            corp_image = image[upper:down, left:right]  # 裁剪图像，仅保留方框人脸部分
            frame_image = cv2.resize(corp_image, 
                self.resize_face, 
                interpolation = cv2.INTER_CUBIC
            )

        # 绘制检测到的人脸方框
        if self.args.record or SETTINGS.show_image :
            annotated_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2BGR) # 恢复彩色通道
            self.mp_drawing.draw_detection(annotated_image, detection)      # 添加 mediapipe 的标注
            cv2.imshow('Preview Frame Face; Exit <Any Key>', annotated_image)
            cv2.waitKey(0)
        return frame_image


    def _get_shape_size(self, image) :
        '''
        获取图像的宽高
        [param] image: CV 载入的图像
        :return: (width, height)
        '''
        height = 0
        width = 0
        if image is not None :
            size = image.shape
            height = size[0]
            width = size[1]
        return (width, height)


    def calculate_feature(self, image) :
        '''
        计算人脸特征值
        [param] image: 对齐的人脸图像
        :return: 特征值
        '''
        feature = []
        log.info("开始计算人脸特征值 ...")

        # 使用 face_mesh 计算人脸 468 个点的三维地标（坐标是归一化的）
        results = self.face_mesh.process(image)
        if not results.multi_face_landmarks:
            log.warn("拟合人脸网格失败")
            return feature

        coords = self._to_coords(results.multi_face_landmarks[0].landmark)
        feature = self._to_feature(coords)
        return feature


    def _to_coords(self, landmark) :
        '''
        把 人脸特征点的地标 转换为 (x,y,z) 坐标数组
        [param] landmark: 人脸特征点的地标
        :return: (x,y,z) 坐标数组（归一化）
        '''
        points = np.array(landmark)

        # 分别获取特征点 (x,y,z) 坐标
        points_x = np.array(list(p.x for p in points))
        points_y = np.array(list(p.y for p in points))
        points_z = np.array(list(p.z for p in points))

        # 将三个方向坐标合并
        coords = np.vstack((points_x, points_y, points_z)).T
        return coords


    def _to_feature(self, coords) :
        '''
        计算 坐标数组 的 特征值
        [param] coords: (x,y,z) 坐标数组（归一化）
        :return: 特征值
        '''
        # feature = []
        # size = len(coords)
        # group_num = size / 3                        # 每 3 个坐标一组，分别组成方阵
        # groups = np.array_split(coords, group_num)
        # for group in groups :                       # 迭代每组方阵
        #     eigen, vector = np.linalg.eig(group)    # 计算 特征值(1x3矩阵) 和 特征向量(3x3矩阵)
        #     feature.extend(eigen)                   # 串接 特征值
        # return feature

        size = len(coords)
        feature = []
        for i in range(size - 1) :
            a = coords[i]
            b = coords[i + 1]
            d = np.linalg.norm(a - b)
            feature.append(d)

        a = coords[size - 1]
        b = coords[0]
        d = np.linalg.norm(a - b)
        feature.append(d)
        return feature


    def _feature_to_str(self, feature) :
        '''
        特征值（复数数组）转 字符串
        [param] feature: 特征值
        :return: 字符串
        '''
        return FEATURE_SPLIT.join(str(v) for v in feature)


    def _log(self, desc, feature, debug=False) :
        msg = "%s: [%s ... %s]" % (desc, feature[0], feature[-1])
        if debug :
            log.debug(msg)
        else :
            log.info(msg)

