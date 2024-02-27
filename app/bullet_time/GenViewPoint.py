import os
import glob
import numpy as np
from bullet_time import CalcViewPoint
from bullet_time import ConvExternalMatrix

class GenViewPoint:
    def __init__(
            self,
            img_folder,
            external_folder,
            internal_folder,
            list_view_point,
            list_sight_rotation_matrix
    ):
        self.img_folder = img_folder
        self.external_folder = external_folder
        self.internal_folder = internal_folder
        self.list_view_point = list_view_point
        self.list_sight_rotation_matrix = list_sight_rotation_matrix

    def generate_view_point(self):
        list_img_file = glob.glob(os.path.join(self.img_folder, '*.jpg'))
        list_external_folder = glob.glob(os.path.join(self.external_folder,'*'))
        list_internal_file = glob.glob(os.path.join(self.internal_folder,'*.txt'))

        #注視点の三次元復元に用いるデータリスト
        list_view_point = self.list_view_point
        list_camera_matrix = []
        #生成時の光軸回転
        list_sight_rotation_matrix = self.list_sight_rotation_matrix

        #external_matrix_listに格納するカメラ行列を計算
        for i in range(len(list_img_file)):
            if list_view_point[i] is None:
                list_camera_matrix.append(None)
                continue

            #(fixed_)rotation_matrix.txtと(fixed_)translation_vector.txtの読み込み
            if os.path.exists(os.path.join(list_external_folder[i], 'rotation_matrix.txt')):
                path_rotation_file = os.path.join(list_external_folder[i], 'rotation_matrix.txt')
            else:
                path_rotation_file = os.path.join(list_external_folder[i], 'fixed_rotation_matrix.txt')

            if os.path.exists(os.path.join(list_external_folder[i], 'translation_vector.txt')):
                path_translation_file = os.path.join(list_external_folder[i], 'translation_vector.txt')
            else:
                path_translation_file = os.path.join(list_external_folder[i], 'fixed_translation_vector.txt')

            rotation_matrix = np.loadtxt(path_rotation_file, delimiter=',')
            translation_vector = np.loadtxt(path_translation_file, delimiter = ',')
            internal_matrix = np.loadtxt(list_internal_file[i], delimiter = ',')
            sight_rotation_matrix = list_sight_rotation_matrix[i]

            rotation_matrix = np.dot(sight_rotation_matrix.T, rotation_matrix)
            translation_vector = np.dot(sight_rotation_matrix.T, translation_vector)

            CEM = ConvExternalMatrix.ConvExternalMatrix()
            external_matrix = CEM.conv_external_matrix(rotation_matrix, translation_vector)
            camera_matrix = np.dot(internal_matrix, external_matrix)
            list_camera_matrix.append(camera_matrix)

        #注視点を三次元復元
        scale_param = 1
        CVP2 = CalcViewPoint.CalcViewPoint(list_view_point, list_camera_matrix, scale_param)
        view_point_3D = CVP2.calc_view_point()
        
        return view_point_3D