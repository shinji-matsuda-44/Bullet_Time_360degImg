"""
注視点の三次元復元を行う関数
注視点の指定数は可変
"""
import numpy as np

class CalcViewPoint:
    def __init__(self, list_view_point, list_camera_matrix, scale_param):
        self.list_view_point = list_view_point
        self.list_camera_matrix = list_camera_matrix
        self.scale_param = scale_param

    def calc_view_point(self):
        print("注視点を計算 ... ")

        T = np.array([]).reshape(0,3)
        p = np.array([]).reshape(0,1)

        for i in range(len(self.list_view_point)):
            if self.list_view_point[i] is None:
                continue

            f = self.scale_param
            x = self.list_view_point[i][0]
            y = self.list_view_point[i][1]
            P = self.list_camera_matrix[i]
            
            new_row_T = np.array([[f*P[0][0]-x*P[2][0], f*P[0][1]-x*P[2][1], f*P[0][2]-x*P[2][2]],
                                  [f*P[1][0]-y*P[2][0], f*P[1][1]-y*P[2][1], f*P[1][2]-y*P[2][2]]])
            T = np.vstack((T, new_row_T))
            
            new_row_p = np.array([[f*P[0][3]-x*P[2][3]], 
                                  [f*P[1][3]-y*P[2][3]]])
            p = np.vstack((p, new_row_p))

        view_point_3D = np.dot(np.linalg.inv(np.dot(T.T,T)), np.dot(T.T,-p))
        print(view_point_3D)
        print("計算完了")

        return view_point_3D