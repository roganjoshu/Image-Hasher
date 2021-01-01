from cv2 import cv2 as cv
from PIL import Image as image
from Image import Image
from Root import Root
import numpy as np
import tkinter as tk
import os
import sys
import tkinter.messagebox


class Hash:
    
    #constructor, initilize lists
    def __init__(self):
        self.images = list() #sortable data storage
        self.dpl_images = list()

    #getters
    def get_images_length(self):    #return length of images list
        return len(self.images)

    def get_dpl_images(self):   #return strings of duplicate images
        return self.dpl_images
    
    def get_images(self):   #returns list of image objects
        return self.images


    def read_images(self, path_contents, path_to_file):   #extract data from images using CBIR

        print("Calculating image data...")

        for file_name in path_contents:
            image_path = path_to_file + "\\" + file_name
            temp_image = cv.imread(image_path, 0)

            if temp_image is not None:  #if succesfully read image

                try:    #try retrieve following info and append to list
                    creation_date = image.open(image_path).getexif()[36867]
                    image_shape = temp_image.shape
                    colour_channels = image.open(image_path).mode
                    img_object = Image(file_name, creation_date, image_shape, colour_channels)

                    img_object.set_hash(hasher.hash_image(temp_image))
                    hasher.images.append(img_object)

                except: #if no date, get following info and append to list
                    image_shape = temp_image.shape
                    colour_channels = image.open(image_path).mode
                    img_object = Image(file_name, 0, image_shape, colour_channels)

                    img_object.set_hash(hasher.hash_image(temp_image))
                    hasher.images.append(img_object)
            else:
                continue

    def hash_image(self, temp_image):    #hash image using dHash. Grayscale, normalize, compare, assign 
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

    def binary_search(self, images, size, image, search_first):   #binary search finds first occurence then checks for first and last occurence
        low = 0
        high = size - 1
        result = -1

        while low <= high:
            mid = int((low + high) / 2)

            if image.get_hash() == hasher.images[mid].get_hash():
                result = mid    #set mid to candidate index

                if search_first:               
                    high = mid - 1  #search indices left of mid

                else:
                    low = mid + 1   #search indicese right of mid

            elif image.get_hash() < hasher.images[mid].get_hash():
                high = mid - 1  #search lower bounds

            else:
                low = mid + 1   #search upper bounds

        return result

    def get_duplicate_range(self, images, image):     #generates range of duplicate hash values to loop through
        count = 0
        first_index = hasher.binary_search(hasher.images, len(hasher.images), image, True)   #get first occurence
        last_index = hasher.binary_search(hasher.images, len(hasher.images), image, False)   #get last occurence

        if (last_index - first_index) + 1 > 1:  #get range of duplicates

            for x in range(first_index, last_index + 1):

                if image.get_name() == hasher.images[x].get_name() or hasher.images[x].is_duplicate == True:  #if looking at same image go to next iteration
                    continue

                elif image.get_image_shape() == hasher.images[x].get_image_shape() and image.get_image_channels() == hasher.images[x].get_image_channels():    #if not looking at same image and shape and channels are the same
                    image.append_group(images[x])
                    hasher.images[x].set_is_duplicate(True)
                    image.set_is_duplicate(True)


                    print("Original= " + image.get_name() + "\n"" duplicate= " + hasher.images[x].get_name() + "\n\n")
                    count += 1
        return count


#main window
deduplicator = tk.Tk()
deduplicator.title("UOH: Image de-duplicator")
deduplicator.iconbitmap('idd icon.ico')
deduplicator.geometry("1200x650")
#instantiate hash 
hasher = Hash()
root = Root(deduplicator, hasher)

deduplicator.mainloop()