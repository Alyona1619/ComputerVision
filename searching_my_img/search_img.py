import cv2
import numpy as np
from skimage import measure


# import time
# import os


def count_objects_in_frame(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    labeled = measure.label(binary_image)

    # обводка объектов
    # binary_image_with_rectangles = binary_image.copy()
    # binary_image_with_rectangles = cv2.cvtColor(binary_image_with_rectangles, cv2.COLOR_GRAY2BGR)
    # for region in measure.regionprops(labeled):
    #     y_min, x_min, y_max, x_max = region.bbox
    #     cv2.rectangle(binary_image_with_rectangles, (x_min, y_min), (x_max, y_max), (21, 21, 217), 2)

    object_count = len(np.unique(labeled)) - 1

    return object_count, binary_image


def analyze_video(path):
    cap = cv2.VideoCapture(path)

    count_frames_with_13objects = 0
    # image_counter = 0
    # start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Анализ текущего кадра
        objects_count, frame_with_rectangles = count_objects_in_frame(frame)
        # cv2.imshow("Frame with Rectangles", frame_with_rectangles)
        # time.sleep(4)

        # сохранение кадров
        # image_path = os.path.join("fortask", f"image_{image_counter}.png")
        # cv2.imwrite(image_path, frame_with_rectangles)
        # image_counter += 1

        # Таймер для вывода сообщения каждые 10 секунд
        # elapsed_time = time.time() - start_time
        # if elapsed_time >= 10:
        #     print("Looking for pictures...")
        #     start_time = time.time()

        if objects_count == 13:
            count_frames_with_13objects += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(
        f"Видео содержит {count_frames_with_13objects} кадров с изображением от Алёны Горелик (планета со звездочками)")
    # Видео содержит 186 кадров с изображением от Алёны Горелик (планета со звездочками).
    cap.release()


if __name__ == "__main__":
    video_path = "files/output.avi"
    analyze_video(video_path)
