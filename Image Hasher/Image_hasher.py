from cv2 import cv2 as cv
import numpy as np
import os
import sys
from time import time
from Image import Image
from PIL import Image as image
import vptree

#C:\\Users\\Josh\\Pictures\\duplicates - 5 = 4 duplicates checked against dpf
#C:\\Users\\Josh\\Pictures\\Saved Pictures - 15 items - 1 duplicate checked against dpf
#D:\\S20 Pics - 97 items - 3 duplicates checked against dpf
#D:\\Univeristy\\3rd Year\\Honours Stage Project\\archive\\chest_xray\\chest_xray\\test\\NORMAL - 234 items - 3 duplicates checked against dpf
#D:\\Univeristy\\3rd Year\\Honours Stage Project\\archive\\chest_xray\\train\\PNEUMONIA - 3875 items - 25 duplicates checked against dpf
substring = ".ini"
path_to_file = "D:\\Univeristy\\3rd Year\\Honours Stage Project\\archive\\chest_xray\\chest_xray\\test\\NORMAL"
images = list()

#read images in from path > create customt type > hash image > append to list
def read_images(path_contents, path_to_file):
    hashsize = 8
    image_hash = 0

    print("Calculating image data...")
    for file_name in path_contents:
        if substring in file_name:
            continue
        else:
            image_path = path_to_file + "\\" + file_name
            temp_image = cv.imread(image_path, 0)
            try:
                #get metadata date
                date = image.open(image_path).getexif()[36867]
                #get resolution & colour channels
                image_shape = temp_image.shape
                img_pil = image.open(image_path).mode
                #instantiate object > filename, date, imageshape
                img_object = Image(file_name, date, image_shape, channels)
                #set object hash value > call hash_image()
                img_object.set_hash(hash_image(img_object, temp_image))
                #append custom type to list
                images.append(img_object)
            except:
                #if cant get date, get resolution & colour channels
                image_shape = temp_image.shape
                img_pil = image.open(image_path).mode
                #create custom type and assign date 0
                img_object = Image(file_name, 0, image_shape, channels)
                #set object hash value > call hash_image()
                img_object.set_hash(hash_image(img_object, temp_image))
                #append custom type to list
                images.append(img_object)

#generate hash value from image: grayscale > resize > compute difference intensity > build hash r > l
#9x8 because 9 pixels compared against 8 adjacent pixels renders 8x8 64bit array
def hash_image(image, temp_image):

    hashsize = 8
    image_hash = 0

    #grayscale = cv.cvtColor(temp_image, cv.COLOR_BGR2GRAY)
    #2D array of ints representing pixel intensity  
    image_resized = cv.resize(temp_image, (hashsize + 1, hashsize))
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

    return image_hash

#this needss checking
def binary_search(images, size, image, search_first):
    low = 0
    high = size - 1
    result = -1
    while low <= high:
        mid = int((low + high) / 2)
        #find candidate
        if image.get_hash() == images[mid].get_hash():
            #set mid to candidate index
            result = mid
            if search_first:               
                high = mid - 1  #search left/ lower indices of candidate
            else:
                low = mid + 1   #search right/ higher indices of candidate
        elif image.get_hash() < images[mid].get_hash():
            high = mid - 1
        else:
            low = mid + 1
    return result

#call functions, read images, hash images, identify duplicate hashes/images
time1 = time()

path_contents = os.listdir(path_to_file)
read_images(path_contents, path_to_file)

images.sort(key=lambda x: x.get_hash(), reverse=False)

#check for number of times an image appears
count = 0
for index, image in enumerate(images):
    
    #get first and last occurence
    first_index = binary_search(images, len(images), image, True)
    last_index = binary_search(images, len(images), image, False)

    #get range of duplicates, if greater than 1 and image names do not match and duplicte flag is false then duplicates found.
    if (last_index - first_index) + 1 > 1:
        for x in range(first_index, last_index + 1):
            if image.get_name() == images[x].get_name() or images[x].is_duplicate == True:
                continue
            elif image.get_image_shape() == images[x].get_image_shape():
                image.append_group(images[x].get_name())
                images[x].set_is_duplicate(True)
                image.set_is_duplicate(True)
                print("Original= " + image.get_name() + "\n" " duplicate= " + images[x].get_name() + "\n\n")
                count += 1

print(str(count))
time2 = time()
time_taken = time2 - time1

print(str(time_taken))