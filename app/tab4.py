"""
バレットタイム映像の出力
"""
import os
import cv2
import glob
import shutil
import datetime
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from bullet_time import GenViewPoint
from bullet_time import GenBulletTime1
from bullet_time import GenBulletTime2
from bullet_time import PaintCircle


class Tab4(ttk.Frame):
    def __init__(self, master, database, name):
        super().__init__(master)
        self.database = database
        self.name = name
        self.bind("<Configure>", self.on_self_configure) #ウィンドウサイズ変更時のウィジットサイズ変更

        self.is_running_tab = False #タブ非選択時に不要な処理をスキップ (masterで管理)

        #データ/データパス/データリスト
        self.selected_file = None #リストから選択したファイル
        self.original_current_frame = None #正距円筒画像
        self.current_frame = None #上に処理を行った表示画像
        self.hidden_folder_path_no_point = None #注視点表示なしのデータ群
        self.hidden_folder_path_with_point = None #注視点表示ありのデータ群
        self.path_no_point_imgs = [] #注視画像
        self.path_with_point_imgs = [] #注視画像
        self.path_no_point_bullet_time = [] #バレットタイム映像
        self.path_with_point_bullet_time = [] #バレットタイム映像
        self.view_point_3D = np.array([]) #三次元復元した注視点
        
        #デフォルトのタブサイズ
        self.defalt_tab_width = 0
        self.defalt_tab_height = 0
        self.is_initialize = False
        #ウェジットサイズ/スクリーンサイズ
        self.left_side_width = 150 #リストの幅
        self.right_side_width = 800 #スクリーンを表示する領域やその他のコントロールウェジット領域の幅
        self.control_widget_height = 100
        self.screen_width = self.right_side_width
        self.screen_height = int(self.screen_width/2)
        #動画のフレームレート（1枚のフレームを表示する時間[ms]）
        self.frame_rate = 300 
        #スクリーン処理の分岐用フラグ
        self.has_run_before = False
        self.is_generating_bullet_time = False
        self.is_playing = False
        self.count_frame = 0
        self.total_frame = 0
        #スケーリング処理のフラグ
        self.scale_image = False

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
        #注視点描画有無の切り替え
        self.selected = tk.StringVar()
        self.options = ["注視点描画なし", "注視点描画あり"]
        for option in self.options:
            radio_button = ttk.Radiobutton(self.control_widget, text=option, variable=self.selected, value=option)
            radio_button.pack(anchor='w')
        #切替ボタン
        switch_option_button = ttk.Button(self.control_widget, text="切替/バレットタイム表示", command=self.switch_option)
        switch_option_button.pack(anchor='w')
        #更新と保存のボタン
        save_button = ttk.Button(self.control_widget, text="保存", command=self.save_img)
        save_button.pack(side='right', anchor='s')
        update_button = ttk.Button(self.control_widget, text="更新(スケーリングOFF)", command=self.generate_img)
        update_button.pack(side='right', anchor='s')
        update_button = ttk.Button(self.control_widget, text="更新(スケーリングON)", command=self.generate_img_2)
        update_button.pack(side='right', anchor='s')

        #スクリーン
        self.frame_screen = tk.Frame(self, width=self.screen_width, height=self.screen_height, relief=tk.SOLID, bg='white', bd=1)
        self.frame_screen.propagate(False)
        self.frame_screen.pack(expand=True, padx=10, pady=10)
        self.screen = ttk.Label(self.frame_screen, text='No media', anchor='center')
        self.screen.pack(expand=1, fill='both')

        #一定間隔で繰り返し実行
        self.update_screen() #is_running_tabを使用してタブ非選択時に内部の処理をスキップ
    

    #タブの大きさが変更される、またはタブが選択されると呼び出し
    def on_self_configure(self, event):
        if self.is_initialize is False:
            self.defalt_tab_width = self.database.get_defalt_tab_size(key="width")
            self.defalt_tab_height = self.database.get_defalt_tab_size(key="height")
            self.is_initialize = True
        self.frame_list.config(height=self.winfo_height()) #リストフレームの高さの変更
        diff_width = self.winfo_width() - self.defalt_tab_width #始めのタブサイズと現在のタブサイズにおける width の差分
        diff_height = self.winfo_height() - self.defalt_tab_height #始めのタブサイズと現在のタブサイズにおける height の差分
        self.control_widget.config(width=self.right_side_width + diff_width) #ウェジットフレームの横幅の変更
        if diff_width >= diff_height*2:
            #タブが始めより横長になった場合
            self.screen_height = int(self.right_side_width/2) + diff_height
            self.screen_width = self.screen_height*2
        else:
            #タブが始めより縦長になった場合
            self.screen_width = self.right_side_width + diff_width
            self.screen_height = int(self.screen_width/2)
        self.frame_screen.config(width=self.screen_width, height=self.screen_height) #スクリーンサイズの変更

    def update_listbox(self):
        if(self.selected.get() == self.options[0]):
            image_folder = self.hidden_folder_path_no_point
        if(self.selected.get() == self.options[1]):
            image_folder = self.hidden_folder_path_with_point
        if image_folder and os.path.exists(image_folder):
            image_list = []
            for file in os.listdir(image_folder):
                if file.lower().endswith('.jpg'):
                    image_list.append(file)
                else:
                    self.files_listbox.delete(0, tk.END)
                    self.files_listbox.insert(tk.END, "ファイルが存在しません。")
            if len(image_list) != 0:
                self.files_listbox.delete(0, tk.END)
                for image in image_list:
                    self.files_listbox.insert(tk.END, image)
                self.total_frame = self.files_listbox.size()
        else:
            self.files_listbox.delete(0, tk.END)
            self.files_listbox.insert(tk.END, "無効なフォルダパスです。")

    def show_selected_file(self, event):
        self.is_playing = False
        selected_indices = self.files_listbox.curselection()
        if selected_indices:
            self.selected_file = self.files_listbox.get(selected_indices)
        if self.selected_file:
            if(self.selected.get() == self.options[0]):
                image_folder = self.hidden_folder_path_no_point
            if(self.selected.get() == self.options[1]):
                image_folder = self.hidden_folder_path_with_point
            image_path = os.path.join(image_folder, self.selected_file)
            self.original_current_frame = cv2.imread(image_path)

    def switch_option(self):
        if self.is_generating_bullet_time:
            self.is_playing = True
            self.update_listbox()

    def generate_img(self): #エラー処理や分岐命令が無いのでを追加する
        self.scale_image = False
        long_task_thread = LongTaskThread(parent=self)
        long_task_thread.start() #スレッドで実行しないと、この処理中にGUIの応答がなくなるエラーが生じる

    def generate_img_2(self): #エラー処理や分岐命令が無いのでを追加する
        self.scale_image = True
        long_task_thread = LongTaskThread(parent=self)
        long_task_thread.start() #スレッドで実行しないと、この処理中にGUIの応答がなくなるエラーが生じる
        
    def save_img(self):
        if self.is_generating_bullet_time:
            #フォルダの用意
            now = datetime.datetime.now()
            output_folder = self.database.get_folder_path_entry(key=4)
            main_folder = os.path.join(output_folder, now.strftime('%m%d_%H%M') + '_save_data')
            sub_folder1 = os.path.join(main_folder, 'path_no_point_bullet_time')
            sub_folder2 = os.path.join(main_folder, 'path_with_point_bullet_time')
            sub_folder3 = os.path.join(main_folder, 'select_point_img')
            if not os.path.exists(main_folder):
                os.makedirs(main_folder)
                os.makedirs(sub_folder1)
                os.makedirs(sub_folder2)
                os.makedirs(sub_folder3)
            #path_no_point_bullet_timeの中身
            for path in self.path_no_point_imgs:
                shutil.copy2(path, sub_folder1)
            shutil.copy2(self.path_no_point_bullet_time[0], os.path.join(sub_folder1, "no_point_img.gif"))
            #path_with_point_bullet_timeの中身
            for path in self.path_with_point_imgs:
                shutil.copy2(path, sub_folder2)
            shutil.copy2(self.path_with_point_bullet_time[0], os.path.join(sub_folder2, "with_point_img.gif"))
            #select_point_imgの中身 
            np.savetxt(os.path.join(sub_folder3,'view_point_3D.txt'), self.view_point_3D)
            PC = PaintCircle.PaintCircle()
            list_view_point = self.database.get_list_view_point()
            list_projected_img = self.database.get_list_projected_img()
            for i, img_file in enumerate(list_projected_img):
                if list_projected_img[i] is None:
                    continue
                np.savetxt(os.path.join(sub_folder3, f"view_point_{i+1}.txt"), list_view_point[i])
                img = PC.paint_circle(tuple(list_view_point[i]), img_file)
                cv2.imwrite(os.path.join(sub_folder3, f"check_point_img_{i+1}.jpg"), img)

    def update_screen(self):
        if self.is_running_tab:
            if self.is_generating_bullet_time:
                if self.is_playing:
                    if self.selected.get() == self.options[0]:
                        #バレットタイムの描画
                        frame = cv2.imread(self.path_no_point_imgs[self.count_frame])
                        resized_frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                        self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                        if self.count_frame == self.total_frame-1:
                            self.count_frame = 0
                        else:
                            self.count_frame += 1
                    elif self.selected.get() == self.options[1]:
                        frame = cv2.imread(self.path_with_point_imgs[self.count_frame])
                        resized_frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                        self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                        if self.count_frame == self.total_frame-1:
                            self.count_frame = 0
                        else:
                            self.count_frame += 1
                else:
                    frame = self.original_current_frame
                    resized_frame = cv2.resize(frame, (self.screen_width, self.screen_height))
                    self.current_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                
                if self.current_frame is not None:
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.current_frame))
                    self.screen.configure(image=self.photo)
                    self.screen.image = self.photo
            else:
                if self.has_run_before:
                    #生成中のテキストの表示
                    self.screen.configure(image='')
                    self.screen.configure(text="generating Bullet Time ...")
        self.after(self.frame_rate, self.update_screen) #一定間隔で繰り返し実行


class LongTaskThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.is_running = True

    def run(self):
        self.parent.is_generating_bullet_time = False #生成中フラグ
        self.parent.has_run_before = True

        hidden_folder_path = '.hidden_frame_image_folder'
        img_folder = hidden_folder_path
        external_folder = self.parent.database.get_folder_path_entry(key=2)
        internal_folder = self.parent.database.get_folder_path_entry(key=3)

        list_view_point = self.parent.database.get_list_view_point()
        list_sight_rotation_matrix = self.parent.database.get_list_sight_rotation_matrix()

        #注視点の計算
        GVP = GenViewPoint.GenViewPoint(
            img_folder,
            external_folder,
            internal_folder,
            list_view_point,
            list_sight_rotation_matrix
        )
        self.parent.view_point_3D = GVP.generate_view_point()

        #バレットタイム画像の生成
        if self.parent.scale_image is False:
            print("スケーリングなしでバレットタイムを作成")
            GBT = GenBulletTime1.GenBulletTime1(
                img_folder,
                external_folder,
                self.parent.view_point_3D
            )
            self.parent.hidden_folder_path_no_point, self.parent.hidden_folder_path_with_point \
            = GBT.generate_bullet_time()
        else:
            print("スケーリングありでバレットタイムを作成")
            GBT = GenBulletTime2.GenBulletTime2(
                img_folder,
                external_folder,
                self.parent.view_point_3D
            )
            self.parent.hidden_folder_path_no_point, self.parent.hidden_folder_path_with_point \
            = GBT.generate_bullet_time()

        self.parent.path_no_point_imgs = glob.glob(os.path.join(self.parent.hidden_folder_path_no_point, '*.jpg'))
        self.parent.path_with_point_imgs = glob.glob(os.path.join(self.parent.hidden_folder_path_with_point, '*.jpg'))
        self.parent.path_no_point_bullet_time = glob.glob(os.path.join(self.parent.hidden_folder_path_no_point, '*.gif'))
        self.parent.path_with_point_bullet_time = glob.glob(os.path.join(self.parent.hidden_folder_path_with_point, '*.gif'))

        self.parent.selected.set(self.parent.options[0]) #更新した後のデフォルトは注視点描画なし
        self.parent.update_listbox() #リストの更新 

        self.parent.is_playing = True #更新した後のデフォルトはバレットタイム映像の描画
        self.parent.is_generating_bullet_time = True #生成完了フラグ