import os
import sys
import cv2
import numpy as np
import datetime
import GetLine
import CalcImgLine

def calc_focal_len(txt_fname):
    mtx = np.loadtxt(txt_fname, delimiter =',')
    fx = mtx[0][0]
    fy = mtx[1][1]
    f = (fx + fy)/2
    return f

def main(args):
    picture_fname = args[1]
    num_lines = int(args[2])
    txt_fname = args[3]
    focal_len = calc_focal_len(txt_fname)
    GL = GetLine.GetLine(picture_fname)
    CIL = CalcImgLine.ClacImgLine()
    coefficient_list = []
    img = cv2.imread(picture_fname)
    
    for i in range(num_lines):
        point_list = GL.get_line(i+1) #GUIより点を取得
        coefficient_list.append(CIL.get_line(point_list, focal_len, img.shape))
        x1, y1, x2, y2 = \
            point_list[0][0], point_list[0][1], point_list[1][0], point_list[1][1]
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 225), thickness=1)

    #フォルダを生成
    tmp = picture_fname.split(".")
    now = datetime.datetime.now()
    folder_name = now.strftime('output_data/%m%d_%H%M_' + tmp[0])
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    #txtファイルで保存
    f = open(folder_name + "/img_line.txt", 'w')
    f.write(str(num_lines) + '\n')
    for coefficients in coefficient_list:
        f.write(str(coefficients[0]) + ' ')
        f.write(str(coefficients[1]) + ' ')
        f.write(str(coefficients[2]) + '\n')
    f.close()
    
    #jpgで保存
    cv2.imwrite(folder_name + '/painted_img.jpg', img)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('引数の数が正しくありません。以下3点を指定してください')
        print("1. 線分をとる画像ファイルのファイル名")
        print("2. 指定する線の数")
        print("3. 内部パラメータ行列のテキストファイル(internal_matrix.txt)")
        sys.exit(1)
    else:
        main(sys.argv)