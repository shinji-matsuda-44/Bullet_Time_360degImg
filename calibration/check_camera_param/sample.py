import glob
import numpy as np

def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

#group_1ディレクトリ下のディレクトリ群を取得
folders = glob.glob('group_1/*')
print(folders)

#ディレクトリ群から一組ずつtxtファイルを読み取る
for i in range(len(folders)):
    rotation_matrix = read_txt(folders[0] + '/rotation_matrix.txt')
    print(rotation_matrix)
    tranlational_vector = read_txt(folders[0] + '/translational_vector.txt')
    print(tranlational_vector.reshape(3,1))