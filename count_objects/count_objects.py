import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label


image = np.load('files/coins.npy.txt')

labeled = label(image)
labels, figures = np.unique(labeled, return_counts=True)
print("Общее количество объектов: ", labels[-1])  

variants, counts = np.unique(figures[1:], return_counts=True)
variant_count_dict = dict(zip(variants, counts))
for i, (value, count) in enumerate(variant_count_dict.items(), 1):
    print(f"Вид объекта {i} (с площадью {value}) встречается {count} раз")

# plt.imshow(image, cmap='gray')
# plt.show()

# Общее количество объектов:  50
# Вид объекта 1 (с площадью 69) встречается 10 раз.
# Вид объекта 2 (с площадью 145) встречается 13 раз.
# Вид объекта 3 (с площадью 305) встречается 12 раз.
# Вид объекта 4 (с площадью 609) встречается 15 раз.
