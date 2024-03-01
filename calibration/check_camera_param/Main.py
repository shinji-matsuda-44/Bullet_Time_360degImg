import sys
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

def read_txt(txtFname):
    data = np.loadtxt(txtFname, delimiter = ',')
    return data

def main(args):
    rotation_matrix = read_txt(args[1])
    position = read_txt(args[2])

    # Create a 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw camera position
    ax.scatter(position[0], position[1], position[2], c='r', marker='o')

    # Draw camera orientation
    for i in range(3):
        end_point = position + rotation_matrix[:, i]
        ax.quiver(position[0], position[1], position[2],
                end_point[0], end_point[1], end_point[2],
                color='b')

    # Set aspect of the plot to be equal
    ax.set_box_aspect([1, 1, 1])

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Show the plot
    plt.show()

# 例: 回転行列と並進ベクトル
rotation_matrix = np.array([[1, 0, 0],
                            [0, 0, -1],
                            [0, 1, 0]])

translation_vector = np.array([1, 2, 3])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('引数の数が正しくありません。以下の引数を指定してください')
        print("1. 回転行列")
        print("2. 並進ベクトル")
        sys.exit(1)
    else:
        main(sys.argv)