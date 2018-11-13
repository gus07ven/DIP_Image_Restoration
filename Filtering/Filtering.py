# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv
import numpy as np
import cv2
import math
from decimal import Decimal

class Filtering:
    image = None

    def __init__(self, image):
        """initializes the variables frequency filtering on an input image
        takes as input:
        image: the input image
        filter_name: the name of the mask to use
        cutoff: the cutoff frequency of the filter
        order: the order of the filter (only for butterworth
        returns"""
        self.image = image

    def padding_img(self, img, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize / 2)
        paddingImage = np.zeros((height + margin * 2, width + margin * 2), np.uint8)
        for j in range(margin):
                paddingImage[j,margin:margin+width] = img[0,0:width]
                paddingImage[j+height+margin,margin:margin+width] = img[height-1,0:width]

        paddingImage[margin:margin+height,margin:margin+width] = img[:]

        for j in range(margin):
            paddingImage[0:margin*2+height,j]=paddingImage[0:margin*2+height,margin]
            paddingImage[0:margin * 2 + height, j+width+margin] = paddingImage[0:margin * 2 + height, width+margin-1]

        return paddingImage

    # apply 3*3 mean filter
    def arithmetic_mean_filter(self, img, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize/2)

        paddingImg = self.padding_img(img, windowSize)
        newImg = np.zeros(img.shape[:2],np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((windowSize, windowSize), np.uint8)
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]
                average = np.sum(mask) / (windowSize**2)
                newImg[j][i] = int(average+0.5)
        return newImg

    def geometric_mean_filter(self, img, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize / 2)

        paddingImg = self.padding_img(img, windowSize)
        newImg = np.zeros(img.shape[:2], np.uint8)

        # mask = np.zeros((3, 3), np.uint8)
        for j in range(height):
            for i in range(width):
                mask = np.zeros((windowSize, windowSize), np.uint8)
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]
                multipleValue = Decimal(1)
                for l in range(windowSize):
                    for m in range(windowSize):
                        multipleValue *= mask[l][m]
                newImg[j][i] = int(math.pow(multipleValue, windowSize**(-2))+0.5)
        return newImg