import cv2
import sys
from Filtering.Filtering import Filtering
from datetime import datetime
import numpy as np


def display_image(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():
    """ The main funtion that parses input arguments, calls the approrpiate
     fitlering method and writes the output image"""

    #Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")

    args = parser.parse_args()

    #Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)
        rows, cols = input_image.shape

    """input_image = np.zeros((3, 3), np.uint8)
    num = 1
    for j in range(3):
        for i in range(3):
            input_image[j][i] = num
            num += 1"""
    Filter_obj = Filtering()



    #cv2.imshow("look", output)
    #cv2.waitKey()



    #Write output file
    output_dir = 'output/'


    output = Filter_obj.adaptive_local_noise_reduction_filter(input_image, 60000, 3)
    output_image_name = output_dir + image_name + "_" + datetime.now().strftime("%m%d-%H%M%S") + str(
        "_adaptive_filter") + ".jpg"
    cv2.imwrite(output_image_name, output)

    output = Filter_obj.geometric_mean_filter(input_image, 3)
    output_image_name = output_dir + image_name + "_" + datetime.now().strftime("%m%d-%H%M%S") + str(
        "_geometric_filter") + ".jpg"
    cv2.imwrite(output_image_name, output)

if __name__ == "__main__":
    main()

