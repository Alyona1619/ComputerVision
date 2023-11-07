import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    euler = region.euler_number
    match euler:
        case -1:
            euler = region.euler_number
            if euler == -1:  # B or 8
                if region.image.mean(0)[0] == 1.0:
                    return "B"
                return "8"

        case 0:  # A or 0 or P or D or *
            if region.image.mean(0)[0] == 1.0:
                if region.eccentricity < 0.6:
                    return "D"
                if region.eccentricity > 0.6:
                    return "P"

            if 1 in region.image.mean(1):
                return "*"

            tmp = region.image.copy()
            tmp[-1, :] = 1.0
            tmp_regions = regionprops(label(tmp))
            if tmp_regions[0].euler_number == -1.0:
                return "A"

            return "0"

        case 1:  # 1 W X / *
            tmp1 = region.image.copy()
            tmp1[-1, :] = 1.0
            tmp_regions1 = regionprops(label(tmp1))
            if 1 in tmp_regions1[0].image.mean(0):
                if tmp_regions1[0].euler_number == 0.0:
                    return '*'
                else:
                    return "1"
            tmp = region.image.copy()
            tmp[-1, :] = 1.0
            tmp[0, :] = 1.0
            tmp_regions = regionprops(label(tmp))
            euler = tmp_regions[0].euler_number
            if euler == -1:
                return "X"
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return "/"
            return "*"
        case _:
            return "?"


image = plt.imread('files/symbols.png')
binary = image.mean(2)
binary[binary > 0] = 1
labeled = label(binary)
print("Number of figures:", labeled.max())
regions = regionprops(labeled)

counts = {}

for region in regions:
    symbol = recognize(region)
    if symbol not in counts:
        counts[symbol] = 0
    counts[symbol] += 1

print(counts)
print(f"Character recognition: {(1.0 - counts.get('?', 0) / labeled.max()) * 100}%")
# Number of figures: 400
# {'D': 31, 'X': 23, '/': 35, '*': 41, '1': 40, 'A': 35, 'P': 37, '8': 33, '-': 31, 'B': 38, 'W': 26, '0': 30}
# Character recognition: 100.0%

# print(labeled[regions[0].slice]) # D
# print(labeled[regions[11].slice]) #D
# print(labeled[regions[8].slice]) #P
# print(labeled[regions[16].slice]) #P

# plt.imshow(labeled)
# plt.show()
