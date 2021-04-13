import os
import sys
import numpy as np
from PIL import Image

barc_shape = (264, 264)

def load_image(file: str) -> np.array:
    return np.array(Image.open(file))

def decode(file: str) -> np.array:
    img = load_image(file)
    barcode = []
    row_patch = 3
    col_patch = 3
    row_cnt = 0
    insert_index = col_patch // 2
    for row in range(barc_shape[0]):
        col_cnt = 0
        barcode.append([])
        for col in range(barc_shape[1]):
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
                if img[row_cnt][col_cnt + insert_index][0] == mean[0]:
                    barcode[-1].append(255)
                else:
                    barcode[-1].append(0)
            else:
                if img[row_cnt][col_cnt + insert_index][0] == mean[0]:
                    barcode[-1].append(0)
                else:
                    barcode[-1].append(255)
            col_cnt += col_patch
        row_cnt += row_patch
    decoded_barcode = np.uint8(barcode)
    Image.fromarray(decoded_barcode).save("Decoded_barcode_inv.png")

if __name__ == "__main__":
    decode("Encoded_image.png")