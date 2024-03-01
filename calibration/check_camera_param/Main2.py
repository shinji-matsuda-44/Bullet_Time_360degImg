import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def open_file():
    filepath = filedialog.askopenfilename(
        initialdir="/",             # ダイアログが開かれる最初のディレクトリ
        title="Select a File",      # ダイアログのタイトル
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))  # ファイルの種類
    )
    print("Selected file:", filepath)
    return filepath

def load_matrix_from_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return np.array([[float(val) for val in line.strip().split()] for line in lines])
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def draw_camera(rotation_matrix, translation_vector):
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111, projection='3d')

    # カメラの位置
    camera_position = -np.dot(rotation_matrix.T, translation_vector)

    # カメラの姿勢
    x_axis = np.dot(rotation_matrix.T, np.array([1, 0, 0]))
    y_axis = np.dot(rotation_matrix.T, np.array([0, 1, 0]))
    z_axis = np.dot(rotation_matrix.T, np.array([0, 0, 1]))

    # カメラの位置を描画
    ax.scatter(camera_position[0], camera_position[1], camera_position[2], c='r', label='Camera Position')

    # カメラの姿勢を描画
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], x_axis[0], x_axis[1], x_axis[2], color='r', label='X-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], y_axis[0], y_axis[1], y_axis[2], color='g', label='Y-Axis')
    ax.quiver(camera_position[0], camera_position[1], camera_position[2], z_axis[0], z_axis[1], z_axis[2], color='b', label='Z-Axis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    return fig

def update_camera():
    try:
        #rotation_matrix = load_rotation_matrix()
        #translation_vector = load_translation_vector()

        rotation_matrix = np.array([[float(e.get()), float(f.get()), float(g.get())],
                                    [float(h.get()), float(i.get()), float(j.get())],
                                    [float(k.get()), float(l.get()), float(m.get())]])

        translation_vector = np.array([float(n.get()), float(o.get()), float(p.get())])

        fig = draw_camera(rotation_matrix, translation_vector)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")

    

window = tk.Tk()
window.title("Camera Position and Orientation")

# 回転行列のファイルを読み込むウィジット
open_button = tk.Button(window, text="Open Rotation Matrix File", command=open_file)
open_button.pack(pady=20)

# 回転行列のエントリウィジェット
tk.Label(window, text="Rotation Matrix:").pack()
e = tk.Entry(window)
f = tk.Entry(window)
g = tk.Entry(window)
h = tk.Entry(window)
i = tk.Entry(window)
j = tk.Entry(window)
k = tk.Entry(window)
l = tk.Entry(window)
m = tk.Entry(window)

e.pack()
f.pack()
g.pack()
h.pack()
i.pack()
j.pack()
k.pack()
l.pack()
m.pack()

# 並進ベクトルのエントリウィジェット
tk.Label(window, text="Translation Vector:").pack()
n = tk.Entry(window)
o = tk.Entry(window)
p = tk.Entry(window)

n.pack()
o.pack()
p.pack()

# 更新ボタン
update_button = tk.Button(window, text="更新", command=update_camera)
update_button.pack()

# エラーメッセージ表示
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

window.mainloop()
