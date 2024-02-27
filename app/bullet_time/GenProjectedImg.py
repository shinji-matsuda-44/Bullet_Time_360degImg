"""
透視投影画像の生成を行うプログラム
以下処理手順
1.全方位画像上に指定した座標を透視投影画像の画像中心とする光軸回転の計算
2.光軸の回転行列の計算
3.透視投影画像の生成
"""

import cv2
import math
import numpy as np
from bullet_time import Rotation
from bullet_time import GetPoint
from bullet_time import ConvTool

class GenProjectedImg:
    def __init__(self, img, THETA, PHI, theta_eye=None, phi_eye=None, psi_eye=0, zoom_level=1):
        self.img = img
        self.THETA = THETA
        self.PHI = PHI
        self.theta_eye = theta_eye
        self.phi_eye = phi_eye
        self.psi_eye = psi_eye
        self.zoom_level = zoom_level

    #透視投影画像の生成
    def generateImg(self):
        #計算に用いる関数群
        convTool = ConvTool.ConvTool()

        #正距円筒画像の読み込み
        cylinder_img = cv2.imread(self.img, cv2.IMREAD_COLOR) 
        
        #入力画像（正距円筒画像）のサイズ
        He = cylinder_img.shape[0]
        We = cylinder_img.shape[1]

        #出力画像（透視投影画像）のサイズの自動調整
        Wp = 2*math.tan(self.THETA/2)*(We/(2*math.pi))
        Wp = int(Wp)
        Hp = 2*math.tan(self.PHI/2)*(He/math.pi)
        Hp = int(Hp)

        #GUIから光軸方向を指定
        if(self.theta_eye is None and self.phi_eye is None):
            GP = GetPoint.GetPoint(cylinder_img, comment="Set line of sight")
            point_list = GP.get_point()
            theta_eye, phi_eye = \
                convTool.coordinate2angle(point_list[0][0], point_list[0][1], We, He)
        else:
            theta_eye, phi_eye = self.theta_eye, self.phi_eye

        psi_eye = self.psi_eye

        #空の透視投影画像
        projected_img = np.zeros([Hp, Wp, 3])  #projected_img

        #画像生成
        print("---------------")
        print("正距円筒画像サイズ：" + str(cylinder_img.shape))
        print("透視投影画像サイズ：" + str(projected_img.shape))
        print("透視投影画像画像生成中...")

        #画素間の長さを計算(アルゴリズムの1)
        #画素間の長さを変化させることで、疑似的にカメラを移動する。
        print(f"zoom level = {self.zoom_level}")
        dx = 2/self.zoom_level*math.tan(self.THETA/2)/Wp
        dy = 2/self.zoom_level*math.tan(self.PHI/2)/Hp
        print(f"dx = {dx}")
        print(f"dy = {dy}")

        #回転行列を計算
        R = Rotation.Rotation(theta_eye, phi_eye, psi_eye)
        R_theta_phi = R.calc_R_theta_phi() #x,y軸を回転軸とする回転行列
        camera_view_axis = np.array([0,0,1]).T #光軸
        rotated_view_axis = np.dot(R_theta_phi, camera_view_axis) #光軸を回転する
        R_psi = R.calc_R_psi(rotated_view_axis) #z軸を回転軸とする回転行列
        sight_rotation_matrix = np.dot(R_psi, R_theta_phi) #全ての回転

        #画素の対応付け(アルゴリズムの2〜4)
        for up in range(Wp):
            for vp in range(Hp):
                sight_vector = convTool.coordinate2vector(up, vp, Wp, Hp, dx, dy) #視線ベクトル
                rotated_sight_vector = np.dot(sight_rotation_matrix, sight_vector)
                theta, phi = convTool.vector2angle(rotated_sight_vector) #角度の計算
                ue, ve = convTool.angle2coordinate(theta, phi, We, He) #cylinder_imgの対応する画素
                projected_img[vp, up] = cylinder_img[int(ve), int(ue)]

        return projected_img, sight_rotation_matrix
