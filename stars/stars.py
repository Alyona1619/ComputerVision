import numpy as np
from skimage import morphology, measure

cross = np.array([[1, 0, 0, 0, 1],
                  [0, 1, 0, 1, 0],
                  [0, 0, 1, 0, 0],
                  [0, 1, 0, 1, 0],
                  [1, 0, 0, 0, 1]])

plus = np.array([[0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [1, 1, 1, 1, 1],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0]])

image = np.load('files/stars.npy')

plus_image = morphology.binary_erosion(image, plus)
cross_image = morphology.binary_erosion(image, cross)

labeled_plus_image, num_plus = measure.label(plus_image, return_num=True)
labeled_cross_image, num_cross = measure.label(cross_image, return_num=True)

print("Количество плюсов:", num_plus)
print("Количество крестов:", num_cross)
print("Количество звездочек (плюсы + кресты): ", num_cross + num_plus)

# Количество звезд в виде плюса:  71
# Количество звезд в виде креста:  90
# Количество звезд:  161
