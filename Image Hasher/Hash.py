from cv2 import cv2 as cv
from PIL import Image as image
from PIL.ExifTags import TAGS
from Image import Image
from Root import Root
import numpy as np
import tkinter as tk
import os
import sys
import tkinter.messagebox
import time



class Hash:
    
    #Constructor
    def __init__(self): #initialises hasher with a list of images and a list of duplicates
        self.images = list()
        self.dpl_images = list()
    #getters
    def get_images_length(self):    #return length of images list
        return len(self.images)

    def get_dpl_images_length(self):
        return len(self.dpl_images) 

    def get_dpl_images(self):   #return strings of duplicate images
        return self.dpl_images
    
    def get_images(self):   #returns list of image objects
        return self.images


#member functions - read, hash, identify duplicates
    def read_images(self, path_contents, path_to_file):   #extract data from images using CBIR

        print("Calculating image data...")

        for file_name in path_contents:
            image_path = path_to_file + "\\" + file_name
            if os.path.isfile(image_path):  #if path to image exists do this
                temp_image = cv.imread(image_path, 0)

                if temp_image is not None:  #if succesfully read an image
                    creation_date = time.ctime(os.path.getctime(image_path))
                    try:
                        taken_date = image.open(image_path).getexif()[36867]
                    except:
                        taken_date = "Unavailable"
                    m_time = time.ctime(os.path.getmtime(image_path))
                    image_shape = temp_image.shape
                    colour_channels = image.open(image_path).mode
                    img_size = round((os.path.getsize(image_path) / 1024), 1)

                    img_object = Image(file_name, creation_date,taken_date, image_shape, colour_channels, image_path, path_to_file, m_time, img_size)   #instantiate new image object
                    img_object.set_hash(hasher.hash_image(temp_image))  #dHash image and store in image object
                    hasher.images.append(img_object)

    def hash_image(self, temp_image):    #hash image using dHash. Grayscale, compare, assign 
        hashsize = 8
        image_hash = 0

        image_resized = cv.resize(temp_image, (hashsize + 1, hashsize)) #Image is already grayscaled, resize to 9x8
        r, c = image_resized.shape
        pixel_difference = np.ndarray(shape=(r, c-1), dtype=bool) #initialize array same size as image resized

        for row in range(r):
            for col in range(c-1):
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

    def get_duplicate_range(self, images, image):     #generates range of duplicate hash values to loop through6
        first_index = hasher.binary_search(hasher.images, len(hasher.images), image, True)   #get first occurence
        last_index = hasher.binary_search(hasher.images, len(hasher.images), image, False)   #get last occurence

        if (last_index - first_index) + 1 > 1:  #if multiple duplicates

            for x in range(first_index, last_index + 1):

                if image.get_name() == hasher.images[x].get_name() or hasher.images[x].is_duplicate == True:  #if looking at same image go to next iteration
                    continue

                elif image.get_image_shape() == hasher.images[x].get_image_shape() and image.get_image_channels() == hasher.images[x].get_image_channels():    #if not looking at same image and shape and channels are the same
                    if x == 0:
                        hasher.dpl_images.append(image)

                    hasher.dpl_images.append(images[x])
                    image.append_group(images[x])
                    hasher.images[x].set_is_duplicate(True)
                    image.set_is_duplicate(True)


#main window
deduplicator = tk.Tk()
deduplicator.title("UOH: Image de-duplicator")
deduplicator.iconbitmap('idd icon.ico')
deduplicator.geometry("1200x650")
#instantiate hash

hasher = Hash()
if __name__ == "__main__":
    root = Root(deduplicator, hasher)
    deduplicator.mainloop()