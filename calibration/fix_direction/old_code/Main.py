#########################################
#キャリブレーションに光軸方向を変更した透視投影画像を使った場合、
#光軸方向を変更しなかったときの回転行列を計算する。
#線特徴量の多い方向でキャリブレーションしたいときに、光軸方向を変更した画像を用いることを想定
##########################################
import os
import sys
import math
import numpy as np
import datetime
import Rotation


def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

def main(args):
    fname_matrix = args[1]
    rotation_matrix = read_txt(args[1])
    theta_eye = math.radians(float(args[2]))
    phi_eye = math.radians(float(args[3]))
    psi_eye = math.radians(float(args[4]))

    #回転行列を計算
    R = Rotation.Rotation(theta_eye, phi_eye, psi_eye)
    Rtp = R.calc_Rtp() #x,y軸を回転軸とする回転行列
    v = np.array([0,0,1]).T #光軸
    Rtp_v = np.dot(Rtp, v) #光軸を回転する
    Rp = R.calc_Rp(Rtp_v) #z軸を回転軸とする回転行列
    RpRtp = np.dot(Rp, Rtp) #全ての回転

    #回転行列を補正(左からかける)
    #fix_external_matrix = np.dot(RpRtp, rotation_matrix)
    #fix_external_matrix = np.dot(RpRtp.T, rotation_matrix)
    fix_external_matrix = np.dot(rotation_matrix, RpRtp)
    #fix_external_matrix = np.dot(rotation_matrix, RpRtp.T)

    #フォルダを作成
    now = datetime.datetime.now()
    folder_name = now.strftime('%m%d_%H%M%S')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    #回転行列を保存
    np.savetxt(folder_name + "/fixed_" + fname_matrix, fix_external_matrix, delimiter =',')

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('引数の数が正しくありません。以下4点を指定してください')
        print("1. 回転行列")
        print("2. y軸周りの回転(theta_eye)の値")
        print("3. x軸周りの回転(phi_eye)の値")
        print("4. z軸周りの回転(psi_eye)の値")
        sys.exit(1)
    else:
        main(sys.argv)