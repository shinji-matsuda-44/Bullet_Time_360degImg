"""
回転行列と並進ベクトルから外部パラメータ行列を作成
M = (R|t)
* P=AM のように使用 (ただしPはカメラ行列, Aは内部パラメータ行列)
"""
import numpy as np

class ConvExternalMatrix:
    def __init__(self):
        pass

    def conv_external_matrix(self, rotation_matrix, translational_vector):
        R = rotation_matrix
        t = translational_vector.reshape(-1,1)
        return np.concatenate([R,t],1)