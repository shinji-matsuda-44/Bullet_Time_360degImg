import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def to_homogeneous(coords):
    return np.hstack([coords, np.ones((coords.shape[0], 1))])

def draw_camera_viewport(R, t, size=None):
    K = np.array([[1000, 0, 320],
              [0, 1000, 240],
              [0, 0, 1]])
    W, H = K[0, 2]*2, K[1, 2]*2
    corners = np.array([[0, 0], [W, 0], [W, H], [0, H], [0, 0]])
    
    if size is not None:
        image_extent = max(size * W / 1024.0, size * H / 1024.0)
        world_extent = max(W, H) / (K[0, 0] + K[1, 1]) / 0.5
        scale = 0.5 * image_extent / world_extent
    else:
        scale = 1.0
    
    corners = to_homogeneous(corners) @ np.linalg.inv(K).T
    corners = (corners / 2 * scale) @ R.T + t
    
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # 視錐台の頂点をつなぐ線を描画
    i = [0, 1, 2, 3, 0]
    j = [1, 2, 3, 0, 4]
    k = [2, 3, 0, 1, 4]

    ax.add_collection3d(Poly3DCollection([corners[[i, j, k]]], color='b', linewidths=1, edgecolors='r', alpha=.25))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    window.mainloop()


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
    #try:
        for i, camera in enumerate(cameras):
            rotation_matrix = load_matrix_from_file(f"rotation_matrix_{i}.txt")
            translation_vector = load_matrix_from_file(f"translation_vector_{i}.txt")

            if rotation_matrix is not None and translation_vector is not None:
                draw_camera(rotation_matrix, translation_vector, colors[i])
                draw_camera_viewport(rotation_matrix, translation_vector, size=1.0)  # カメラの視錐台を描画
            else:
                error_label.config(text=f"カメラ{i}のファイルの読み込みに問題がありました。")
                return

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()

        canvas.draw()
        error_label.config(text="")

    #except ValueError:
    #    error_label.config(text="入力値が無効です。数値を入力してください。")

def load_matrix_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return np.array([[float(val) for val in line.strip().split()] for line in lines])
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

###########以下GUIの設定とウェジットの配置##############
window = tk.Tk()
window.title("Camera Positions and Orientations")

# カメラの数と各カメラの色
num_cameras = 3
colors = ['red', 'green', 'blue']

cameras = []
for i in range(num_cameras):
    tk.Label(window, text=f"Camera {i}").pack()

    rotation_matrix_entry = tk.Entry(window)
    translation_vector_entry = tk.Entry(window)

    rotation_matrix_entry.pack()
    translation_vector_entry.pack()

    cameras.append((rotation_matrix_entry, translation_vector_entry))

# 更新ボタン
update_button = tk.Button(window, text="更新", command=update_cameras)
update_button.pack()

# エラーメッセージ表示
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

# 3Dグラフィックスを描画するための準備
fig = Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111, projection='3d')

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

window.mainloop()
