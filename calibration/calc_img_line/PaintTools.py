import cv2

class PaintTools:
    def __init__(self):
        pass

    def paint_circle(self, point, img):
        radius = int(img.shape[0]*0.005)
        color = (0,0,225)
        thickness = -1
        cv2.circle(img, point, radius, color, thickness)
        return img