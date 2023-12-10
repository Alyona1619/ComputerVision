import time
import cv2
import keyboard
import numpy as np
from mss import mss
import pyautogui as ptg
import matplotlib.pyplot as plt

trex_path = 'trex1.png'


def find_trex(screen, template):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc, (max_loc[0] + w, max_loc[1] + h)


def find_lower_obstacle(screen_rect, trex_top_left, sct):
    obstacle_area = {"top": screen_rect["top"] + trex_top_left[1] + round(h/2), #+305
                     "left": screen_rect["top"] + trex_top_left[0] + w, # +72
                     "width": 100,
                     "height": 50}
    obstacle_area1 = np.array(sct.grab(obstacle_area))
    plt.imshow(obstacle_area1)
    plt.show()

    gray_obstacle = cv2.cvtColor(obstacle_area1, cv2.COLOR_BGR2GRAY)
    _, thresholded_obstacle = cv2.threshold(gray_obstacle, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print(thresholded_obstacle)
    return obstacle_area, cv2.countNonZero(thresholded_obstacle) > 0


template_trex = cv2.imread(trex_path, cv2.IMREAD_GRAYSCALE)
w, h = template_trex.shape[::-1]
with mss() as sct:
    screen_rect = {"top": 300, "left": 79, "width": 700, "height": 180}
    screen = np.array(sct.grab(screen_rect))
    plt.imshow(screen)
    plt.show()
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    trex_top_left, trex_bottom_right = find_trex(screen, template_trex)
    print(trex_top_left)
    while True:

        obstacle_area = find_lower_obstacle(screen_rect, trex_top_left, sct)[0]
        # cv2.rectangle(screen, (screen_rect["left"], screen_rect["top"]),
        #               (screen_rect["left"] + screen_rect["width"], screen_rect["top"] + screen_rect["height"]),
        #               (255, 0, 0), 2)
        #
        # cv2.rectangle(screen, trex_top_left, trex_bottom_right, (0, 255, 0), 2)
        #
        # cv2.rectangle(screen, (obstacle_area["left"], obstacle_area["top"]),
        #               (obstacle_area["left"] + obstacle_area["width"], obstacle_area["top"] + obstacle_area["height"]),
        #               (0, 0, 255), 2)
        #
        # cv2.imshow("Marked Image", screen)
        # cv2.waitKey(1)

        is_obs = find_lower_obstacle(screen_rect, trex_top_left, sct)[1]
        # plt.imshow(obstacle_area, cmap='gray')
        # plt.show()
        if is_obs:
            ptg.press('up')
            time.sleep(0.2)
        else:
            time.sleep(0.01)
            ptg.keyDown('down')
        if keyboard.is_pressed('q'):
            break

cv2.destroyAllWindows()
