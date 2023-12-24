import cv2
import numpy as np
import zmq
from skimage.measure import regionprops

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://192.168.0.104:6556")

flimit = 60
slimit = 15


def fupdate(value):
    global flimit
    flimit = value


def supdate(value):
    global slimit
    slimit = value


cv2.namedWindow("Camera")
cv2.namedWindow("Mask")


c = -1
while True:
    buffer = socket.recv()
    c += 1
    arr = np.frombuffer(buffer, np.uint8)
    frame = cv2.imdecode(arr, -1)
    cv2.putText(frame, f"{c}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0))

    # image_path = os.path.join("fortask", f"image_task_cubes.png")
    # cv2.imwrite(image_path, frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (7, 7), 0)

    cannys = cv2.Canny(gauss, flimit, slimit)
    good_contours = cv2.dilate(cannys, None, iterations=2)  ###
    contours, _ = cv2.findContours(good_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circles = 0
    cubes = 0
    print(f"Total number of objects: {len(contours)}")

    for contour in contours:
        mask = np.zeros(frame.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 1, thickness=cv2.FILLED)

        props = regionprops(mask)[0]
        contour_area = props.area
        bbox_area = props.bbox_area

        fullness = contour_area / bbox_area
        print(fullness)
        if fullness > 0.7:  ###
            circles += 1
        else:
            print(fullness)
            cubes += 1

    print(f"Number of circles: {circles}, number of cubes: {cubes}")

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", cannys)

    key = cv2.waitKey(500)
    if key == ord("q"):
        break
