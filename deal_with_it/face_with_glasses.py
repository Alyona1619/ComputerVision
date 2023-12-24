import cv2
import numpy as np


def overlay_glasses(frame, glasses, x, y, w, h, width_factor=1.5, shift_factor=0.1):
    new_w = int(w * width_factor)
    glasses = cv2.resize(glasses, (new_w, h))

    x_shift = int(shift_factor * w)
    x -= x_shift

    glasses_gray = cv2.cvtColor(glasses, cv2.COLOR_BGR2GRAY)
    roi = frame[y:y + h, x:x + new_w]

    _, mask = cv2.threshold(glasses_gray, 25, 255, cv2.THRESH_BINARY)
    mask_not = cv2.bitwise_not(mask)

    glasses_fg = cv2.bitwise_and(glasses, glasses, mask=mask_not)
    roi_bg = cv2.bitwise_and(roi, roi, mask=mask)

    frame[y:y + h, x:x + new_w] = cv2.add(roi_bg, glasses_fg)


cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
glasses = cv2.imread("img/deal_with_it.png")
cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray, 1.3, 5)
    if len(eyes) == 2:
        # eyes = sorted(eyes, key=lambda x: x[0])
        (x1, y1, w1, h1) = eyes[0]
        (x2, y2, w2, h2) = eyes[1]
        x = min(x1, x2)
        y = min(y1, y2)
        w = max(x1 + w1, x2 + w2) - x
        h = max(y1 + h1, y2 + h2) - y
        overlay_glasses(frame, glasses, x, y, w, h, width_factor=1.5, shift_factor=0.2)
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
