import math
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def dist(pos1, pos2):
    s = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    return round(s, 5)


def regioning(image_path):
    image = np.load(image_path)
    labeled = label(image)
    regions = regionprops(labeled)
    return regions


def track_balls(image_path):
    regions = regioning(image_path)
    ball_centers = [(0, 0), (0, 0), (0, 0)]
    for r in regions:
        center = r.centroid

        if dist(center, trajectory_data[0][-1]) < dist(center, trajectory_data[1][-1]) \
                and dist(center, trajectory_data[0][-1]) < dist(center, trajectory_data[2][-1]):
            ball_centers[0] = center
        elif dist(center, trajectory_data[1][-1]) < dist(center, trajectory_data[0][-1]) \
                and dist(center, trajectory_data[1][-1]) < dist(center, trajectory_data[2][-1]):
            ball_centers[1] = center
        else:
            ball_centers[2] = center

    return ball_centers


trajectory_data = [[] for i in range(3)]

# заполнение в trajectory_data координат центра каждого шара
regions = regioning("files/out/h_0.npy")
ball_centers = []
for r in regions:
    center = r.centroid
    ball_centers.append(center)
for j, center in enumerate(ball_centers):
    trajectory_data[j].append(center)

# заполнение остальных координат центра каждого шара (с отслеживанием предыдущей координаты центра и подбором наиболее
# вероятной следующей точки) с помощью функции track_balls
for i in range(1, 100):
    image_path = f"files/out/h_{i}.npy"
    ball_centers = track_balls(image_path)
    for j, center in enumerate(ball_centers):
        trajectory_data[j].append(center)

for i, trajectory in enumerate(trajectory_data):
    y, x = zip(*trajectory)
    plt.plot(x, y, label=f"Ball {i + 1}")
plt.legend()
plt.title("Trajectories of Balls")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
