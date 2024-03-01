import cv2
import numpy as np
import MouseEventHandler
import PaintTools

class GetLine:
    def __init__(self, fname):
        self.fname = fname

    def get_line(self, line_count):
        point_list = []
        img = cv2.imread(self.fname)

        for i in range(2):
            #GUIを表示
            prev_point = (0,0)
            txt = "line{} click and mark a point : {}/2"
            window_name = txt.format(line_count, i+1)
            print(window_name)
            mouse_handler = MouseEventHandler.MouseEventHandler()
            paint_tools = PaintTools.PaintTools()

            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window_name, mouse_handler.handle_mouse)
            cv2.imshow(window_name, img)
            while (True):
                point = mouse_handler.get_clicled_point()
                if point != prev_point:
                    print(point)
                    prev_point = point
                    painting_img = paint_tools.paint_circle(point, np.copy(img))
                    if i == 1:
                        cv2.line(painting_img, point, np.array(point_list[0]), (0, 0, 225), thickness=1)
                    cv2.imshow(window_name, painting_img)
                if cv2.waitKey(1) == ord("q"):
                    point_list.append(list(point))
                    img = paint_tools.paint_circle(point, img)
                    break
            cv2.destroyAllWindows()

        return point_list