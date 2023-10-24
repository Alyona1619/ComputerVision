import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage import morphology, measure
from skimage.draw import rectangle

mask_rect = np.array([[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1]], np.uint8)
mask_up = np.array([[1, 0, 0, 1],
                    [1, 0, 0, 1],
                    [1, 1, 1, 1],
                    [1, 1, 1, 1]])
mask_down = np.array([[1, 1, 1, 1, 1, 1],
                      [1, 1, 1, 1, 1, 1],
                      [1, 1, 0, 0, 1, 1],
                      [1, 1, 0, 0, 1, 1]])
mask_right = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 0, 0],
                       [1, 1, 0, 0],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]])
mask_left = np.array([[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [0, 0, 1, 1],
                      [0, 0, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 1]])

image = np.load('files/ps.npy.txt')
labeled = label(image)
labels, figures = np.unique(labeled, return_counts=True)
print("Общее количество объектов: ", labels[-1])

rect = morphology.binary_erosion(image, mask_rect)
labeled_rect, num_rect = measure.label(rect, return_num=True)
# Находим прямоугольники и удаляем их
for label in range(1, num_rect + 1):
    label_indices = np.where(labeled_rect == label)
    min_y, min_x = np.min(label_indices, axis=1)
    max_y, max_x = np.max(label_indices, axis=1)

    rr, cc = rectangle(start=(min_y, min_x), end=(max_y, max_x))
    image[rr, cc] = 0
print("Количество прямоугольников:", num_rect)

masks = [mask_up, mask_down, mask_left, mask_right]
labels = ["up", "down", "left", "right"]

for mask, label in zip(masks, labels):
    eroded_image = morphology.binary_erosion(image, mask)
    labeled_image, num = measure.label(eroded_image, return_num=True)
    print(f"Количество {label}:", num)

# Общее количество объектов:  500
# Количество прямоугольников: 92
# Количество up: 95
# Количество down: 96
# Количество left: 123
# Количество right: 94
