import os
import sys
import glob
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

def draw_camera(rotation_matrix, translation_vector, color):
    # カメラの位置
    camera_position = -np.dot(rotation_matrix.T, translation_vector)

    # カメラの姿勢
    x_axis = np.dot(rotation_matrix.T, np.array([1, 0, 0]))
    y_axis = np.dot(rotation_matrix.T, np.array([0, 1, 0]))
    z_axis = np.dot(rotation_matrix.T, np.array([0, 0, 1]))

    # カメラの位置を描画
    ax.scatter(camera_position[0], camera_position[1], camera_position[2], c=color, label=f'Camera {color}')

    # カメラの姿勢を描画
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], x_axis[0], x_axis[1], x_axis[2], color=color, label=f'Camera {color} X-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], y_axis[0], y_axis[1], y_axis[2], color=color, label=f'Camera {color} Y-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], z_axis[0], z_axis[1], z_axis[2], color=color, label=f'Camera {color} Z-Axis')

    #カメラ
def update_cameras():
    #group_1ディレクトリ下のデータを取得
    #folders_1 = glob.glob('group_1/*')
    folders_1 = glob.glob(os.path.join(sys.argv[1],"*"))
    try:
        for i in range(len(folders_1)):
            rotation_matrix = read_txt(os.path.join(folders_1[i], 'fixed_rotation_matrix.txt'))
            tranlational_vector = read_txt(os.path.join(folders_1[i],'fixed_translation_vector.txt'))

            if rotation_matrix is not None and tranlational_vector is not None:
                draw_camera(rotation_matrix, tranlational_vector, "red")
            else:
                error_label.config(text=f"カメラ{i}のファイルの読み込みに問題がありました。")
                return

        canvas.draw()
        error_label.config(text="")
    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")

    #group_2ディレクトリ下のデータを取得
    """
    folders_2 = glob.glob('group_2/*')
    try:
        for i in range(len(folders_2)):
            rotation_matrix = read_txt(folders_2[i] + '/fixed_rotation_matrix.txt')
            tranlational_vector = read_txt(folders_2[i] + '/fixed_translational_vector.txt')

            if rotation_matrix is not None and tranlational_vector is not None:
                draw_camera(rotation_matrix, tranlational_vector, "green")
            else:
                error_label.config(text=f"カメラ{i}のファイルの読み込みに問題がありました。")
                return

        canvas.draw()
        error_label.config(text="")
    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")
    """

###########以下GUIの設定とウェジットの配置##############
window = tk.Tk()
window.title("Camera Positions and Orientations")

# 更新ボタン
update_button = tk.Button(window, text="更新", command=update_cameras)
update_button.pack()

# エラーメッセージ表示
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

# 3Dグラフィックスを描画するための準備
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 15) # x軸の範囲を指定
ax.set_ylim(0, 10) # y軸の範囲を指定
ax.set_zlim(0, 5) # z軸の範囲を指定
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# 直線の始点と終点の座標を定義
x = [0, 11.885]  # x座標の始点と終点
y = [5.485, 5.485]  # y座標の始点と終点
z = [0, 0]  # z座標の始点と終点
ax.plot(x, y, z, color='blue')

x = [0, 11.885]  # x座標の始点と終点
y = [4.115, 4.115]  # y座標の始点と終点
z = [0, 0]  # z座標の始点と終点
ax.plot(x, y, z, color='blue')

x = [0, 11.885]  # x座標の始点と終点
y = [0, 0]  # y座標の始点と終点
z = [0, 0]  # z座標の始点と終点
ax.plot(x, y, z, color='blue')

x = [11.885, 11.885]  # x座標の始点と終点
y = [-1, 5.485]  # y座標の始点と終点
z = [0, 0]  # z座標の始点と終点
ax.plot(x, y, z, color='blue')

x = [6.40, 6.40]  # x座標の始点と終点
y = [-1, 5.485]  # y座標の始点と終点
z = [0, 0]  # z座標の始点と終点
ax.plot(x, y, z, color='blue')

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()
