"""
画像上の座標を指定・取得するGUI
"""

import cv2
import numpy as np
from bullet_time import MouseEventHandler
from bullet_time import PaintCircle

class GetPoint:
    def __init__(self, img, num_points=1, comment=None):
        self.img = img
        self.num_points = num_points
        self.comment = comment

    def get_point(self):
        point_list = []

        for i in range(self.num_points):
            #GUIを表示
            prev_center = (0,0)
            has_data = False
            if self.comment:
                window_name = f"click and mark a point : {i+1}/{self.num_points}   /   Click 'S' to save   /   {self.comment}"
            else:
                window_name = f"click and mark a point : {i+1}/{self.num_points}   /   Click 'S' to save"
            print(window_name)
            mouse_handler = MouseEventHandler.MouseEventHandler()
            paint_circle = PaintCircle.PaintCircle()
            painting_img = self.img

            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window_name, mouse_handler.handle_mouse)
            cv2.imshow(window_name, self.img)
            #キーボード入力の「s」以外ではウィンドウは閉じられない。
            while (True):
                center = mouse_handler.get_clicled_point()
                if center != prev_center:
                    has_data = True
                    print(center)
                    prev_center = center
                    painting_img = paint_circle.paint_circle(center, np.copy(self.img))
                    cv2.imshow(window_name, painting_img)
                else:
                    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                    cv2.setMouseCallback(window_name, mouse_handler.handle_mouse)
                    cv2.imshow(window_name, painting_img)
                if cv2.waitKey(1) == ord("s"):
                    if has_data == False:
                        print("点を打って下さい")
                        continue
                    point_list.append(list(center))
                    break
            cv2.destroyAllWindows()

        return point_list