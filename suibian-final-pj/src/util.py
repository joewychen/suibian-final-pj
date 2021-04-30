import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import sys

""" Reading images from filenames list """
def readImage(filenames, image_name, SHAPE):
    data = []
    for f in filenames:
        img = plt.imread(f)
        data.append(img)
        sys.stdout.write("\r" + "Loading " + image_name + "'s images" + "." * (int((len(data) / (SHAPE[0] * SHAPE[1])) * 10)) + " " + str(int((len(data) / (SHAPE[0] * SHAPE[1])) * 100)) + " %")
    return data

""" Filenames contain important information for camera position, those information may be represented by 
    filename = "out_00_00_-859.738525_1022.898743", where 00_00_ represents the position of lens, 
    and -859.73 represents y position, and 1022.89 represents x position. We observed that all picture in the first
    row must be going from left position to right position, while y position does not guarantee to always have exactly the same
    pattern. Therefore, we must determine whether y position goes from top -> bottom or bottom -> top.
    """
def determine_file_processing_order(filenames, x_max, y_max, dirpath):
    first_image = filenames[0] #out_00_00_
    last_row_first_image = filenames[(x_max - 1) * y_max] #out_16_00_
    last_col_first_row = filenames[x_max - 1] #out_00_16
    first_image = first_image[len(dirpath) + 10:]
    last_row_first_image = last_row_first_image[len(dirpath) + 10:]
    last_col_first_row = last_col_first_row[len(dirpath) + 10:]
    if first_image[-4:] != ".png" or last_row_first_image[-4:] != ".png":
        raise ValueError("Non png files are not supported")
    first_image = first_image[:-4]
    last_row_first_image = last_row_first_image[:-4]
    last_col_first_row = last_col_first_row[:-4]
    f_ = find_char(first_image)
    l_ = find_char(last_row_first_image)
    c_ = find_char(last_col_first_row)
    first_val = float(first_image[:f_])
    last_val = float(last_row_first_image[:l_])

    first_x = float(first_image[f_+1:])
    last_x = float(last_col_first_row[c_+1:])
    return first_val > last_val, first_x > last_x

def find_char(filename):
    for i in range(len(filename)):
        if filename[i] == "_":
            return i
    raise ValueError("String value can't be parsed")

""" In case of going from right to left, we need extra handling. """
def reorder_filename(filenames, x_max, y_max):
    res = []
    for i in range(x_max):
        res += ((filenames[i * y_max : (i+1) * y_max])[::-1])
    return res