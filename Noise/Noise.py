import numpy as np
import os
import cv2
def noisy(noise_typ,image):
   if noise_typ == "Gaussian":
      row,col,ch= image.shape
      mean = 0
      var = 0.1
      sigma = var**0.5
      gauss = np.random.normal(mean,sigma,(row,col,ch))
      gauss = gauss.reshape(row,col,ch)
      noisy = image + gauss
      noisy = np.array(noisy,dtype=np.uint8)
      return noisy
   elif noise_typ == "salt&pepper":
      row,col,ch = image.shape
      s_vs_p = 0.5
      amount = 0.004
      out = np.copy(image)
      # Salt mode
      num_salt = np.ceil(amount * image.size * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
      out[coords] = 1

      # Pepper mode
      num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
      out[coords] = 0
      return out
   elif noise_typ == "poisson":
      vals = len(np.unique(image))
      vals = 2 ** np.ceil(np.log2(vals))
      noisy = np.random.poisson(image * vals) / float(vals)
      noisy = np.array(noisy, dtype=np.uint8)
      return noisy
   elif noise_typ =="speckle":
      row,col,ch = image.shape
      gauss = np.random.randn(row,col,ch)
      gauss = gauss.reshape(row,col,ch)
      noisy = image + image * gauss
      noisy = np.array(noisy, dtype=np.uint8)
      return noisy

if  __name__ == "__main__":
    print("type of noise:")
    print("\t 1. Gaussian \n\t 2. salt&pepper \n\t 3.Poisson \n\t 4.speckle")
    type = input("enter your choice \n")
    img = cv2.imread("C:\\Users\\ani49\\OneDrive\\Documents\\GitHub\\homework-3-ani4991\\Lenna.png")
    noisy_img = noisy(type,img)


    cv2.imshow('noisy_image',noisy_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
