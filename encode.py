import os
import sys
import numpy as np
from PIL import Image

def load_image(file: str) -> np.array:
    return np.array(Image.open(file))

def encode(image_file: str, barcode_file: str) -> None:
    img = load_image(image_file)
    barc = load_image(barcode_file)
    if img.shape[0] < 3 * barc.shape[0] or img.shape[1] < 3 * barc.shape[1]:
        raise ValueError("Cannot encode image size is too small!")
    row_patch = 3
    col_patch = 3
    row_cnt = 0
    insert_index = col_patch // 2
    for row in range(barc.shape[0]):
        col_cnt = 0
        for col in range(barc.shape[1]):
            temp = img[row_cnt][col_cnt : col_cnt + col_patch].tolist()
            temp.pop(insert_index)
            mean = temp[0]
            if len(temp) - 1:
                for i in temp[1:]:
                    mean[0] += i[0]
                    mean[1] += i[1]
                    mean[2] += i[2]
            mean[0] //= len(temp)
            mean[1] //= len(temp)
            mean[2] //= len(temp)
            if mean[0] != 255 or mean[1] != 255 or mean[2] != 255:
                insert = np.array(mean) + barc[row][col] * 10
            else:
                insert = np.array(mean) + (barc[row][col] - 1) * 10
            img[row_cnt][col_cnt + insert_index] = insert
            col_cnt += col_patch
        row_cnt += row_patch
    encoded_image = np.uint8(img)
    Image.fromarray(encoded_image).save("Encoded_image.png")
if __name__ == "__main__":
    encode("image.jpg", "v2Phone.png")