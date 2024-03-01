import os
import sys
import glob
import math
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_true_camera(color):
    #世界座標系より、撮影時に中心とした点(※)を原点としたときの極座標の値
    r = np.zeros([9])
    r[0] = 6.66 #メートル
    r[1] = 4.62
    r[2] = 3.71
    r[3] = 3.56
    r[4] = 3.89
    r[5] = 4.84
    r[6] = 6.44
    r[7] = 6.08
    r[8] = 6.60

    r = np.full(9, 3.56) #B配置の場合

    a,b,c = 6.40, 11.885, 5.485
    alpha = math.radians(180/8)
    beta = math.atan2(-c, b)
    theta = np.zeros([9])
    theta[0] = alpha*8 + beta
    theta[1] = alpha*7 + beta
    theta[2] = alpha*6 + beta
    theta[3] = alpha*5 + beta
    theta[4] = alpha*4 + beta
    theta[5] = alpha*3 + beta
    theta[6] = alpha*2 + beta
    theta[7] = alpha*1 + beta
    theta[8] = alpha*0 + beta

    height = 1.35 #メートル

    #中心の点の座標
    center = np.array([a, c-a*c/b, height])
    
    #カメラ位置の描画
    for i in range(9):
        #カメラの位置
        camera_position = np.array([r[i]*math.cos(theta[i])+center[0], r[i]*math.sin(theta[i])+center[1], center[2]])
        np.savetxt(f"true_camera_pos/patarnB/camera_{i}.txt", camera_position)

        # カメラの姿勢
        z_axis = center - camera_position  # カメラ位置から指定した点へのベクトル
        z_axis /= np.linalg.norm(z_axis)

        # x_axisの計算
        x_axis = np.cross(z_axis, np.array([0, 0, 1]))
        x_axis /= np.linalg.norm(x_axis)

        # y_axisの計算
        y_axis = np.cross(z_axis, x_axis)
        y_axis /= np.linalg.norm(y_axis)

        # カメラの位置を描画
        ax.scatter(camera_position[0], camera_position[1], camera_position[2], c=color, label=f'Camera {color}')

        # カメラの姿勢を描画
        ax.quiver(camera_position[0], camera_position[1], camera_position[2], x_axis[0], x_axis[1], x_axis[2], color=color, label=f'Camera {color} X-Axis')
        ax.quiver(camera_position[0], camera_position[1], camera_position[2], y_axis[0], y_axis[1], y_axis[2], color=color, label=f'Camera {color} Y-Axis')
        ax.quiver(camera_position[0], camera_position[1], camera_position[2], z_axis[0], z_axis[1], z_axis[2], color=color, label=f'Camera {color} Z-Axis')



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
    fname = sys.argv[1]
    folders_1 = glob.glob(f'{fname}/*')
    try:
        for i in range(len(folders_1)):

            #(fixed_)rotation_matrix.txtと(fixed_)translation_vector.txtの読み込み
            if os.path.exists(os.path.join(folders_1[i], 'rotation_matrix.txt')):
                path_rotation_file = os.path.join(folders_1[i], 'rotation_matrix.txt')
            else:
                path_rotation_file = os.path.join(folders_1[i], 'fixed_rotation_matrix.txt')

            if os.path.exists(os.path.join(folders_1[i], 'translation_vector.txt')):
                path_translation_file = os.path.join(folders_1[i], 'translation_vector.txt')
            else:
                path_translation_file = os.path.join(folders_1[i], 'fixed_translation_vector.txt')

            rotation_matrix = np.loadtxt(path_rotation_file, delimiter=',')
            tranlational_vector = np.loadtxt(path_translation_file, delimiter=',')

            if rotation_matrix is not None and tranlational_vector is not None:
                draw_camera(rotation_matrix, tranlational_vector, "red")
            else:
                error_label.config(text=f"カメラ{i}のファイルの読み込みに問題がありました。")
                return

        canvas.draw()
        error_label.config(text="")
    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")

    #draw_true_camera("blue")
    #canvas.draw()

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
# アスペクト比を設定して、x軸とy軸のスケールを合わせる
ax.set_aspect('equal', adjustable='box')

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

# 点を打つ座標を定義
point_x = 6.522378083123165027
point_y = 2.372517795036355626
point_z = 1.030753566435547386

# 点をプロット
ax.plot([point_x], [point_y], [point_z], marker='o', markersize=8, color='red')

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()
