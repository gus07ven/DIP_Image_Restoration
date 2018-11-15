import numpy as np
import math
from decimal import Decimal


class Filtering:
    image = None

    def __init__(self, image = None):
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
                maskNum = 0
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]
                multipleValue = Decimal(1)
                for l in range(windowSize):
                    for m in range(windowSize):
                        if mask[l][m] != 0:
                            multipleValue *= mask[l][m]
                            maskNum += 1
                newImg[j][i] = int(math.pow(multipleValue, 1/maskNum)+0.5)
        return newImg

    def harmonic_mean_filter(self, img, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize / 2)

        paddingImg = self.padding_img(img, windowSize)
        newImg = np.zeros(img.shape[:2], np.uint8)

        # mask = np.zeros((3, 3), np.uint8)
        for j in range(height):
            for i in range(width):
                mask = np.zeros((windowSize, windowSize), np.uint8)
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]
                denominator = 0.0
                for l in range(windowSize):
                    for m in range(windowSize):
                        if mask[l][m] != 0:
                            denominator += 1/(mask[l][m])
                newImg[j][i] = int((windowSize ** 2)/denominator +0.5)
        return newImg

    def contraharmonic_mean_filter(self, img, Qpara, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize / 2)

        paddingImg = self.padding_img(img, windowSize)
        newImg = np.zeros(img.shape[:2], np.uint8)

        # mask = np.zeros((3, 3), np.uint8)
        for j in range(height):
            for i in range(width):
                mask = np.zeros((windowSize, windowSize), np.uint8)
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]
                valueNom = 0.0
                valueDen = 0.0
                for l in range(windowSize):
                    for m in range(windowSize):
                        if mask[l][m] != 0:
                            if Qpara+1 >= 0:
                                valueNom += math.pow(mask[l][m], Qpara + 1)
                            else:
                                valueNom += 1/math.pow(mask[l][m], -(Qpara+1))
                            if Qpara >= 0:
                                valueDen += math.pow(mask[l][m], Qpara)
                            else:
                                valueDen += 1/math.pow(mask[l][m], -Qpara)
                newImg[j][i] = int(valueNom/valueDen + 0.5)
        return newImg

    def median_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_img = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0:window_size, 0:window_size] = padding_img[j:j + window_size, i:i + window_size]
                new_img[j][i] = np.ma.median(np.squeeze(np.asarray(mask)))    # we can implement getMedian if necessary
        return new_img

    def max_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_img = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0:window_size, 0:window_size] = padding_img[j:j + window_size, i:i + window_size]
                new_img[j][i] = mask.max()  # we can implement getMax if necessary
        return new_img

    def min_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_img = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0:window_size, 0:window_size] = padding_img[j:j + window_size, i:i + window_size]
                new_img[j][i] = mask.min()  # we can implement getMin if necessary
        return new_img

    def midpoint_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_img = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0:window_size, 0:window_size] = padding_img[j:j + window_size, i:i + window_size]
                midpoint = (mask.max() + mask.min()) / 2  # Getting rid of the decimal part. Should we add + .5?
                new_img[j][i] = midpoint
        return new_img

    def alpha_trimmed_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_img = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)
        d = 2  # Should we make this a user determined parameter? If so, we have to be careful

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0:window_size, 0:window_size] = padding_img[j:j + window_size, i:i + window_size]
                mask_to_ordered_array = np.sort(np.asarray(mask).flatten())
                new_mask = mask_to_ordered_array[int(d/2): mask_to_ordered_array.size - (int(d/2))]
                alpha_trimmed_mean = int(np.ma.mean(np.squeeze(new_mask)))  # Should we cast to int when np takes care of it?
                new_img[j][i] = alpha_trimmed_mean
        return new_img

    def adaptive_local_noise_reduction_filter(self, img, theta_square_n, windowSize = 3):
        height, width = img.shape[:2]
        margin = int(windowSize / 2)

        paddingImg = self.padding_img(img, windowSize)
        newImg = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((windowSize, windowSize), np.uint8)
                mask[0:windowSize, 0:windowSize] = paddingImg[j:j + windowSize, i:i + windowSize]

                localMean = np.sum(mask) / (windowSize**2)
                varianceMask = mask - localMean
                varianceSquare = varianceMask * varianceMask
                localVariance = np.sum(varianceSquare) / (windowSize**2)
                if theta_square_n == 0:
                    newImg = img
                    return newImg
                elif theta_square_n > localVariance:
                    newImg[j][i] = localMean
                else:
                    newImg[j][i] = img[j][i] - theta_square_n/localVariance*(img[j][i] - localMean)
        return newImg

    def adaptive_median_filter(self, img, window_size=3):
        height, width = img.shape[:2]
        padding_image = self.padding_img(img, window_size)
        new_img = np.zeros(img.shape[:2], np.uint8)

        for j in range(height):
            for i in range(width):
                mask = np.zeros((window_size, window_size), np.uint8)
                mask[0: window_size, 0: window_size] = padding_image[j: j + window_size, i: i + window_size]
                z_min = mask.min()
                z_max = mask.max()
                z_med = int(np.ma.median(np.squeeze(np.asarray(mask))))
                z_xy = np.asarray(img)[j][i]
                s_max = 7

                test = self.level_a(j, i, z_med, z_min, z_max, z_xy, window_size, s_max)
                new_img[j][i] = test
        return new_img

    def level_a(self, j, i, z_med, z_min, z_max, z_xy, window_size, s_max):
        a_1 = z_med - z_min
        a_2 = z_med - z_max
        if a_2 < 0 < a_1:
            return self.level_b(z_med, z_min, z_max, z_xy)
        else:
            window_size += 2
            if window_size <= s_max:
                return self.level_a(j, i, z_med, z_min, z_max, z_xy, window_size, s_max)
            else:
                return z_xy

    def level_b(self, z_med, z_min, z_max, z_xy):
        b_1 = z_xy - z_min
        b_2 = z_xy - z_max
        if b_2 < 0 < b_1:
            return z_xy
        else:
            return z_med




