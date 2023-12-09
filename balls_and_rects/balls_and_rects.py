import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import cv2


def clustering(colors):
    clusters = []
    while colors:
        color1 = colors.pop(0)
        clusters.append([color1])
        for color2 in colors.copy():
            if abs(color1 - color2) < 5:
                clusters[-1].append(color2)
                colors.pop(colors.index(color2))
    return clusters


def outputting(clucters):
    for i, subarray in enumerate(clucters, 1):
        min_val = min(subarray)
        max_val = max(subarray)
        num_elements = len(subarray)
        print(f"Оттенок {i} ({min_val:.5f} - {max_val:.5f}): \t{num_elements} элемент{'ов' if num_elements > 1 else ''}")


image = plt.imread("files/balls_and_rects.png")
#print(image.shape)

hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

binary = image.mean(2) > 0
labeled = label(binary)
print(f"Total number of figures: {np.max(labeled)}")
print()

regions = regionprops(labeled)
h = hsv[:, :, 0]

rects_colors = []
circles_colors = []
counter = 0
for region in regions:
    pixels = h[region.coords]
    r = h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]
    #print(np.unique(r))
    if len(np.unique(r)) == 3:
        if counter == 0:
            circles_colors.extend(np.unique(r)[2:])
            counter += 1
        elif counter == 1:
            circles_colors.extend(np.unique(r)[1:2])
    elif len(np.unique(r)) == 1:
        rects_colors.extend(np.unique(r))
    else:
        circles_colors.extend(np.unique(r)[1:])


print(f"Total number of rects: {len(rects_colors)}")
rect_clusters = clustering(rects_colors)
outputting(rect_clusters)
print()
print(f"Total number of circles: {len(circles_colors)}")
circle_clusters = clustering(circles_colors)
outputting(circle_clusters)

# Total number of figures: 257
#
# Total number of rects: 135
# Оттенок 1 (69.13047 - 70.71432): 	32 элементов
# Оттенок 2 (19.68749 - 20.19802): 	22 элементов
# Оттенок 3 (219.75002 - 220.40817): 	29 элементов
# Оттенок 4 (300.00000 - 300.00003): 	13 элементов
# Оттенок 5 (109.72974 - 110.32259): 	17 элементов
# Оттенок 6 (149.71428 - 150.52631): 	22 элементов
#
# Total number of circles: 122
# Оттенок 1 (19.19999 - 20.20408): 	17 элементов
# Оттенок 2 (219.23077 - 220.36365): 	29 элементов
# Оттенок 3 (69.54547 - 70.45873): 	19 элементов
# Оттенок 4 (300.00000 - 300.00003): 	23 элементов
# Оттенок 5 (149.43394 - 150.37973): 	22 элементов
# Оттенок 6 (109.71429 - 110.40000): 	12 элементов

