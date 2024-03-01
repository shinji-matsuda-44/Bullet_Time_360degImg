#########################################
#キャリブレーションに光軸方向を変更した透視投影画像を使った場合、
#光軸方向を変更しなかったときの回転行列と並進ベクトルを計算する。
#線特徴量の多い方向でキャリブレーションしたいときに、光軸方向を変更した画像を用いることを想定
##########################################
import os
import sys
import math
import numpy as np
import datetime

def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

def main(args):
    rotation_matrix = np.loadtxt(args[1], delimiter = ',')
    translation_vector = np.loadtxt(args[2], delimiter = ',')
    sight_rotation_matrix = np.loadtxt(args[3], delimiter = ',')
    folder = args[4]

    fixed_rotation_matrix = np.dot(sight_rotation_matrix, rotation_matrix)
    fixed_translation_vector = np.dot(sight_rotation_matrix, translation_vector)

    #フォルダを作成
    """
    now = datetime.datetime.now()
    folder_name = now.strftime('%m%d_%H%M')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    """

    if not os.path.exists(folder):
        os.makedirs(folder)

    #回転行列を保存
    np.savetxt(folder + "/fixed_" + args[1], fixed_rotation_matrix, delimiter =',')
    np.savetxt(folder + "/fixed_" + args[2], fixed_translation_vector, delimiter =',')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('引数の数が正しくありません。以下3点を指定してください')
        print("1. 姿勢推定した結果の回転行列")
        print("2. 姿勢推定した結果の並進ベクトル")
        print("3. 光軸回転に使用した回転行列")
        print("4. 出力するフォルダ名")
        sys.exit(1)
    else:
        main(sys.argv)