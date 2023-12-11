import cv2
import numpy as np
import random

colors = {
    'b': {'lower': (90, 150, 120), 'upper': (115, 255, 255), 'color': (255, 0, 0)},
    'r': {'lower': (0, 100, 140), 'upper': (12, 255, 255), 'color': (0, 0, 255)},
    'g': {'lower': (60, 100, 100), 'upper': (80, 255, 255), 'color': (0, 255, 0)},
    'y': {'lower': (25, 100, 100), 'upper': (33, 255, 255), 'color': (0, 255, 255)}
}


def find_ball(frame, hsv, lower, upper, color):
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        m = cv2.moments(c)
        center = int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])
        if r > 10:
            cv2.circle(frame, (int(x), int(y)), int(r), color, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color, 2)
            return int(x), int(y), int(r), center
    return None, None, None, None


capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
capture.set(cv2.CAP_PROP_EXPOSURE, -6)

cv2.namedWindow("Camera")

order = 'brgy'
order = ''.join(random.sample(order, len(order)))
print(order)

while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    balls = {}
    for color_name, params in colors.items():
        x, y, r, c = find_ball(frame, hsv, params['lower'], params['upper'], params['color'])
        balls[color_name] = {'x': x, 'y': y, 'r': r, 'center': c}

    if all(balls[color]['x'] is not None for color in colors):
        colors_dict = {color: balls[color]['center'] for color in order}

        if (
                colors_dict[order[0]][0] < colors_dict[order[1]][0] and
                abs(colors_dict[order[0]][1] - colors_dict[order[1]][1]) <= 50 and
                colors_dict[order[2]][0] < colors_dict[order[3]][0] and
                abs(colors_dict[order[2]][1] - colors_dict[order[3]][1]) <= 50
        ):
            cv2.putText(frame, "Win", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        else:
            cv2.putText(frame, "Wrong", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    else:
        cv2.putText(frame, "Show me all balls", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
