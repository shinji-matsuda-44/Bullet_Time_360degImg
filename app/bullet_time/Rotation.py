# -*- coding: utf-8 -*-
"""
回転行列の計算に関する関数
"""

import numpy as np
import math

class Rotation:
    def __init__(self, theta_eye, phi_eye, psi_eye):
        self.theta_eye = theta_eye
        self.phi_eye = phi_eye
        self.psi_eye = psi_eye

    def calc_R_theta_phi(self):
        #y軸周りの回転行列
        cos_theta = math.cos(self.theta_eye)
        sin_theta = math.sin(self.theta_eye)
        A = np.array([[cos_theta, 0, sin_theta],
                      [0, 1, 0],
                      [-sin_theta, 0, cos_theta]])

        #x軸周りの回転行列
        cos_phi = math.cos(self.phi_eye)
        sin_phi = math.sin(self.phi_eye)
        B = np.array([[1, 0, 0],
                      [0, cos_phi, -sin_phi],
                      [0, sin_phi, cos_phi]])
        
        #X軸周りに回転した後、y軸周りに回転する回転行列
        R_theta_phi = np.dot(A, B)

        return R_theta_phi

    def calc_R_psi(self, rotated_view_axis):
        rotated_view_axis_norm = np.linalg.norm(rotated_view_axis)
        l = rotated_view_axis / rotated_view_axis_norm #回転軸方向の単位ベクトル
        lx, ly, lz = l[0], l[1], l[2]

        #z軸周りの回転行列
        cos_psi = math.cos(self.psi_eye)
        sin_psi = math.sin(self.psi_eye)
        R_psi = np.array([[lx*lx*(1-cos_psi)+cos_psi, lx*ly*(1-cos_psi)-lz*sin_psi, lz*lx*(1-cos_psi)+ly*sin_psi],
                          [lx*ly*(1-cos_psi)+lz*sin_psi, ly*ly*(1-cos_psi)+cos_psi, ly*lz*(1-cos_psi)-lx*sin_psi],
                          [lz*lx*(1-cos_psi)-ly*sin_psi, ly*lz*(1-cos_psi)+lx*sin_psi, lz*lz*(1-cos_psi)+cos_psi]])

        return R_psi