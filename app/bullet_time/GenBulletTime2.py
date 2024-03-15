"""
バレットタイム映像生成
・仮想的なカメラ位置移動によるスケーリングを行う
・光軸方向による視線方向の設定
"""
import os
import cv2
import glob
import math
import subprocess
import numpy as np
from bullet_time import GenProjectedImg
from bullet_time import PaintCircle
from bullet_time import ConvExternalMatrix2
from bullet_time import GenerateGIF
from bullet_time import ConvTool

class GenBulletTime2:
    def __init__(self, img_folder, external_folder, view_point_3D):
        self.img_folder = img_folder
        self.external_folder = external_folder
        self.view_point_3D = view_point_3D

    def read_param(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                label, value = line.strip().split(': ')
                if label == '横方向の画角':
                    THETA = math.radians(float(value))
                if label == '縦方向の画角':
                    PHI = math.radians(float(value))
        return THETA, PHI

    def generate_bullet_time(self):
        path_img_files = glob.glob(os.path.join(self.img_folder,'*.jpg'))
        path_external_folders = glob.glob(os.path.join(self.external_folder,'*'))
        view_point_3D = self.view_point_3D

        THETA, PHI = self.read_param("bullet_time/viewingAngle.txt")
        convTool = ConvTool.ConvTool()

        # 隠れフォルダのパス
        hidden_folder_path1 = '.hidden_folder1' 
        hidden_folder_path2 = '.hidden_folder2' 

        # 隠れフォルダが存在しない場合は作成する
        if not os.path.exists(hidden_folder_path1):
            os.makedirs(hidden_folder_path1)
            subprocess.run(['attrib', '+h', hidden_folder_path1], check=True) #windowsなら必要
        if not os.path.exists(hidden_folder_path2):
            os.makedirs(hidden_folder_path2)
            subprocess.run(['attrib', '+h', hidden_folder_path2], check=True) #windowsなら必要

        list_rotation_matrix = []
        list_translation_vector = []
        distance_camera_to_viewpoint = []
        for i in range(len(path_img_files)):
            #(fixed_)rotation_matrix.txtと(fixed_)translation_vector.txtの読み込み
            if os.path.exists(os.path.join(path_external_folders[i], 'rotation_matrix.txt')):
                path_rotation_file = glob.glob(os.path.join(path_external_folders[i], 'rotation_matrix.txt'))
            else:
                path_rotation_file = glob.glob(os.path.join(path_external_folders[i], 'fixed_rotation_matrix.txt'))

            if os.path.exists(os.path.join(path_external_folders[i], 'rotation_matrix.txt')):
                path_translation_file = glob.glob(os.path.join(path_external_folders[i], 'translation_vector.txt'))
            else:
                path_translation_file = glob.glob(os.path.join(path_external_folders[i], 'fixed_translation_vector.txt'))

            rotation_matrix = np.loadtxt(path_rotation_file[0], delimiter = ',')
            list_rotation_matrix.append(rotation_matrix)
            translation_vector = np.loadtxt(path_translation_file[0], delimiter = ',')
            list_translation_vector.append(translation_vector)

            #各カメラと注視点までの距離を計算
            camera_position = -np.dot(rotation_matrix.T, translation_vector)
            distance = math.sqrt((view_point_3D[0]-camera_position[0])**2 + \
                                (view_point_3D[1]-camera_position[1])**2 + \
                                (view_point_3D[2]-camera_position[2])**2)
            distance_camera_to_viewpoint.append(distance)

        for i in range(len(path_img_files)):
            rotation_matrix = list_rotation_matrix[i]
            translation_vector = list_translation_vector[i]

            #各画像の拡大・縮小率の計算
            #注視点からカメラまでの距離の逆比を取る
            min_direction = min(distance_camera_to_viewpoint)
            zoom_level = distance_camera_to_viewpoint[i]/min_direction

            #視線の回転を計算
            CEM2 = ConvExternalMatrix2.ConvExternalMatrix2()
            external_matrix = CEM2.conv_external_matrix(rotation_matrix, translation_vector)
            view_point_of_world = np.append(view_point_3D, 1) #同次座標系にする
            view_point_of_camera = np.dot(external_matrix, view_point_of_world) #そのまま光軸方向とする
            sight_vector = (view_point_of_camera[0], view_point_of_camera[1], view_point_of_camera[2])
            theta_eye, phi_eye = convTool.vector2angle(sight_vector)

            #透視投影画像を隠れフォルダへ保存
            path_img = path_img_files[i]
            GPI = GenProjectedImg.GenProjectedImg(path_img, THETA, PHI, theta_eye=theta_eye, phi_eye=phi_eye, \
                                                  zoom_level=zoom_level)
            projected_img, _ = GPI.generateImg()
            cv2.imwrite(os.path.join(hidden_folder_path1, f'no_point_img_{i+1}.jpg'), projected_img)

            PC = PaintCircle.PaintCircle()
            point_projected_img = PC.paint_circle((int(projected_img.shape[1]/2), int(projected_img.shape[0]/2)), projected_img)
            cv2.imwrite(os.path.join(hidden_folder_path2, f'with_point_img_{i+1}.jpg'), point_projected_img)

        #gif画像を隠れフォルダへ保存
        GGIF = GenerateGIF.GenerateGIF()
        GGIF.generateGIF(hidden_folder_path1)
        GGIF.generateGIF(hidden_folder_path2)
        
        return hidden_folder_path1, hidden_folder_path2
    