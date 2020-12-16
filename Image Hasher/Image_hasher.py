from cv2 import cv2 as cv
import numpy as np
import os
import sys
from time import time
from Image import Image
from PIL import Image as image
import vptree

substring = ".ini"
path_to_file = "D:\S20 Pics"
images = list()

#read images in from path, convert to mat obejct and store in custom type Image
def read_images(path_contents, path_to_file):
    print("Reading images...")
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
    print("Hashing images")
    for index, image in enumerate(images):
        hashsize = 8
        image_hash = 0

        grayscale = cv.cvtColor(image.get_image(), cv.COLOR_BGR2GRAY)
        #2D array of ints representing pixel intensity  
        image_resized = cv.resize(grayscale, (hashsize + 1, hashsize))
        #instantiate 2d matrix 8x8
        m, n = image_resized.shape
        pixel_difference = np.ndarray(shape=(m, n-1), dtype=bool)

        for row in range(m):
                for col in range(n-1):
                    #if right pixel more intense than left then index = TRUE
                    if image_resized[row, col+1] > image_resized[row, col]:
                        pixel_difference[row,col] = True
                    else:
                        pixel_difference[row,col] = False
        
        #flatten pixel difference to 1D array, if index is TRUE append image hash with 5^value of the index
        for index, value in enumerate(pixel_difference.flatten()):
                if value == True:
                    image_hash += 5**index

        image.set_hash(image_hash)

#if hashes & channels/size the same then a duplicate has been found
#O(n) linear time complexity, very slow
def identify_duplicate_hashes(images):
    print("Idenitfying duplicates")
    for index, image in enumerate(images):
        for new_index, new_image in enumerate(images):
            if new_index <= index:
                continue
            elif new_image.get_hash() == image.get_hash() and new_image.get_image_shape() == image.get_image_shape():
                print(new_image.get_name())
                print(image.get_name())


def sort_images(images):
    images.sort(key=lambda x: x.get_hash(), reverse=True)
    count = 0
    
    #just a check to see if images are sorted
    for index, image in enumerate(images):
        if index == len(images) - 1:
            break
        elif image.get_hash() >= images[index + 1].get_hash():
            count += 1
            print(">= is true")

    print(str(count))
    print()

#this needss checking
def recursive_binary_search(images, low, high, hash_to_check):
    if low > high:
        return False
    mid = int(low + (high - low) / 2)

    if hash_to_check == images[mid].get_hash():
        return True
    elif hash_to_check < images[mid].get_hash():
        return recursive_binary_search(images, low, mid - 1, hash_to_check)
    else:
        return recursive_binary_search(images, mid + 1, high, hash_to_check)

#call functions, read images, hash images, identify duplicate hashes/images
time1 = time()

path_contents = os.listdir(path_to_file)
read_images(path_contents, path_to_file)
hash_image(images)
#identify_duplicate_hashes(images)
sort_images(images)

for index, image in enumerate(images):
    if recursive_binary_search(images, 0, len(images)-1, image.get_hash()):
        print("duplicate found")

time2 = time()
time_taken = time2 - time1

print(str(time_taken))