"""
各所で用いる変換式のライブラリ
"""

import math
import numpy as np

class ConvTool:
    def __init__(self):
        pass

    #"透視投影画像"の座標を視線ベクトルへ変換
    def coordinate2vector(self, up, vp, Wp, Hp, dx, dy):
        x = (up - Wp/2)*dx
        y = (vp - Hp/2)*dy
        return np.array([x, y, 1])
    
    def coordinate2vector_V(self, up, vp, Wp, Hp, dx, dy, zoom_level):
        x = (up - Wp/2)*dx
        y = (vp - Hp/2)*dy
        return np.array([x, y, 1+1/zoom_level])

    #視線ベクトルを光軸からの角度へ変換
    def vector2angle(self, X):
        x, y, z = X[0], X[1], X[2]
        theta = math.atan2(x, z)
        phi = -math.atan2(y, math.sqrt(x*x + z*z))
        return theta, phi

    #角度を"正距円筒画像"の座標へ変換
    def angle2coordinate(self, theta, phi, We, He):
        ue = (theta + math.pi)*We/(2*math.pi)
        ve = (math.pi/2 - phi)*He/math.pi
        return ue, ve

    #"正距円筒画像"の座標を角度へ変換
    def coordinate2angle(self, ue, ve, We, He):
        theta = (ue - We/2)*(2*math.pi/We)
        phi = (He/2 - ve)*(math.pi/He)
        return theta, phi
    
    #カメラ行列の作成
    def create_external_matrix(self, rotation_matrix, translational_vector):
        R = rotation_matrix
        t = translational_vector.reshape(-1,1)
        return np.concatenate([R,t],1)
    