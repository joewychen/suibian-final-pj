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

class Lightfield:
    def __init__(self, dirpath, image_name):
        self.data = [] # 105
        self.output = []
        # info  = list(os.walk(dirpath))
        # filenames = info[0][2]
        # filenames.sort()
        print(dirpath)
        extension = ".png"
        filenames = sorted(glob.glob(dirpath + "*" + extension))
        # print("sorted filename: " + str(filenames))
        order, left = determine_file_processing_order(filenames, SHAPE[0], SHAPE[1], dirpath)
        if left:
            filenames = reorder_filename(filenames, SHAPE[0], SHAPE[1])
            order, left = determine_file_processing_order(filenames, SHAPE[0], SHAPE[1], dirpath)
            if left:
                raise ValueError("Changing order failure")
        start = time.time()
        self.data = readImage(filenames, image_name, SHAPE)
        # print(self.data)
        end = time.time()
        sys.stdout.write('\033[1A')
        print('\n')
        print("Preprocessing done! Preprocessing takes " + (str(int(end - start))) + " seconds")
        # self.image_size = self.data[0].size      #image -> each has (x, y) rgb vectors

        # print("Casting python list into numpy array...")
        # start = time.time()
        # self.data = np.array(self.data)
        # end = time.time()
        # print("List casting done! List casting takes " + str(int(end - start)) + " seconds")

    def refocus(self, alpha = 0):
        self.output = []
        center = (SHAPE[0] // 2, SHAPE[1] // 2)
        for i in range(SHAPE[0]):
            for j in range(SHAPE[1]):
                dx = (i - center[0]) * (-1 if order else 1)
                dy = (j - center[1]) * -1
                if (not order):
                    shiftx = np.roll(self.data[(SHAPE[0] - 1 - i) * SHAPE[1] + SHAPE[1] - j - 1], int(alpha * dx), axis = 0)
                    shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
                else:
                    shiftx = np.roll(self.data[(i) * SHAPE[1] + j], int(alpha * dx), axis = 0)
                    shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
                self.output.append(shifty)
                sys.stdout.write("\r" + "Refocusing" + "." * (int((i * SHAPE[1] + j) / (SHAPE[0] * SHAPE[1]) * 10)) + " " + str(int((i * SHAPE[1] + j + 1) / (SHAPE[0] * SHAPE[1]) * 100)) + "%")
        # sys.stdout.write("\nList casting again...")
        # self.output = np.array(self.output)
        # sys.stdout.write("\nList casting done!")
        return np.mean(self.output, axis = 0)

    def refocus_sol(self, imgs, scale):
        # Refocuses Image by Shifting Array of Images
        shifted_imgs = []
        ref_array = np.arange(289).reshape((17, 17))
        center_coord = (np.floor(ref_array.shape[0]/2.), np.floor(ref_array.shape[0]/2.))
        #ref_array = np.flipud(ref_array)

        for x in range(ref_array.shape[0]):
            for y in range(ref_array.shape[1]):
                img = imgs[ref_array[x][y]]
                dx = int(x - center_coord[0]) * -1
                dy = int(y - center_coord[1]) * -1
                shifted_img = np.roll(img, int(dx * scale), axis=0)
                shifted_img = np.roll(shifted_img, int(dy * scale), axis=1)
                shifted_imgs.append(shifted_img)

        refocused_img = np.mean(shifted_imgs, axis=0)
        return refocused_img


    def apeture(self, radius):
        assert(radius >= 0 and radius <= SHAPE[0] // 2)
        # if radius < 0 and radius > SHAPE[0] // 2: return
        self.output = []
        radius = int(radius)
        center = (SHAPE[0] // 2, SHAPE[1] // 2)
        row_start = center[0] - radius
        col_start = center[1] - radius
        for r in range(row_start, row_start + radius * 2 + 1):
            for c in range(col_start, col_start + radius * 2 + 1):
                self.output.append(self.data[r * SHAPE[1] + c])
        return np.mean(self.output, axis=0)

""" Alpha determines the refocusing distance in the image, while the camera position
will also affect alpha's behavior."""
# def main():
#     lf = Lightfield("../scene/" + image_name + "/")
#     # print(lf.refocus())
#     base = alpha = -2
#     for i in range(9):
#         print("writing image with alpha =", alpha)
#         ret = lf.refocus(alpha)
#         sys.stdout.write("\nWriting to the disk buffer...")
#         plt.imsave("./results/" + image_name + "/" + image_name + str(i) + " " + str(alpha) + ".png", ret)
#         sys.stdout.write("\nRefocused with alpha = " + str(alpha) + " has ready!\n")
#         alpha += 0.5
# main()
