import cv2
import os

smallest_area = 10800
biggest_area = 14500


def orientation_fix(image):
    height, width = image.shape
    if height > width:
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return rotated_image
    else:
        return image


def resizing(image):
    scale_percent = 20  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim)
    return resized


def count_pencils(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = orientation_fix(image)
    imgRS = resizing(image)

    blur = cv2.GaussianBlur(imgRS, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    thresh = cv2.bitwise_not(th3)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counter = 0
    for c in contours:
        area = cv2.contourArea(c)

        if biggest_area > area > smallest_area:
            counter += 1

        # To look at the areas on the picture
        # x, y, w, h = cv2.boundingRect(c)
        # cv2.rectangle(imgRS, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(imgRS, f'Area: {area}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.imshow(image_path, imgRS)
    return counter


folder_path = "pencils"
pencils_count = []
file_list = os.listdir(folder_path)
for file_name in file_list:
    if file_name.lower().endswith('.jpg'):
        image_path = os.path.join(folder_path, file_name)
        pencils_count.append(count_pencils(image_path))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

print(f'Количество карандашей: {sum(pencils_count)}')  # 21
