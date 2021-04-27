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
        end = timeit.timeit()
        print("Init takes " + str(end - start) + "seconds")
        # self.image_size = self.data[0].size      #image -> each has (x, y) rgb vectors          
        self.data = np.array(self.data)
        # print(self.data[:10])
        # print(self.image_size)

    def refocus(self, alpha = 0):
        # for img in range(SHAPE[0]*SHAPE[1]):
        # start = timeit.timeit()
        # ret = np.mean(self.data, axis = 0) #np.imgshow
        # end = timeit.timeit()
        # print(end - start)
        # return ret
        self.output = []
        center = (SHAPE[0] // 2, SHAPE[1] // 2)
        for i in range(SHAPE[0]):
            for j in range(SHAPE[1]):
                dx = abs(i - center[0])
                dy = abs(j - center[1])
                shiftx = np.roll(self.data[i * SHAPE[1] + j], int(alpha * dx), axis = 0)
                shifty = np.roll(shiftx, int(alpha * dy), axis = 1)
                self.output.append(shifty)
        self.output = np.array(self.output)
        return np.mean(self.output, axis = 0)
                

    def apeture():
        pass

def main():
    lf = Lightfield("../temp/data/chess/")
    # print(lf.refocus())
    alpha = -1
    for alpha in range(5):
        print("writing the alpha =", alpha)
        ret = lf.refocus(alpha)
        plt.imsave("./results/" + "chess" + str(alpha) + ".png", ret)
        alpha += 0.5

main()