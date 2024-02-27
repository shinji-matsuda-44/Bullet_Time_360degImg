"""
タブ間のデータ受け渡し用
・エントリに入力されたパス
・映像ファイルのリストボックス
・画像ファイルのリストボックス
"""

class Database():
    def __init__(self):
        self.defalt_tab_size = {} #タブのデフォルトサイズの辞書

        self.running_tab = None

        self.folder_path_entry = {} #パスエントリの辞書

        self.list_view_point = []
        self.list_sight_rotation_matrix = []
        self.list_projected_img = []

        self.is_update_path_movie = False
        self.is_update_path_frame_image = False
    
    #ゲッター
    def get_defalt_tab_size(self, key):
        return self.defalt_tab_size.get(key)

    def get_folder_path_entry(self, key):
        return self.folder_path_entry.get(key).get()
    
    def get_list_view_point(self):
        return self.list_view_point
    
    def get_list_sight_rotation_matrix(self):
        return self.list_sight_rotation_matrix
    
    def get_list_projected_img(self):
        return self.list_projected_img
    
    #セッター
    def set_defalt_tab_size(self, key, value):
        self.defalt_tab_size[key] = value

    def set_entry(self, key, value):
        self.folder_path_entry[key] = value

    def set_list_view_point(self, index, content):
        self.list_view_point[index] = content

    def set_list_sight_rotation_matrix(self, index, content):
        self.list_sight_rotation_matrix[index] = content

    def set_list_projected_img(self, index, content):
        self.list_projected_img[index] = content
    
    #リストの一括リセット
    def reset_param(self, list_size):
        self.list_view_point = [None]*list_size
        self.list_sight_rotation_matrix = [None]*list_size
        self.list_projected_img = [None]*list_size

    #タブ２のリスト更新用
    def update_movie_list(self):
        self.is_update_path_movie = True

    def update_path_movie(self):
        if self.is_update_path_movie:
            self.is_update_path_movie = False
            return True
        else:
            return False
    
    #タブ3のリスト更新用
    def update_frame_image_list(self):
        self.is_update_path_frame_image = True

    def update_path_frame_image(self):
        if self.is_update_path_frame_image:
            self.is_update_path_frame_image = False
            return True
        else:
            return False