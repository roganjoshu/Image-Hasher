from cv2 import cv2 as cv
import numpy as np
import os
import sys
from time import time
from Image import Image
from PIL import Image as image

def read_images(path_contents, path_to_file):   #extract data from images using CBIR
    print("Calculating image data...")
    for file_name in path_contents:
        image_path = path_to_file + "\\" + file_name
        temp_image = cv.imread(image_path, 0)
        if temp_image is not None:  #if succesfully read image
            try:    #try retrieve following info and append to list
                date = image.open(image_path).getexif()[36867]
                image_shape = temp_image.shape
                channels = image.open(image_path).mode
                img_object = Image(file_name, date, image_shape, channels)
                img_object.set_hash(hash_image(temp_image))
                images.append(img_object)
            except: #if no date, get following info and append to list
                image_shape = temp_image.shape
                channels = image.open(image_path).mode
                img_object = Image(file_name, 0, image_shape, channels)
                img_object.set_hash(hash_image(temp_image))
                images.append(img_object)
        else:
            continue

def hash_image(temp_image): #difference hash image. Grayscale, Resize (normalize), compare, assign 
    hashsize = 8
    image_hash = 0

    image_resized = cv.resize(temp_image, (hashsize + 1, hashsize)) #Image is already grayscaled, resize to 9x8
    m, n = image_resized.shape
    pixel_difference = np.ndarray(shape=(m, n-1), dtype=bool) #initialize array same size as image resized

    for row in range(m):
            for col in range(n-1):
                if image_resized[row, col+1] > image_resized[row, col]:
                    pixel_difference[row,col] = True    #if right pixel > left pixel assign true
                else:
                    pixel_difference[row,col] = False   #else assign false
    
    for index, value in enumerate(pixel_difference.flatten()):
            if value == True:
                image_hash += 5**index  #if true add 5^index to image_hash

    return image_hash

def binary_search(images, size, image, search_first):  #binary search finds first occurence then checks for first and last occurence
    low = 0
    high = size - 1
    result = -1
    while low <= high:
        mid = int((low + high) / 2)
        if image.get_hash() == images[mid].get_hash():
            result = mid    #set mid to candidate index
            if search_first:               
                high = mid - 1  #search indices left of mid
            else:
                low = mid + 1   #search indicese right of mid
        elif image.get_hash() < images[mid].get_hash():
            high = mid - 1  #search lower bounds
        else:
            low = mid + 1   #search upper bounds
    return result

def get_duplicate_range(images, image): #generates range of duplicate hash values to loop through
    count = 0
    first_index = binary_search(images, len(images), image, True)   #get first occurence
    last_index = binary_search(images, len(images), image, False)   #get last occurence

    if (last_index - first_index) + 1 > 1:  #get range of duplicates
        for x in range(first_index, last_index + 1):
            if image.get_name() == images[x].get_name() or images[x].is_duplicate == True:  #if looking at same image go to next iteration
                continue
            elif image.get_image_shape() == images[x].get_image_shape():    #if not looking at same image and shape and channels are the same
                image.append_group(images[x].get_name())    #append image to original image duplicate list
                images[x].set_is_duplicate(True)    #set duplicate flags to true
                image.set_is_duplicate(True)
                print("Original= " + image.get_name() + "\n"" duplicate= " + images[x].get_name() + "\n\n")
                count += 1
    return count

path_to_file = "D:\\Univeristy\\3rd Year\\Honours Stage Project\\archive\\chest_xray\\chest_xray\\test\\NORMAL"
images = list()

time1 = time()
path_contents = os.listdir(path_to_file)
read_images(path_contents, path_to_file)

images.sort(key=lambda x: x.get_hash(), reverse=False)  #sort images list ascending order based on hash value

count = 0
for index, image in enumerate(images):  #check for number of times an image appears
    count += get_duplicate_range(images, image)
print(str(count))   

time2 = time()
time_taken = time2 - time1

print(len(images))
print("Program execution taken " + str(time_taken))

#steps:
#1. Retrieve image information
#2. Perform dHash on image
#3. Idenitify duplicate hashes using variation on binary search