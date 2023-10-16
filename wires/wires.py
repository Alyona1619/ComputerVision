import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from scipy.ndimage import binary_erosion

mask = np.array([[1], [1], [1]])


def wire_checker(image):
    erosied = binary_erosion(image, mask)
    labeled = label(erosied)

    total_wire_number = np.nonzero(labeled[:, 0])
    for i, wire_line in enumerate(total_wire_number[0], 1):
        wl = labeled[wire_line]
        wire_start = np.min(wl[wl != 0])
        wire_end = np.max(labeled[wire_line])
        parts = wire_end - wire_start + 1
        print(f'Wire number: {i}, parts: {parts}')
    print()


for i in range(1, 7):
    filename = f"files/wires{i}.npy.txt"
    image = np.load(filename)

    print(f"File {filename[6:]}")
    wire_checker(image)
    # plt.imshow(image, cmap='gray')
    # plt.show()

