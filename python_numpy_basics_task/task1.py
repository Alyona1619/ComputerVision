import numpy as np
import matplotlib.pyplot as plt

for i in range(1, 7):
    file_name = f"files/figure{i}.txt"

    with open(file_name, 'r') as file:
        min_size = float(file.readline())
        _ = file.readline()

        lines = np.loadtxt(file)

        figure = [sum(line) for line in lines if 1 in line]

        if not figure:
            print(f"File {file_name} is empty")
        else:
            print(f"Nominal resolution {file_name}: {min_size / max(figure)}")


# image = np.loadtxt('figure1.txt', skiprows=1)
# plt.imshow(image, cmap='gray')
# plt.show()
