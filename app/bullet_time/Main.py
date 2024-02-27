"""
注視点の三次元復元を行うプログラム
以下処理手順
1.全方位画像から注視点を指定するための透視投影画像を生成
2.透視投影画像上にて指定した注視点から世界座標における座標を三次元復元
"""

import os
import sys
import cv2
import glob
import math
import datetime
import numpy as np
import GetPoint
import bullet_time.GenProjectedImg as GenProjectedImg
import PaintCircle
import CalcViewPoint
import ConvExternalMatrix


def read_param(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            label, value = line.strip().split(': ')
            if label == '横方向の画角':
                THETA = math.radians(float(value))
            if label == '縦方向の画角':
                PHI = math.radians(float(value))
    return THETA, PHI


def main(args):
    img_folder = args[1]
    external_folder = args[2]
    internal_folder = args[3]

    list_img_file = glob.glob(os.path.join(img_folder, '*.jpg'))
    list_external_folder = glob.glob(os.path.join(external_folder,'*'))
    list_internal_file = glob.glob(os.path.join(internal_folder,'*.txt'))

    #注視画像の画角パラメータの読み込み
    THETA, PHI = read_param("viewingAngle.txt")

    #注視点の三次元復元に用いるデータリスト
    list_view_point = []
    list_camera_matrix = []

    #透視投影画像と生成時の光軸回転
    list_projected_img = []
    list_sight_rotation_matrix = []
    list_is_used = []

    #view_point_listに格納する各画像上での注視点を取得
    for i, img_file in enumerate(list_img_file):
        #注視点指定に使用するか否か
        window_name = "check_picture"
        img = cv2.imread(img_file, cv2.IMREAD_COLOR)
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        while True:
            user_input = input("YesまたはNoを入力してください: ")
            if user_input.lower() == 'yes' or user_input.lower() == 'no':
                break
            else:
                print("YesまたはNoを入力してください。")

        if user_input == 'no':
            list_is_used.append("not used")
            list_projected_img.append(None)
            list_sight_rotation_matrix.append(None)
            list_view_point.append(None)
            continue
        else:
            list_is_used.append("used")

        #全方位画像から注視画像指定に用いる透視投影画像を生成
        GI = GenProjectedImg.GenerateImg(img_file, THETA, PHI)
        projected_img, sight_rotation_matrix = GI.generateImg()
        projected_img = cv2.cvtColor(projected_img.astype(np.uint8), cv2.COLOR_BGR2BGRA) #numpy配列からcv2の画像へ変換
        list_projected_img.append(projected_img)
        list_sight_rotation_matrix.append(sight_rotation_matrix)

        #透視投影画像より注視点を指定
        GP = GetPoint.GetPoint(projected_img)
        view_point = np.array(GP.get_point()[0])
        list_view_point.append(view_point)


    #external_matrix_listに格納するカメラ行列を計算
    for i in range(len(list_img_file)):
        if list_is_used[i] == "not used":
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

    #フォルダを作成
    now = datetime.datetime.now()
    output_folder = now.strftime('%m%d_%H%M')
    output_img_folder = os.path.join(output_folder, 'pointed_imgs')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        os.makedirs(output_img_folder)
    
    #txtファイルで三次元復元した注視点の座標を保存
    np.savetxt(os.path.join(output_folder,'view_point_3D.txt'), view_point_3D)

    #透視投影画像上で指定した注視点のデータを保存    
    PC = PaintCircle.PaintCircle()
    for i, img_file in enumerate(list_projected_img):
        if list_projected_img[i] is None:
            continue
        np.savetxt(os.path.join(output_img_folder, f"view_point_{i+1}.txt"), list_view_point[i])
        img = PC.paint_circle(tuple(list_view_point[i]), img_file)
        cv2.imwrite(os.path.join(output_img_folder, f"check_point_img_{i+1}.jpg"), img)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('引数の数が正しくありません。以下4点を指定してください')
        print("1. 画像群のフォルダ名")
        print("2. 外部パラメータのデータ群のフォルダ名")
        print("3. 内部パラメータのデータ群のフォルダ名")
        sys.exit(1)
    else:
        main(sys.argv)