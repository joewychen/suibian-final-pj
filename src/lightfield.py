import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cupy as np
from PIL import Image
import util
import time
import glob
import sys
from util import *

SHAPE = (17,17)

# image_name = "ball"

order = 0
left = 0
# initialize current position to be at the center image.
cur_pos = (8, 8)

class Lightfield:
    def __init__(self, dirpath, image_name):
        self.data = [] # 105
        self.output = []
        # info  = list(os.walk(dirpath))
        # filenames = info[0][2]
        # filenames.sort()
        extension = ".png"
        filenames = sorted(glob.glob(dirpath + "*" + extension))
        # print("sorted filename: " + str(filenames))
        order, left = determine_file_processing_order(filenames, SHAPE[0], SHAPE[1], dirpath)
        if left:
            filenames = reorder_filename(filenames, SHAPE[0], SHAPE[1])
            order, left = determine_file_processing_order(filenames, SHAPE[0], SHAPE[1], dirpath)
            if left:
                raise ValueError("Changing order failure")
        image_arr = [[None for _ in range(SHAPE[1])] for _ in range(SHAPE[0])]
        for i in range(SHAPE[0]):
            for j in range(SHAPE[1]):
                image_arr[i][j] = filenames[i * SHAPE[1] + j]
        start = time.time()
        if os.path.exists("../docs/" + image_name):
            self.data = read_from_a_file(image_name)
        else:
            self.data = readImage(filenames, image_name, SHAPE)
            write_to_a_file(image_name, self.data)
        # print(self.data)
        end = time.time()
        # sys.stdout.write('\033[1A')
        print('\n')
        print("Preprocessing done! Preprocessing takes " + (str(int(end - start))) + " seconds")
        # self.image_size = self.data[0].size      #image -> each has (x, y) rgb vectors

        # print("Casting python list into numpy array...")
        # start = time.time()
        # self.data = np.array(self.data)
        # end = time.time()
        # print("List casting done! List casting takes " + str(int(end - start)) + " seconds")

    def refocus(self, alpha, imgs, size):
        output = []
        center = (size[0] // 2, size[1] // 2)
        for i in range(size[0]):
            for j in range(size[1]):
                dx = (i - center[0]) * (-1 if order else 1)
                dy = (j - center[1]) * -1
                if (not order):
                    shiftx = np.roll(imgs[(size[0] - 1 - i) * size[1] + size[1] - j - 1], int(alpha * dx), axis = 0)
                    shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
                else:
                    shiftx = np.roll(imgs[(i) * size[1] + j], int(alpha * dx), axis = 0)
                    shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
                output.append(shifty)
                sys.stdout.write("\r" + "Refocusing" + "." * (int((i * size[1] + j) / (size[0] * size[1]) * 10)) + " " + str(int((i * size[1] + j + 1) / (size[0] * size[1]) * 100)) + "%")
        # sys.stdout.write("\nList casting again...")
        # self.output = np.array(self.output)
        # sys.stdout.write("\nList casting done!")
        return np.mean(output, axis = 0)

    # def refocus(self, alpha = 0, imgs, size):
    #     self.output = []
    #     center = (SHAPE[0] // 2, SHAPE[1] // 2)
    #     for i in range(SHAPE[0]):
    #         for j in range(SHAPE[1]):
    #             dx = (i - center[0]) * (-1 if order else 1)
    #             dy = (j - center[1]) * -1
    #             if (not order):
    #                 shiftx = np.roll(self.data[(SHAPE[0] - 1 - i) * SHAPE[1] + SHAPE[1] - j - 1], int(alpha * dx), axis = 0)
    #                 shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
    #             else:
    #                 shiftx = np.roll(self.data[(i) * SHAPE[1] + j], int(alpha * dx), axis = 0)
    #                 shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
    #             self.output.append(shifty)
    #             sys.stdout.write("\r" + "Refocusing" + "." * (int((i * SHAPE[1] + j) / (SHAPE[0] * SHAPE[1]) * 10)) + " " + str(int((i * SHAPE[1] + j + 1) / (SHAPE[0] * SHAPE[1]) * 100)) + "%")
    #     # sys.stdout.write("\nList casting again...")
    #     # self.output = np.array(self.output)
    #     # sys.stdout.write("\nList casting done!")
    #     return np.mean(self.output, axis = 0)


    def apeture(self, radius):
        assert(radius >= 0 and radius <= SHAPE[0] // 2)
        # if radius < 0 and radius > SHAPE[0] // 2: return
        output = []
        radius = int(radius)
        assert radius <= cur_pos[0]
        assert radius <= cur_pos[1]
        row_start = cur_pos[0] - radius
        col_start = cur_pos[1] - radius
        for r in range(row_start, row_start + radius * 2 + 1):
            for c in range(col_start, col_start + radius * 2 + 1):
                output.append(self.data[r * SHAPE[1] + c])
        return output
        # return np.mean(self.output, axis=0)

    def combine(self, alpha, radius):
        imgs = self.apeture(radius)
        ret = self.refocus(alpha, imgs, (1+ radius * 2, 1 + radius * 2))
        return ret
