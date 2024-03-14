"""
回転行列と並進ベクトルから外部パラメータ行列を作成
M = (R t
     0 1)
* r_c = Mr_w のように使用
(ただしr_c,r_wはそれぞれカメラ座標系,世界座標系における座標)
"""
import numpy as np

class ConvExternalMatrix2:
    def __init__(self):
        pass

    def conv_external_matrix(self, rotation_matrix, translational_vector):
        R = rotation_matrix
        t = translational_vector
        M = np.array([[R[0][0], R[0][1], R[0][2], t[0]],
                      [R[1][0], R[1][1], R[1][2], t[1]],
                      [R[2][0], R[2][1], R[2][2], t[2]],
                      [0, 0, 0, 1]
                      ])

        return M