#########################################
#キャリブレーションに光軸方向を変更した透視投影画像を使った場合、
#光軸方向を変更しなかったときの回転行列と並進ベクトルを計算する。
#線特徴量の多い方向でキャリブレーションしたいときに、光軸方向を変更した画像を用いることを想定
##########################################
import os
import sys
import glob
import math
import numpy as np
import datetime

def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

def main(args):
    input_folder_name = args[1]
    output_folder_name = args[2]
    folder_path = glob.glob(input_folder_name + "/*")

    for i, path in enumerate(folder_path):
        rotation_matrix = np.loadtxt(path + "/rotation_matrix.txt", delimiter = ',')
        translation_vector = np.loadtxt(path + "/translation_vector.txt", delimiter = ',')
        sight_rotation_matrix = np.loadtxt(f"rotation_matrix_{i+1}.txt", delimiter = ',')

        fixed_rotation_matrix = np.dot(sight_rotation_matrix, rotation_matrix)
        fixed_translation_vector = np.dot(sight_rotation_matrix, translation_vector)
   
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
        sub_folder = path.split("\\")[1]
        path_output = os.path.join(output_folder_name, sub_folder)
        if not os.path.exists(path_output):
            os.makedirs(path_output)

        #回転行列を保存

        path_rotation = os.path.join(path_output, "fixed_rotation_matrix.txt")
        path_translation = os.path.join(path_output, "fixed_translation_vector.txt")
        np.savetxt(path_rotation, fixed_rotation_matrix, delimiter =',')
        np.savetxt(path_translation, fixed_translation_vector, delimiter =',')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('引数の数が正しくありません。以下2点を指定してください')
        print("1. 姿勢推定した結果のパラメータフォルダ名")
        print("2. 出力するフォルダ名")
        sys.exit(1)
    else:
        main(sys.argv)