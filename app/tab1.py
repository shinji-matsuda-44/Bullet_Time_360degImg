"""
フォルダパス指定
"""
#パスが存在するか、ファイルが存在するかをチェックするようにする。
import os
import glob
import tkinter as tk
from tkinter import ttk, filedialog

class Tab1(ttk.Frame):
    def __init__(self, master, database, name):
        super().__init__(master)
        self.database = database
        self.name = name
        self.bind("<Configure>", self.on_self_configure)

        self.is_initialize = False

        #画像群を入力するエントリと選択ボタン
        frame1 = ttk.Frame(self)
        frame1.pack(pady=10)
        ttk.Label(frame1, text='入力する映像群または画像群のフォルダを選択してください').grid(row=0, column=0, padx=10, sticky='w')
        self.folder_path_entry1 = ttk.Entry(frame1, width=50)
        self.folder_path_entry1.grid(row=1, column=0, padx=10)
        select_button1 = ttk.Button(frame1, text='選択', command=self.select_folder1)
        select_button1.grid(row=1, column=1)

        #外部パラメータを入力するエントリと選択ボタン
        frame2 = ttk.Frame(self)
        frame2.pack(pady=10)
        ttk.Label(frame2, text='入力する外部パラメータのフォルダを選択してください').grid(row=0, column=0, padx=10, sticky='w')
        self.folder_path_entry2 = ttk.Entry(frame2, width=50)
        self.folder_path_entry2.grid(row=1, column=0, padx=10)
        select_button2 = ttk.Button(frame2, text='選択', command=self.select_folder2)
        select_button2.grid(row=1, column=1)

        #内部パラメータを入力するエントリと選択ボタン
        frame3 = ttk.Frame(self)
        frame3.pack(pady=10)
        ttk.Label(frame3, text='入力する内部パラメータのフォルダを選択してください').grid(row=0, column=0, padx=10, sticky='w')
        self.folder_path_entry3 = ttk.Entry(frame3, width=50)
        self.folder_path_entry3.grid(row=1, column=0, padx=10)
        select_button3 = ttk.Button(frame3, text='選択', command=self.select_folder3)
        select_button3.grid(row=1, column=1)

        #出力するフォルダを選択するエントリと選択ボタン
        frame4 = ttk.Frame(self)
        frame4.pack(pady=10)
        ttk.Label(frame4, text='出力するフォルダを選択してください').grid(row=0, column=0, padx=10, sticky='w')
        self.folder_path_entry4 = ttk.Entry(frame4, width=50)
        self.folder_path_entry4.grid(row=1, column=0, padx=10)
        select_button4 = ttk.Button(frame4, text='選択', command=self.select_folder4)
        select_button4.grid(row=1, column=1)

    def select_folder1(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry1.delete(0, tk.END)
        self.folder_path_entry1.insert(0, folder_path)
        self.database.set_entry(key=1, value=self.folder_path_entry1)
        self.database.update_movie_list() #フォルダが選択されたとき、タブ2のリストを更新
        self.reset_param() #フォルダが選択されたとき、計算に使用するパラメータリストをリセット

    def select_folder2(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry2.delete(0, tk.END)
        self.folder_path_entry2.insert(0, folder_path)
        self.database.set_entry(key=2, value=self.folder_path_entry2)

    def select_folder3(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry3.delete(0, tk.END)
        self.folder_path_entry3.insert(0, folder_path)
        self.database.set_entry(key=3, value=self.folder_path_entry3)

    def select_folder4(self):
        folder_path = filedialog.askdirectory()
        self.folder_path_entry4.delete(0, tk.END)
        self.folder_path_entry4.insert(0, folder_path)
        self.database.set_entry(key=4, value=self.folder_path_entry4)

    def reset_param(self):
        path = self.folder_path_entry1.get()
        files = glob.glob(os.path.join(path, '*.mp4'))
        if len(files) == 0:
            files = glob.glob(os.path.join(path, '*.jpg'))
        total_input_files = len(files)
        self.database.reset_param(total_input_files)

    def on_self_configure(self, event):
        #タブサイズの初期値を取得
        if self.is_initialize is False:
            if self.winfo_width() != 1:
                defalt_tab_width = self.winfo_width()
                defalt_tab_height = self.winfo_height()
                self.database.set_defalt_tab_size(key="width", value = defalt_tab_width)
                self.database.set_defalt_tab_size(key="height", value = defalt_tab_height)
                self.is_initialize = True
