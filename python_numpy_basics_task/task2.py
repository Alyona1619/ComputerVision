import numpy as np

img1 = np.loadtxt('files/img1.txt', skiprows=1)
img2 = np.loadtxt('files/img2.txt', skiprows=1)

y1, x1 = np.where(img1 != 0)
y2, x2 = np.where(img2 != 0)

print(f"Offset (y:{min(y2) - min(y1)}, x:{min(x2) - min(x1)})")  # Offset (y:-4, x:10)
