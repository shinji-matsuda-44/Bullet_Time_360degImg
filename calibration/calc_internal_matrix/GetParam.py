# -*- coding: utf-8 -*-

#from sqlite3 import row
import numpy as np
import cv2
import glob
import datetime
import os
import sys

def main(args):
    num_rows = int(args[1]) #チェッカーボードの横方向の交点の数
    num_cols = int(args[2]) #チェッカーボードの縦方向の交点の数
    square_size_cm = float(args[3]) #チェッカーボードのマスの大きさ

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((num_rows*num_cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:num_rows,0:num_cols].T.reshape(-1,2)
    objp *= square_size_cm

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    #make folder
    now = datetime.datetime.now()
    folder_name = now.strftime('%m%d_%H%M%S')
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    images = glob.glob('input_imgs/*.jpg')

    for fname in images:
        print("loading..." + fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (num_rows,num_cols),None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (num_rows,num_cols), corners2,ret)
            #img_name = fname.split("/")[1]
            img_name = fname.split("\\")[1]
            filename = folder_name + '/' + img_name
            cv2.imwrite(filename, img)
        else:
            print('Chessboard not found!')

    # 内部パラメータを計算
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    # 計算結果を表示
    print("RMS = " + str(ret))
    print("mtx = \n" + str(mtx))
    print("dist = "  + str(dist.ravel()))
    # 計算結果を保存
    np.savetxt(folder_name + "/ret.txt", np.array([ret]), delimiter =',',fmt="%0.14f")
    np.savetxt(folder_name + "/mtx.txt", mtx, delimiter =',',fmt="%0.14f")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('引数の数が正しくありません。3つの数値を指定してください。')
        print("1. チェッカーボードの横方向の交点の数")
        print("2. チェッカーボードの縦方向の交点の数")
        print("3. マスの大きさ（cm）")
        sys.exit(1)
    else:
        main(sys.argv)