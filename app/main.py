import os
import shutil
import tkinter as tk
from tkinter import ttk
from tab1 import Tab1
from tab2 import Tab2
from tab3 import Tab3
from tab4 import Tab4
from database import Database

class Main:
    def __init__(self):
        pass

    #隠しフォルダの後始末
    def on_closing(self):
        if os.path.exists(".hidden_folder1"):
            shutil.rmtree(".hidden_folder1")
        if os.path.exists(".hidden_folder2"):
            shutil.rmtree(".hidden_folder2")
        if os.path.exists(".hidden_frame_image_folder"):
            shutil.rmtree(".hidden_frame_image_folder")
        self.root.destroy()

    #タブの動作管理
    def on_tab_changed(self, event):
        current_tab = event.widget.tab(event.widget.select(), "text")
        self.tab2.is_running_tab = False
        self.tab3.is_running_tab = False
        self.tab4.is_running_tab = False
        if current_tab == self.name_tab2:
            self.tab2.is_running_tab = True
        elif current_tab == self.name_tab3:
            self.tab3.is_running_tab = True
        elif current_tab == self.name_tab4:
            self.tab4.is_running_tab = True

    def start(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("バレットタイム作成GUI")
        database = Database()
        tab_control = ttk.Notebook(self.root)

        self.name_tab1 = 'Step 1    '
        self.tab1 = Tab1(tab_control, database, self.name_tab1)
        tab_control.add(self.tab1, text=self.name_tab1)

        self.name_tab2 = 'Step 2    '
        self.tab2 = Tab2(tab_control, database, self.name_tab2)
        tab_control.add(self.tab2, text=self.name_tab2)

        self.name_tab3 = 'Step 3    '
        self.tab3 = Tab3(tab_control, database, self.name_tab3)
        tab_control.add(self.tab3, text=self.name_tab3)

        self.name_tab4 = 'Step 4    '
        self.tab4 = Tab4(tab_control, database, self.name_tab4)
        tab_control.add(self.tab4, text=self.name_tab4)

        tab_control.pack(expand=1, fill="both")
        tab_control.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        self.root.mainloop()

if __name__ == "__main__":
    bullet_time_gui = Main()
    bullet_time_gui.start()