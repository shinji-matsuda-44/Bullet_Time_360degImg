"""
注視点の指定
"""
import os
import cv2
import glob
import math
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bullet_time import GenProjectedImg
from bullet_time import GetPoint

class Tab3(ttk.Frame):
    def __init__(self, master, database, name):
        super().__init__(master)
        self.database = database
        self.name = name
        self.bind("<Configure>", self.on_self_configure) #ウィンドウサイズ変更時のウィジットサイズ変更
        
        self.is_running_tab = False #タブ非選択時に不要な処理をスキップ (masterで管理)

        #データ/データリスト
        self.selected_file = None
        self.original_current_frame = None
        self.current_frame = None
        self.list_view_point = [] #注視点
        self.list_projected_img = [] #注視画像
        self.list_sight_rotation_matrix = [] #注視画像生成に用いた光軸の回転行列
        self.is_all_registered = False #全ての動画のフレームが登録されているか

        #デフォルトのタブサイズ
        self.defalt_tab_width = 0
        self.defalt_tab_height = 0
        self.is_initialize = False
        #ウェジットサイズ/スクリーンサイズ
        self.left_side_width = 150 #リストの幅
        self.right_side_width = 800 #スクリーンを表示する領域やその他のコントロールウェジット領域の幅
        self.control_widget_height = 100 #コントロールウェジット領域の高さ
        self.screen_width = self.right_side_width #表示する画像の幅
        self.screen_height = int(self.screen_width/2) #表示する画像の高さ
        #動画のフレームレート（1枚のフレームを表示する時間[ms]）
        self.frame_rate = 100 

        
        #ファイルリスト
        self.frame_list = tk.Frame(self, width=self.left_side_width, height=self.winfo_height())
        self.frame_list.pack(side='left')
        self.frame_list.propagate(False) #ウェジットの自動リサイズを禁止
        max_num_files = 30
        max_len_file_name = 20
        self.files_listbox = tk.Listbox(self.frame_list, width=max_num_files, height=max_len_file_name)
        self.files_listbox.bind("<<ListboxSelect>>", self.show_selected_file)
        self.files_listbox.pack(expand=1, fill='both')
        

        #コントロールウェジットなど
        self.control_widget = tk.Frame(self, width=self.right_side_width, height=self.control_widget_height)
        self.control_widget.pack(side='bottom', padx=10, pady=10)
        self.control_widget.propagate(False)
        #注視点の指定数を表示
        self.count_label = ttk.Label(self.control_widget, text="(指定数 0/?)", anchor='center')
        self.count_label.pack(side='bottom', anchor='e')
        #注視点が指定済か否かを表示
        self.check_label = ttk.Label(self.control_widget, text=" ", anchor='center')
        self.check_label.pack(anchor='e')
        #OpenCVのウィンドウを開いて注視点を指定
        annotation_button = ttk.Button(self.control_widget, text="注視点を指定", command=self.open_annotation_window)
        annotation_button.pack(side='right')
        #登録した注視点のリセット
        reset_button = ttk.Button(self.control_widget, text="リセット", command=self.reset_param)
        reset_button.pack(side='right')
        #ファイル数が足りているか否かを表示
        self.erorr_label = ttk.Label(self.control_widget, text=" ", anchor='center')
        self.erorr_label.pack(side='left')

        #スクリーン
        self.frame_screen = tk.Frame(self, width=self.screen_width, height=self.screen_height, relief=tk.SOLID, bg='white', bd=1)
        self.frame_screen.propagate(False)
        self.frame_screen.pack(expand=True, padx=10, pady=10)
        self.screen = ttk.Label(self.frame_screen, text='No media', anchor='center')
        self.screen.pack(expand=1, fill='both')

        #一定間隔で繰り返し実行
        self.update_screen() #is_running_tabを使用してタブ非選択時に内部の処理をスキップ
        self.update_listbox()
       

    #タブの大きさが変更される、またはタブが選択されると呼び出される。
    def on_self_configure(self, event):
        if self.is_initialize is False:
            self.defalt_tab_width = self.database.get_defalt_tab_size(key="width")
            self.defalt_tab_height = self.database.get_defalt_tab_size(key="height")
            self.is_initialize = True
        self.frame_list.config(height=self.winfo_height()) #リストフレームの高さの更新
        diff_width = self.winfo_width() - self.defalt_tab_width #始めのタブサイズと現在のタブサイズにおける width の差分
        diff_height = self.winfo_height() - self.defalt_tab_height #始めのタブサイズと現在のタブサイズにおける height の差分
        self.control_widget.config(width=self.right_side_width + diff_width) #ウェジットフレームの横幅の更新        
        if diff_width >= diff_height*2:
            #タブが始めより横長になった場合
            self.screen_height = int(self.right_side_width/2) + diff_height
            self.screen_width = self.screen_height*2
        else:
            #タブが始めより縦長になった場合
            self.screen_width = self.right_side_width + diff_width
            self.screen_height = int(self.screen_width/2)
        self.frame_screen.config(width=self.screen_width, height=self.screen_height)

    #タブ２でフレームが登録されたときリスト更新
    def update_listbox(self):
        update = self.database.update_path_frame_image()
        if update:
            hidden_folder_path = '.hidden_frame_image_folder'
            image_folder = hidden_folder_path
            if image_folder and os.path.exists(image_folder):
                image_list = []
                for file in os.listdir(image_folder):
                    if file.lower().endswith('.jpg'):
                        image_list.append(file)
                    else:
                        self.files_listbox.delete(0, tk.END)
                        self.files_listbox.insert(tk.END, "ファイルが存在しません。")
                        self.selected_file = None
                if len(image_list) != 0:
                    self.files_listbox.delete(0, tk.END)
                    for image in image_list:
                        self.files_listbox.insert(tk.END, image)
                    self.check_files_count()
            else:
                self.files_listbox.delete(0, tk.END)
                self.files_listbox.insert(tk.END, "無効なフォルダパスです。")
                self.selected_file = None
        self.after(500, self.update_listbox) #更新時間 0.5秒に1回

    #リストの数が映像のファイル数に満たないときのエラー処理
    def check_files_count(self):
        path = self.database.get_folder_path_entry(key=1)
        files = glob.glob(os.path.join(path, '*.mp4'))
        if len(files) == 0:
            files = glob.glob(os.path.join(path, '*.jpg'))
        total_input_files = len(files)
        now_files = self.files_listbox.size() #この値が0であることはない(insert命令があった後でしか呼び出されないため)
        if now_files == total_input_files:
                self.is_all_registered = True
                self.erorr_label.configure(text=' ')
        else:
            self.is_all_registered = False
            self.erorr_label.configure(text='全ての映像についてフレームを登録して下さい', foreground='red')

    def show_selected_file(self, event):
        selected_indices = self.files_listbox.curselection()
        if selected_indices:
            self.selected_file = self.files_listbox.get(selected_indices)
        if self.selected_file and len(selected_indices) != 0:
            hidden_folder_path = '.hidden_frame_image_folder'
            image_path = os.path.join(hidden_folder_path, self.selected_file)
            self.original_current_frame = cv2.imread(image_path)
            #注視点の指定済判定
            list = self.database.get_list_view_point()
            if list[selected_indices[0]] is None:
                self.check_label.configure(text = " ")
            else:
                self.check_label.configure(text = "注視点指定済")

    #表示した画像を別ウィンドウで操作
    def open_annotation_window(self):
        if self.is_all_registered:
            if self.selected_file:
                #注視画像の画角パラメータの読み込み
                THETA, PHI = self.read_param("bullet_time/viewingAngle.txt")
                #選択した画像のインデックス
                index = self.files_listbox.curselection()[0]
                
                #全方位画像から注視画像指定に用いる透視投影画像を生成
                hidden_folder_path = '.hidden_frame_image_folder'
                image_path = os.path.join(hidden_folder_path, self.selected_file)
                GI = GenProjectedImg.GenProjectedImg(image_path, THETA, PHI)
                projected_img, sight_rotation_matrix = GI.generateImg()
                projected_img = cv2.cvtColor(projected_img.astype(np.uint8), cv2.COLOR_BGR2BGRA) #numpy配列からcv2の画像へ変換
                self.database.set_list_projected_img(index, projected_img)
                self.database.set_list_sight_rotation_matrix(index, sight_rotation_matrix)

                #透視投影画像から注視点を指定
                GP = GetPoint.GetPoint(projected_img, comment="Set viewpoint")
                view_point = np.array(GP.get_point()[0])
                self.database.set_list_view_point(index, view_point)

                #注視点の指定数をカウント
                list = self.database.get_list_view_point()
                count = 0
                for i in range(len(list)):
                    if list[i] is not None:
                        count += 1
                self.count_label.configure(text = f"(指定数 {count}/{len(list)})")
                self.check_label.configure(text = "注視点指定済")

    def read_param(self, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                label, value = line.strip().split(': ')
                if label == '横方向の画角':
                    THETA = math.radians(float(value))
                if label == '縦方向の画角':
                    PHI = math.radians(float(value))
        return THETA, PHI
    
    def reset_param(self):
        list = self.database.get_list_view_point()
        if self.is_all_registered:
            if self.selected_file:
                list_size = self.files_listbox.size()
                self.database.reset_param(list_size)
                self.count_label.configure(text = f"(指定数 0/{len(list)})")
                self.check_label.configure(text = " ")

    #スクリーンの画像を連続的に更新する。
    def update_screen(self):
        if self.is_running_tab:
            if self.selected_file:
                if self.original_current_frame is not None:
                    frame = self.original_current_frame
                    resized_frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                    self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

                if self.current_frame is not None:
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.current_frame))
                    self.screen.configure(image=self.photo)
                    self.screen.image = self.photo
            else:
                self.screen.configure(image='')
                self.screen.configure(text='No media')

        self.after(self.frame_rate, self.update_screen) #更新頻度 0.01秒に1回
