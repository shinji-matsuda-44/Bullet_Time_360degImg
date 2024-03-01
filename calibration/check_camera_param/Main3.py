import tkinter as tk
from tkinter import filedialog
import numpy as np

def open_file():
    filepath = filedialog.askopenfilename(
        initialdir="/",             # ダイアログが開かれる最初のディレクトリ
        title="Select a File",      # ダイアログのタイトル
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))  # ファイルの種類
    )
    print("Selected file:", filepath)

def load_rotation_matrix():
    filename = filedialog.askopenfilename(title="Select Rotation Matrix File")
    with open(filename, 'r') as file:
        lines = file.readlines()
        return np.array([[float(val) for val in line.strip().split()] for line in lines])

def load_translation_vector():
    filename = filedialog.askopenfilename(title="Select Translation Vector File")
    with open(filename, 'r') as file:
        lines = file.readlines()
        return np.array([float(val) for val in lines])

def draw_camera(rotation_matrix, translation_vector):
    camera_position = -np.dot(rotation_matrix.T, translation_vector)
    
    # カメラの位置を描画
    canvas.create_oval(camera_position[0]-2, camera_position[1]-2, camera_position[0]+2, camera_position[1]+2, fill='red', outline='red')
    
    # カメラの姿勢を描画
    x_axis = np.dot(rotation_matrix.T, np.array([1, 0, 0]))
    y_axis = np.dot(rotation_matrix.T, np.array([0, 1, 0]))
    z_axis = np.dot(rotation_matrix.T, np.array([0, 0, 1]))
    
    canvas.create_line(camera_position[0], camera_position[1], camera_position[0]+x_axis[0]*10, camera_position[1]+x_axis[1]*10, fill='red', arrow=tk.LAST)
    canvas.create_line(camera_position[0], camera_position[1], camera_position[0]+y_axis[0]*10, camera_position[1]+y_axis[1]*10, fill='green', arrow=tk.LAST)
    canvas.create_line(camera_position[0], camera_position[1], camera_position[0]+z_axis[0]*10, camera_position[1]+z_axis[1]*10, fill='blue', arrow=tk.LAST)

def update_camera():
    #print(filepath)
    try:
        rotation_matrix = load_rotation_matrix()
        translation_vector = load_translation_vector()
        
        rotation_matrix = np.array([[float(e.get()), float(f.get()), float(g.get())],
                                    [float(h.get()), float(i.get()), float(j.get())],
                                    [float(k.get()), float(l.get()), float(m.get())]])

        translation_vector = np.array([float(n.get()), float(o.get()), float(p.get())])

        canvas.delete("all")  # 以前の描画をクリア

        draw_camera(rotation_matrix, translation_vector)
        
        error_label.config(text="")

    except ValueError:
        error_label.config(text="入力値が無効です。数値を入力してください。")

window = tk.Tk()
window.title("Camera Position and Orientation")

open_button = tk.Button(window, text="Open File", command=open_file)
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

# グラフィックスを描画するキャンバス
canvas = tk.Canvas(window, width=300, height=300)
canvas.pack()

window.mainloop()
