# For this part of the assignment, You can use inbuilt functions to compute the fourier transform
# You are welcome to use fft that are available in numpy and opencv
import numpy as np
import cv2
import math
from decimal import Decimal

class Filtering:
    image = None

    # apply 3*3 mean filter
    def arithmetic_mean_filter(self, img, windowSize = 3):
        height, width = img.shape[:2]
        newimg = np.zeros(img.shape[:2], np.uint8)
        # mask = np.zeros((3, 3), np.uint8)
        for j in range(height):
            for i in range(width):
                if 0 < i < width - 1 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 0:3] = img[j - 1:j + 2, i - 1:i + 2]

                elif i == 0 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 1:3] = img[j - 1:j + 2, i:i + 2]
                    mask[0:3, 0] = img[j - 1:j + 2, i]
                elif i == width - 1 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 0:2] = img[j - 1:j + 2, i - 1:i + 2]
                    mask[0:3, 2] = img[j - 1:j + 2, i]

                elif 0 < i < width - 1 and j == 0:  # ok
                    mask = np.zeros((3, 3), np.uint8)
                    mask[1:3, :] = img[j:j + 2, i - 1:i + 2]
                    mask[0, :] = img[j, i - 1:i + 2]

                elif 0 < i < width - 1 and j == height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:2, 0:3] = img[j - 1:j + 2, i - 1:i + 2]
                    mask[2, 0:3] = img[j, i - 1:i + 2]
                else:
                    mask = np.full((3, 3), img[j][i])
                average = np.sum(mask) / 9
                newimg[j][i] = int(average)
        return newimg

    def geometric_mean_filter(self, img):
        height, width = img.shape[:2]
        newimg = np.zeros(img.shape[:2], np.uint8)
        # mask = np.zeros((3, 3), np.uint8)
        for j in range(height):
            for i in range(width):
                if 0 < i < width - 1 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 0:3] = img[j - 1:j + 2, i - 1:i + 2]

                elif i == 0 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 1:3] = img[j - 1:j + 2, i:i + 2]
                    mask[0:3, 0] = img[j - 1:j + 2, i]
                elif i == width - 1 and 0 < j < height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:3, 0:2] = img[j - 1:j + 2, i - 1:i + 2]
                    mask[0:3, 2] = img[j - 1:j + 2, i]

                elif 0 < i < width - 1 and j == 0:  # ok
                    mask = np.zeros((3, 3), np.uint8)
                    mask[1:3, :] = img[j:j + 2, i - 1:i + 2]
                    mask[0, :] = img[j, i - 1:i + 2]

                elif 0 < i < width - 1 and j == height - 1:
                    mask = np.zeros((3, 3), np.uint8)
                    mask[0:2, 0:3] = img[j - 1:j + 2, i - 1:i + 2]
                    mask[2, 0:3] = img[j, i - 1:i + 2]
                else:
                    mask = np.full((3, 3), img[j][i])
                multiple = Decimal(1)
                for l in range(3):
                    for m in range(3):
                        multiple *= mask[l][m]
                newimg[j][i] = int(math.pow(multiple, 1 / 9))
        return newimg