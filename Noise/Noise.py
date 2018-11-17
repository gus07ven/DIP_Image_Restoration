import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import random
import math
def noisy(noise_typ,image):
   if noise_typ == "Gaussian":
      row,col= image.shape
      mean = 0
      var = 10
      sigma = var**0.5
      gauss = np.random.normal(mean,var,(row,col))
      print(gauss.shape)
      gauss = gauss.reshape(row,col)
      noisy = image + gauss
      #plt.hist(noisy, bins='auto')
      #plt.show()
      noisy = np.array(noisy,dtype=np.uint8)
      #plt.hist(noisy, bins='auto')
      #plt.show()

      return noisy
   elif noise_typ == "salt&pepper":
      prob = 0.2
      thres = 1 - prob
      for i in range(0,image.shape[0]):
          for j in range(0,image.shape[1]):
              rdn = random.random()
              if rdn < prob:
                  image[i][j] = 0
              elif rdn > thres:
                  image[i][j] = 255
              else:
                  image[i][j] = image[i][j]
      plt.hist(image, bins='auto')
      plt.show()
      return image
   elif noise_typ == "poisson":
      vals = len(np.unique(image))
      vals = 2 ** np.ceil(np.log2(vals))
      noisy = np.random.poisson(image * vals) / float(vals)
      noisy = np.array(noisy, dtype=np.uint8)
      #plt.hist(noisy, bins='auto')
      #plt.show()
      return noisy
   elif noise_typ =="speckle":
      row,col = image.shape
      mean = 0
      var = 0.1
      gauss = np.random.normal(mean,math.sqrt(var),(row,col))
      noisy = image + image * gauss
      noisy = np.array(noisy, dtype=np.uint8)
      #plt.hist(noisy,bins='auto')
      #plt.show()
      return noisy
   elif noise_typ == "rayleigh":
       row, col = image.shape
       mean = 0
       var = 0.1
       sigma = var ** 0.5
       gauss = np.random.rayleigh(scale=10, size=(row, col))
       print(gauss.shape)
       plt.hist(gauss, bins='auto')
       plt.show()
       gauss = gauss.reshape(row, col)
       noisy = image + gauss
       noisy = np.array(noisy, dtype=np.uint8)


if  __name__ == "__main__":
    print("type of noise:")
    print("\t 1. Gaussian \n\t 2. salt&pepper \n\t 3.Poisson \n\t 4.speckle")
    type = input("enter your choice \n")
    img = cv2.imread("C:\\Users\\ani49\\OneDrive\\Documents\\GitHub\\homework-3-ani4991\\Lenna.png",0)
    #plt.hist(img, bins='auto')
    #plt.show()
    noisy_img = noisy(type,img)
    cv2.imshow('noisy_image',noisy_img)
    cv2.imwrite(type + "_noise_img.jpg",noisy_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
