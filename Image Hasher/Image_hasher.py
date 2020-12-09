from cv2 import cv2 as cv
import numpy as np
import os
import sys
from time import time
from Image import Image
from PIL import Image as image

substring = ".ini"
path_to_file = "D:\\S20 Pics"
images = list()
duplicates = list()

#read images in from path, convert to mat obejct and store in custom type Image
def read_images(path_contents, path_to_file):

    for file_name in path_contents:
        if substring in file_name:
            continue
        else:
            image_path = path_to_file + "\\" + file_name
            temp_image = cv.imread(image_path)
            try:
                date = image.open(image_path).getexif()[36867]
                image_shape = temp_image.shape
                img_object = Image(temp_image, file_name, date, image_shape)
                images.append(img_object)
            except:
                image_shape = temp_image.shape
                img_object = Image(temp_image, file_name, 0, image_shape)
                images.append(img_object)

#generate hash value from image: grayscale > resize > compute difference between pixels (intensity) > build hash if intensity value = true
#grayscale improves speed, only one channel being examined, resize allows us to identify similar images as we ignore aspect ratio. 
#9x8 because 9 pixels compared against 8 adjacent pixels renders 8x8 64bit array
def hash_image(images):

    hashsize = 8
    image_hash = 0
    for index, image in enumerate(images):
        grayscale = cv.cvtColor(image.get_image(), cv.COLOR_BGR2GRAY)
        image_Resized = cv.resize(grayscale, (hashsize + 1, hashsize))
        r, c = image_Resized.shape
        pixel_difference = np.ndarray(shape=(r,c-1), dtype=bool)

        for row in range(r):
            for col in range(c-1):
                if image_Resized[row,col+1] > image_Resized[row,col]:
                    pixel_difference[row,col] = True
                else:
                    pixel_difference[row,col] = False


        for index, value in enumerate(pixel_difference.flatten()):
            if value == True:
                image_hash += 5**index
        image.set_hash(image_hash)

#if hashes & channels/size the same then a duplicate has been found
def identify_duplicate_hashes(images):

    for index, image in enumerate(images):
        for new_index, new_image in enumerate(images):
            if new_index <= index:
                continue
            elif new_image.get_hash() == image.get_hash() and new_image.get_image_shape() == image.get_image_shape():
                print(new_image.get_name())

#call functions, read images, hash images, identify duplicate hashes/images
time1 = time()

path_contents = os.listdir(path_to_file)
read_images(path_contents, path_to_file)
hash_image(images)
identify_duplicate_hashes(images)

time2 = time()
time_taken = time2 - time1
print(str(time_taken))