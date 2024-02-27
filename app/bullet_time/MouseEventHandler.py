import cv2

class MouseEventHandler:
    def __init__(self):
        self.clicked_point = (0, 0)  # クリックされた座標を保持するメンバ変数

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x)
            self.clicked_point = (x, y)
    
    def get_clicled_point(self):
        return self.clicked_point