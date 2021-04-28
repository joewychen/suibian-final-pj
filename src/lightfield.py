import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
import util
import timeit
import glob

SHAPE = (17,17)

class Lightfield:
    def __init__(self, dirpath):
        self.data = [] # 105
        self.output = []
        # info  = list(os.walk(dirpath))
        # filenames = info[0][2]
        #filenames.sort()
        start = timeit.timeit()
        extension = ".png"
        filenames = sorted(glob.glob(dirpath + "*" + extension))
        for f in filenames:
            img = plt.imread(f)
            self.data.append(img)
        # print(self.data)
        self.image_size = self.data[0].shape      #image -> each has (x, y) rgb vectors          
        self.data = np.array(self.data)
        end = timeit.timeit()
        print(self.image_size)
        print("Init takes " + str(end - start) + "seconds")


    def refocus(self, alpha = 0):
        # for img in range(SHAPE[0]*SHAPE[1]):
        # start = timeit.timeit()
        # ret = np.mean(self.data, axis = 0) #np.imgshow
        # end = timeit.timeit()
        # print(end - start)
        # return ret

        # self.output = []
        # center = (SHAPE[0] // 2, SHAPE[1] // 2)
        # for i in range(SHAPE[0]):
        #     for j in range(SHAPE[1]):
        #         dx = (i - center[0]) * -1
        #         dy = (j - center[1]) * -1
        #         shiftx = np.roll(self.data[i * SHAPE[1] + j], int(alpha * dx), axis = 0)
        #         shifty = np.roll(shiftx, int(alpha * dy) // 3 * 3, axis = 1)
        #         self.output.append(shifty)
        # #self.output = np.array(self.output)
        # return np.mean(self.output, axis = 0)
        self.output = []
        center = (SHAPE[0] // 2, SHAPE[1] // 2)
        for i in range(SHAPE[0]):
            for j in range(SHAPE[1]):
                dx = (i - center[0])
                dy = (j - center[1]) * -1
                shiftx = np.roll(self.data[(SHAPE[0] - 1 - i) * SHAPE[1] + SHAPE[1] - j - 1], int(alpha * dx), axis = 0)
                shifty = np.roll(shiftx, int(alpha * dy) // 3 * 3, axis = 1)
                self.output.append(shifty)
        self.output = np.array(self.output)
        return np.mean(self.output, axis = 0)
                

    def apeture():
        pass

def main():
    lf = Lightfield("../scene/chess/")
    # print(lf.refocus())
    alpha = -1
    for _ in range(5):
        print("writing the alpha =", alpha)
        ret = lf.refocus(alpha)
        plt.imsave("./results/" + "chess" + str(alpha) + ".png", ret)
        alpha += 0.5

main()