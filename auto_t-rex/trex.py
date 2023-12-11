import time
import cv2
import keyboard
import numpy as np
from mss import mss
import pyautogui as ptg
import matplotlib.pyplot as plt

trex_path = 'trex1.png'  # прыгает 555


def find_trex(screen, template):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc, (max_loc[0] + w, max_loc[1] + h)


def find_lower_obstacle(screen_rect, trex_top_left, sct, shift):
    print(trex_top_left)  # 128 104 9...
    if trex_top_left[1] > 104:
        obstacle_area = {"top": screen_rect["top"] + trex_top_left[1],  # +305 round(h/2)
                         "left": screen_rect["left"] + trex_top_left[0] + w,  # +w+72
                         "width": 40,
                         "height": 1}
    else:
        obstacle_area = {"top": screen_rect["top"] + trex_top_left[1] + round(h/3)*2,  # +305 round(h/2)
                         "left": screen_rect["left"] + trex_top_left[0] + w,  # +w+72
                         "width": 8+shift,
                         "height": 15}
    obstacle_area1 = np.array(sct.grab(obstacle_area))
    #plt.imshow(obstacle_area1)
    #plt.show()
    gray_obstacle = cv2.cvtColor(obstacle_area1, cv2.COLOR_BGR2GRAY)
    _, thresholded_obstacle = cv2.threshold(gray_obstacle, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return cv2.countNonZero(thresholded_obstacle) > 0


def count_shift():
    current_time = time.time()
    score = (current_time - start_time) * 10
    shift = int((score // 100) * 7.5)
    return shift


template_trex = cv2.imread(trex_path, cv2.IMREAD_GRAYSCALE)
w, h = template_trex.shape[::-1]

start_time = time.time()
with mss() as sct:
    screen_rect = {"top": 300, "left": 79, "width": 700, "height": 160}
    screen = np.array(sct.grab(screen_rect))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    trex_top_left, trex_bottom_right = find_trex(screen, template_trex)

    while True:
        shift = count_shift()
        is_obs = find_lower_obstacle(screen_rect, trex_top_left, sct, shift)
        if is_obs:
            ptg.press('up')
            time.sleep(0.2)
        else:
            pass
        if keyboard.is_pressed('q'):
            break

cv2.destroyAllWindows()
