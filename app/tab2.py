"""
動画のフレーム切り出し
"""
import os
import cv2
import glob
import shutil
import subprocess
import numpy as np
import tkinter as tk
import MakeMap
from tkinter import ttk
from PIL import Image, ImageTk

class Tab2(ttk.Frame):
    def __init__(self, master, database, name):
        super().__init__(master)
        self.database = database
        self.name = name
        self.bind("<Configure>", self.on_self_configure) #ウィンドウサイズ変更時のウィジットサイズ変更
        
        self.is_running_tab = False #タブ非選択時に不要な処理をスキップ (masterで管理)

        #指定したフレームを保存しておく隠しフォルダ
        self.hidden_folder_path = '.hidden_frame_image_folder'

        #フレーム処理に関連の変数など
        self.cap = None
        self.selected_file = None
        self.original_current_frame = None
        self.current_frame = None
        self.total_frames = 0
        self.is_playing = False
        self.is_moving_seek_scale = False
        self.make_map = MakeMap.MakeMap()

        #マウスイベントの変数など
        self.g_drag_flag = False
        self.g_prev_x, self.g_prev_y = None, None
        self.g_diff_x, self.g_diff_y = None, None
        self.is_update_g_diff = False

        #ウェジット関連の変数など
        self.defalt_tab_width = 0
        self.defalt_tab_height = 0
        self.left_side_width = 150 #リストの幅
        self.right_side_width = 800 #スクリーンを表示する領域やその他のコントロールウェジット領域の幅
        self.control_widget_height = 100 #コントロールウェジット領域の高さ
        self.frame_rate = 10 #動画のフレームレート（1枚のフレームを表示する時間[ms]）
        self.screen_width = self.right_side_width #表示する画像の幅
        self.screen_height = int(self.screen_width/2) #表示する画像の高さ
        self.is_initialize = False

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
        #シークバー
        self.seek_scale = ttk.Scale(self.control_widget, from_=0, to=self.total_frames-1 , orient="horizontal", length=self.right_side_width, command=self.set_frame)
        self.seek_scale.pack(side='bottom', pady=10)
        self.seek_scale.bind("<ButtonPress-1>", self.on_seek_scale_press)
        self.seek_scale.bind("<ButtonRelease-1>", self.on_seek_scale_release)
        #再生・停止・フレーム送り
        self.reset_button = ttk.Button(self.control_widget, text="|◀", command=self.reset_video)
        self.reset_button.pack(side='left')
        self.play_button = ttk.Button(self.control_widget, text="▶", command=self.play_pause_video)
        self.play_button.pack(side='left')
        self.previous_button = ttk.Button(self.control_widget, text="１フレーム戻る", command=self.previous_frame)
        self.previous_button.pack(side='left')
        self.next_button = ttk.Button(self.control_widget, text="１フレーム進む", command=self.next_frame)
        self.next_button.pack(side='left')
        #フレーム選択
        self.frame_menu_button = tk.Frame(self.control_widget, highlightbackground="#adadad", highlightthickness=1)
        self.frame_menu_button.pack(side='right')
        style = ttk.Style()
        style.configure("TMenubutton", background="#d4d4d4")  # あとで統一する
        self.register_frame = ttk.Menubutton(self.frame_menu_button, text="フレームを登録", style="TMenubutton")
        self.register_frame.pack()
        # メニューボタンにメニューを追加
        menu = tk.Menu(self.register_frame, tearoff=False)
        menu.add_command(label="選択したビデオのフレームのみ登録", command=self.register_one)
        menu.add_command(label="全ビデオの対応フレームを一括登録", command=self.register_all)
        self.register_frame["menu"] = menu
        self.register_frame.pack()

        #スクリーン
        self.frame_screen = tk.Frame(self, width=self.screen_width, height=self.screen_height, relief=tk.SOLID, bg='white', bd=1)
        self.frame_screen.propagate(False)
        self.frame_screen.pack(expand=True, padx=10, pady=10)
        self.screen = ttk.Label(self.frame_screen, text='No media', anchor='center')
        self.screen.bind("<ButtonPress-1>", self.on_button_press)
        self.screen.bind("<B1-Motion>", self.on_mouse_motion)
        self.screen.bind("<ButtonRelease-1>", self.on_button_release)
        self.screen.pack(expand=1, fill='both')

        #一定間隔で繰り返し実行
        self.update_screen() #is_running_tabを使用してタブ非選択時に内部の処理をスキップ
        self.update_listbox() 

    
    #タブの大きさが変更される、またはタブが選択されると呼び出される。
    def on_self_configure(self, event):
        #タブサイズの初期値を取得
        if self.is_initialize is False:
            self.defalt_tab_width = self.database.get_defalt_tab_size(key="width")
            self.defalt_tab_height = self.database.get_defalt_tab_size(key="height")
            self.is_initialize = True
        self.frame_list.config(height=self.winfo_height()) #リストフレームの高さの更新
        diff_width = self.winfo_width() - self.defalt_tab_width #始めのタブサイズと現在のタブサイズにおける width の差分
        diff_height = self.winfo_height() - self.defalt_tab_height #始めのタブサイズと現在のタブサイズにおける height の差分
        self.control_widget.config(width=self.right_side_width + diff_width) #ウェジットフレームの横幅の更新
        self.seek_scale.config(length=self.right_side_width + diff_width) #シークバーの横幅の更新
        if diff_width >= diff_height*2:
            #タブが始めより横長になった場合
            self.screen_height = int(self.right_side_width/2) + diff_height
            self.screen_width = self.screen_height*2
        else:
            #タブが始めより縦長になった場合
            self.screen_width = self.right_side_width + diff_width
            self.screen_height = int(self.screen_width/2)
        self.frame_screen.config(width=self.screen_width, height=self.screen_height)


    #タブ１でパスが設定されたときリスト更新
    def update_listbox(self):
        update = self.database.update_path_movie()
        if update:
            movie_folder = self.database.get_folder_path_entry(key=1)
            if movie_folder and os.path.exists(movie_folder):
                image_list = []
                for file in os.listdir(movie_folder):
                    if file.lower().endswith('.mp4'):
                        self.delete_img_folder()
                        self.files_listbox.delete(0, tk.END)
                        image_list.append(file)
                        self.selected_file = None
                    elif file.lower().endswith('.jpg'):
                        self.delete_img_folder()
                        self.files_listbox.delete(0, tk.END)
                        self.register_from_img_folder() #画像ファイルを隠しファイルに移動
                        self.selected_file = None
                    else:
                        self.files_listbox.delete(0, tk.END)
                        self.files_listbox.insert(tk.END, "ファイルが存在しません。")
                        self.selected_file = None
                if len(image_list) != 0:
                    self.files_listbox.delete(0, tk.END)
                    for image in image_list:
                        self.files_listbox.insert(tk.END, image)
            else:
                self.files_listbox.delete(0, tk.END)
                self.files_listbox.insert(tk.END, "無効なフォルダパスです。")
                self.selected_file = None
        self.after(500, self.update_listbox) #更新時間 0.5秒に1回

    def show_selected_file(self, event):
        selected_indices = self.files_listbox.curselection()
        if selected_indices:
            self.selected_file = self.files_listbox.get(selected_indices)
        if self.selected_file:
            if self.cap is not None:
                prev_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)) #新しい動画を読み込む前のフレーム数
            else:
                prev_frame_number = None
            video_path = os.path.join(self.database.get_folder_path_entry(key=1), self.selected_file)
            self.cap = cv2.VideoCapture(video_path)
            if prev_frame_number is not None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, prev_frame_number - 1) #setの処理は重い
            _, self.original_current_frame = self.cap.read()
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.seek_scale.configure(to=self.total_frames)
            #self.make_map = MakeMap.MakeMap()
            #マウスイベントの変数のリセット
            self.g_drag_flag = False
            self.g_prev_x, self.g_prev_y = None, None
            self.g_diff_x, self.g_diff_y = None, None
            self.is_update_g_diff = False

    #ボタンのイベント
    def play_pause_video(self):
        if self.selected_file:
            if self.is_playing:
                self.is_playing = False
                self.play_button.configure(text="▶")
            else:
                self.is_playing = True
                self.play_button.configure(text="■")

    def reset_video(self):
        if self.selected_file:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) #setの処理は重い
            ret, frame = self.cap.read()
            if ret:
                self.original_current_frame = frame
                self.seek_scale.set(0)

    def next_frame(self):
        if self.selected_file:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    self.original_current_frame = frame
                    current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    self.seek_scale.set(current_frame_number)

    def previous_frame(self):
        if self.selected_file:
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) - 2) #setの処理は重い
                ret, frame = self.cap.read()
                if ret:
                    self.original_current_frame = frame
                    current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    self.seek_scale.set(current_frame_number)

    def set_frame(self, value):
        if self.selected_file:
            if self.is_moving_seek_scale:
                frame_number = int(float(value))
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1) #setの処理は重い
                ret, frame = self.cap.read()
                if ret:
                    self.original_current_frame = frame

    def register_one(self):
        if self.selected_file:
            if not os.path.exists(self.hidden_folder_path):
                os.makedirs(self.hidden_folder_path)
                subprocess.run(['attrib', '+h', self.hidden_folder_path], check=True)
            index = self.files_listbox.curselection()[0]
            cv2.imwrite(os.path.join(self.hidden_folder_path, f"selected_frame_{index+1}.jpg"), self.original_current_frame)
            self.database.update_frame_image_list() #リスト更新のお知らせ

    #処理に時間がかかる
    def register_all(self):
        if self.selected_file:
            #隠しフォルダの作成
            if not os.path.exists(self.hidden_folder_path):
                os.makedirs(self.hidden_folder_path)
                subprocess.run(['attrib', '+h', self.hidden_folder_path], check=True)
            #フレーム画像を保存
            current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            for i in range(self.files_listbox.size()):
                image_name = self.files_listbox.get(i)
                video_source = os.path.join(self.database.get_folder_path_entry(key=1), image_name)
                cap = cv2.VideoCapture(video_source)
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_number - 1) #setの処理は重い
                _, frame = cap.read()
                cv2.imwrite(os.path.join(self.hidden_folder_path, f"selected_frame_{i+1}.jpg"), frame)
            self.database.update_frame_image_list() #リスト更新のお知らせ

    #タブ１で指定したパスから画像をコピー
    def register_from_img_folder(self):
        if not os.path.exists(self.hidden_folder_path):
            os.makedirs(self.hidden_folder_path)
            subprocess.run(['attrib', '+h', self.hidden_folder_path], check=True)
        path_img_folder = self.database.get_folder_path_entry(key=1)
        path_imgs = glob.glob(os.path.join(path_img_folder, '*.jpg'))
        for path in path_imgs:
                shutil.copy2(path, self.hidden_folder_path)
        self.database.update_frame_image_list() #リスト更新のお知らせ

    #frame_image_folderの削除
    def delete_img_folder(self):
        if os.path.exists(self.hidden_folder_path):
            shutil.rmtree(self.hidden_folder_path)
        self.database.update_frame_image_list() #リスト更新のお知らせ
        
    def update_screen(self):
        if self.is_running_tab:
            if self.selected_file:
                if self.is_playing:
                    ret, frame = self.cap.read()
                    if ret:
                        self.original_current_frame = frame
                        phi, theta = self.make_map.update_map(self.g_diff_x, self.g_diff_y, self.is_update_g_diff)
                        remap_frame = self.remap_image(frame, phi, theta)
                        resized_frame = cv2.resize(remap_frame, (self.screen_width, self.screen_height))
                        self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                        self.is_update_g_diff = False

                        current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                        self.seek_scale.set(current_frame_number)
                else:
                    if self.original_current_frame is not None:
                        frame = self.original_current_frame
                        phi, theta = self.make_map.update_map(self.g_diff_x, self.g_diff_y, self.is_update_g_diff)
                        remap_frame = self.remap_image(frame, phi, theta)
                        resized_frame = cv2.resize(remap_frame, (self.screen_width, self.screen_height))
                        self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                        self.is_update_g_diff = False

                if self.current_frame is not None:
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.current_frame))
                    self.screen.configure(image=self.photo)
                    self.screen.image = self.photo
            else:
                self.screen.configure(image='')
                self.screen.configure(text='No media')
        self.after(self.frame_rate, self.update_screen)

    #マウスイベント
    def on_button_press(self, event):
        self.g_drag_flag = True
        self.g_prev_x, self.g_prev_y = event.x, event.y

    def on_button_release(self, event):
        self.g_drag_flag = False

    def on_mouse_motion(self, event):
        if self.g_drag_flag:
            if self.g_prev_x is not None and self.g_prev_y is not None:
                self.is_update_g_diff = True
                self.g_diff_x, self.g_diff_y = self.g_prev_x - event.x, self.g_prev_y - event.y
        self.g_prev_x, self.g_prev_y = event.x, event.y

    def on_seek_scale_press(self,event):
        self.is_moving_seek_scale = True

    def on_seek_scale_release(self, event):
        self.is_moving_seek_scale = False

    #remapの処理
    def remap_image(self, image, phi, theta):
        input_height, input_width = image.shape[:2]
        # X座標とY座標の変換マップ
        phi = (phi * input_height / np.pi + input_height / 2)
        phi = phi.astype(np.float32)
        theta = (theta * input_width / (2 * np.pi) + input_width / 2)
        theta = theta.astype(np.float32)
        output_image = cv2.remap(image, theta, phi, cv2.INTER_NEAREST)
        return output_image