#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------


class FaceData :
    '''
    人脸缓存数据（目前只支持单人）
    '''

    def __init__(self) -> None:
        self.name = None                            # 图像文件名
        self.image_id = None                        # 分配的图像 ID
        self.bgr_frame = None                       # 原始图像数据（BGR 通道，彩色）
        self.rgb_frame = None                       # 原始图像数据（RGB 通道，反色）
        self.imgpath = None                         # 原始图像存储位置
        self.width = 0                              # 图像宽度
        self.height = 0                             # 图像高度

        self.detection_frame = None                 # 人脸标注后的图像数据
        self.detection_path = None                  # 人脸标注后的图像存储位置
        self.normalized_box_coords = []             # 人脸边界框地标（归一化坐标）
        self.box_coords = []                        # 人脸边界框地标（原始比例坐标）
        self.normalized_fkp6_coords = []            # 人脸关键点-6 地标（归一化坐标）
        self.fkp6_coords = []                       # 人脸关键点-6 地标（原始比例坐标）

        self.mesh_frame = None                      # 人脸网格的图像数据
        self.mesh_path = None                       # 人脸网格的图像存储位置
        self.normalized_fkp468_coords = []          # 人脸关键点-468 地标（归一化坐标）
        self.fkp468_coords = []                     # 人脸关键点-468 地标（原始比例坐标）

        self.alignment_frame = None                 # 人脸对齐后的图像数据
        self.alignment_path = None                  # 人脸对齐后的图像存储位置
        self.feature = None                         # 人脸特征值
        
    
    def copy_BGR(self) :
        frame = None
        if self.bgr_frame is not None :
            frame = self.bgr_frame.copy()
        return frame

    
    def copy_RGB(self) :
        frame = None
        if self.rgb_frame is not None :
            frame = self.rgb_frame.copy()
        return frame


    def __repr__(self) :
        return '\n'.join([
            f'[图像 ID ] {self.image_id}', 
            f'[图像名称] {self.name}', 
            f'[图像宽度] {self.width}', 
            f'[图像高度] {self.height}', 
            f'[原始图像路径] {self.imgpath}', 

            f'[人脸检测路径] {self.detection_path}', 
            self._print_box_coords(self.normalized_box_coords, True), 
            self._print_box_coords(self.box_coords, False), 
            self._print_fkp6_coords(self.normalized_fkp6_coords, True), 
            self._print_fkp6_coords(self.fkp6_coords, False), 

            f'[人脸网格路径] {self.alignment_path}', 
            self._print_fkp468_coords(self.normalized_fkp468_coords, True), 
            self._print_fkp468_coords(self.fkp468_coords, False), 

            f'[人脸对齐路径] {self.alignment_path}', 
            f'[人脸特征值] {self.feature}', 
        ])


    def _print_box_coords(self, box_coords, normalized) :
        desc = "（归一化）" if normalized else ''
        info = []
        info.append(f'[人脸边界框地标{desc}]: ')
        if len(box_coords) == 2 :
            info.append(f'  左上角: {box_coords[0]}')
            info.append(f'  右下角: {box_coords[1]}')
        return '\n'.join(info)


    def _print_fkp6_coords(self, fkp_coords, normalized) :
        desc = "（归一化）" if normalized else ''
        info = []
        info.append(f'[人脸关键点-6 地标{desc}]: ')
        if len(fkp_coords) == 6 :
            info.append(f'  右眼: {fkp_coords[0]}')
            info.append(f'  左眼: {fkp_coords[1]}')
            info.append(f'  鼻尖: {fkp_coords[2]}')
            info.append(f'  嘴中: {fkp_coords[3]}')
            info.append(f'  右耳: {fkp_coords[4]}')
            info.append(f'  左耳: {fkp_coords[5]}')
        return '\n'.join(info)


    def _print_fkp468_coords(self, fkp_coords, normalized) :
        desc = "（归一化）" if normalized else ''
        info = []
        info.append(f'[人脸网格关键点-468 地标{desc}]: ')
        if len(fkp_coords) == 468 :
            for id, coord in enumerate(fkp_coords) :
                info.append(f'  {id}: {coord}')
        return '\n'.join(info)