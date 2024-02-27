"""
画像に点(円)を描画する関数
"""
import cv2

class PaintCircle:
    def __init__(self):
        pass

    def paint_circle(self, point, img):
        radius = int(img.shape[0]*0.030)
        color = (0,0,225)
        thickness = -1
        cv2.circle(img, point, radius, color, thickness)
        return img