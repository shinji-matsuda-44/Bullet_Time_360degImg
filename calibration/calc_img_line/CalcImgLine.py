import numpy as np

class ClacImgLine:
    def __init__(self):
        pass

    def get_line(self, point_list, forcal_len, img_shape):
        print("calc line and get coefficients ...")

        W = img_shape[1] #img.shapeの値は(縦, 横, チャネル数)であることに注意
        H = img_shape[0]

        x1, y1, x2, y2 = \
            point_list[0][0], point_list[0][1], point_list[1][0], point_list[1][1]
        #xy座標⇒uv座標(画像中心が原点)へ変換
        u0, v0 = W/2, H/2
        u1, v1, u2, v2 = \
            x1-u0, y1-v0, x2-u0, y2-v0
        #2点の外積としてa,b,cを計算
        A = np.array([x1 - u0, y1 - v0, forcal_len])
        B = np.array([x2 - u0, y2 - v0, forcal_len])
        C = np.cross(A.T, B.T)
        C_norm = np.linalg.norm(C)
        coefficients = C / C_norm

        #計算結果のチェック(内部テスト)
        #ax+by+cに二点の値を代入して解が0になるかを計算
        """
        check_1 = coefficients[0]*u1 + coefficients[1]*v1 + coefficients[2]*forcal_len
        print("check_1 = " + str(check_1))
        check_2 = coefficients[0]*u2 + coefficients[1]*v2 + coefficients[2]*forcal_len
        print("check_2 = " + str(check_2))
        print(coefficients)
        """
        print("end")
        return coefficients