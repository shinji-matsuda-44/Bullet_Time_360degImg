import os
import glob
from PIL import Image

class GenerateGIF:
    def __init__(self):
        pass

    def generateGIF(self, input_folder):
        # 静止画像のファイル名リスト
        input_image_filenames = [] 
        file_names = glob.glob(os.path.join(input_folder, "*.jpg"))
        for filename in file_names:
            input_image_filenames.append(filename)

        # 生成するGIF画像のファイル名
        output_gif_filename = 'output.gif' 

        # 静止画像をImageオブジェクトに読み込み
        frames = [Image.open(filename) for filename in input_image_filenames]

        # フレーム間の時間間隔（ミリ秒）を指定
        frame_duration = 200  # 例として200ミリ秒に設定

        # GIF画像を保存する
        output_folder = os.path.join(input_folder, output_gif_filename)
        frames[0].save(output_folder, save_all=True, append_images=frames[1:], loop=0, duration=frame_duration)  # durationはフレーム間の時間間隔（ミリ秒）

        print("GIF画像が生成されました。")