import numpy as np

for i in range(9):
    
    
    trueA = np.loadtxt(f"true_camera_pos/patarnA/camera_{i}.txt")
    xA = np.loadtxt(f"patarnAA/calib_camera_{i+1}/camera_position.txt", delimiter=',')
    np.set_printoptions(precision=3)

    np.savetxt(f"savetxt/A/true_camera_{i+1}.txt", trueA, fmt="%.3f")
    np.savetxt(f"savetxt/A/camera_{i+1}.txt", xA, fmt="%.3f")

    d = np.sqrt((trueA[0]-xA[0])**2 + (trueA[1]-xA[1])**2 + (trueA[2]-xA[2])**2)
    d= np.array([d])
    np.set_printoptions(precision=3)
    np.savetxt(f"savetxt/A/d_{i+1}.txt", d, fmt="%.3f")

    trueB = np.loadtxt(f"true_camera_pos/patarnA/camera_{i}.txt")
    xB = np.loadtxt(f"patarnAA/calib_camera_{i+1}/camera_position.txt", delimiter=',')
    np.set_printoptions(precision=3)

    np.savetxt(f"savetxt/B/true_camera_{i+1}.txt", trueB, fmt="%.3f")
    np.savetxt(f"savetxt/B/camera_{i+1}.txt", xB, fmt="%.3f")

    d = np.sqrt((trueB[0]-xB[0])**2 + (trueB[1]-xB[1])**2 + (trueB[2]-xB[2])**2)
    d = np.array([d])
    np.set_printoptions(precision=3)
    np.savetxt(f"savetxt/B/d_{i+1}.txt", d, fmt="%.3f")