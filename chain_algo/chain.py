import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x + 1), (y, x - 1), (y - 1, x), (y + 1, x)


def neighbours8(y, x):
    return neighbours4(y, x) + ((y - 1, x + 1), (y + 1, x + 1), (y - 1, x - 1), (y + 1, x - 1))


def get_boundaries(image_labeled, lbl=1, connectivity=neighbours8):
    pos = np.where(image_labeled == lbl)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > image_labeled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > image_labeled.shape[1] - 1:
                bounds.append((y, x))
                break
            elif image_labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds


def chaining(labeled, label, connectivity=neighbours8):
    chain = []
    boundaries = get_boundaries(labeled, label)
    start = boundaries[0]
    current = boundaries[1]
    while current != start:
        neighbours = connectivity(current[0], current[1])
        for neighbour in neighbours:
            if boundaries.count(neighbour):
                chain.append(neighbours.index(neighbour))
                boundaries.remove((current[0], current[1]))
                current = neighbour
                break
    chain.append(0)
    return chain


print("First test")
image1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0, 1, 1, 1, 0],
                   [0, 1, 1, 1, 0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0]])
labeled = label(image1)
chain1 = chaining(labeled, 1)
print("Chain 1:", chain1)
chain2 = chaining(labeled, 2)
print("Chain 2:", chain2)

image = np.load('files/similar.npy')
plt.imshow(image, cmap='gray')
plt.show()

labeled = label(image)

print("Second test")
print("Chain 1:", chaining(labeled, 1))
print("Chain 2:", chaining(labeled, 2))
print("Chain 3:", chaining(labeled, 3))
print("Chain 4:", chaining(labeled, 4))
