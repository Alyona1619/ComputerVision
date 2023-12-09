import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
import cv2

image = plt.imread("files/balls_and_rects.png")
print(image.shape)

hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

binary = image.mean(2) > 0
labeled = label(binary)
print(f"Total number of figures: {np.max(labeled)}")

regions = regionprops(labeled)
h = hsv[:, :, 0]
colors = []

rects_colors = []
circles_colors = []
counter = 0
for region in regions:
    pixels = h[region.coords]
    r = h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]
    #print(np.unique(r))
    if len(np.unique(r)) == 3:
        print(list(np.unique(r)))
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
print(f"Total number of circles: {len(circles_colors)}")

clusters = []
while colors:
    color1 = colors.pop(0)
    clusters.append([color1])
    for color2 in colors.copy():
        if abs(color1 - color2) < 5:
            clusters[-1].append(color2)
            colors.pop(colors.index(color2))




for cluster in clusters:
    print(len(cluster))

plt.imshow(image)
plt.show()

print(sum(map(len, clusters)))
