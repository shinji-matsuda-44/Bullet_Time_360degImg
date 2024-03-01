import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def draw_camera(rotation_matrix, translation_vector, color):
    # 以前の描画をクリア
    ax.cla()

    # カメラの位置
    camera_position = -np.dot(rotation_matrix.T, translation_vector)

    # カメラの姿勢
    x_axis = np.dot(rotation_matrix.T, np.array([1, 0, 0]))
    y_axis = np.dot(rotation_matrix.T, np.array([0, 1, 0]))
    z_axis = np.dot(rotation_matrix.T, np.array([0, 0, 1]))

    # カメラの位置を描画
    ax.scatter(camera_position[0], camera_position[1], camera_position[2], c=color, label='Camera Position')

    # カメラの姿勢を描画
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], x_axis[0], x_axis[1], x_axis[2], color='r', label='X-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], y_axis[0], y_axis[1], y_axis[2], color='g', label='Y-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], z_axis[0], z_axis[1], z_axis[2], color='b', label='Z-Axis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

def update_cameras():
    try:
        for i, camera in enumerate(cameras):
            rotation_matrix = load_matrix_from_file(f"rotation_matrix_{i}.txt")
            translation_vector = load_matrix_from_file(f"translation_vector_{i}.txt")

            if rotation_matrix is not None and translation_vector is not None:
                draw_camera(rotation_matrix, translation_vector, colors[i])
            else:
                error_label.config(text=f"カメラ{i}のファイルの読み込みに問題がありました。")
                return

        canvas.draw()
        error_label.config(text="")

    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")

def load_matrix_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return np.array([[float(val) for val in line.strip().split()] for line in lines])
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

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
