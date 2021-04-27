import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

def readImage(filename):
    # img = mpimg.imread(filename)
    # print(img)
    # plt.imshow(img)
    img = Image.open(filename)
    pix = img.load()
    #print(img.size, pix)
    return list(img.getdata())
    
# def main():
#     print(readImage("../scene/original/IMG_7334.JPG"))

# main()