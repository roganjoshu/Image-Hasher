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
import py2exe

class Hash:
    
    #Constructor
    def __init__(self): #initialises hasher with a list of images and a list of duplicates
        self.images = list()
        self.dpl_images = list()
        self.items_scanned = 0
        self.images_scanned = 0
        self.items_excluded = 0
        self.exceptions = ["windows", "program files", "recycle.bin", "programdata"]
    #getters
    def get_images_length(self):    #return length of images list
        return len(self.images)

    def get_dpl_images_length(self):
        return len(self.dpl_images) 

    def get_dpl_images(self):   #return strings of duplicate images
        return self.dpl_images
    
    def get_images(self):   #returns list of image objects
        return self.images


    def read_images(self, file_name, location):   #extract data from images using CBIR
        
        print("Calculating image data...")
        path_to_file = location + "\\" + file_name
        if os.path.isfile(path_to_file):  #if path to image exists do this
            temp_image = cv.imread(path_to_file, 0)
            if temp_image is not None:  #if succesfully read an image
                try:
                    exif = image.open(path_to_file).getexif()
                    date_taken = exif.get(36867)
                except:
                    date_taken = None            
                try:
                    colour_channels = image.open(path_to_file).mode
                except:
                    colour_channels = None

                creation_date = time.ctime(os.path.getctime(path_to_file))
                modified_date = time.ctime(os.path.getmtime(path_to_file))
                image_shape = temp_image.shape
                image_size = round((os.path.getsize(path_to_file) / 1024), 1)

                img_object = Image(file_name, creation_date, date_taken, image_shape, colour_channels, path_to_file, path_to_file, modified_date, image_size)   #instantiate new image object
                img_object.set_hash(hasher.hash_image(temp_image, img_object))
                hasher.images.append(img_object)
                return True
            else:
                return False
    
    def scan_drive(self, location, drives): #when drive scan is requested this method is called
        for r, d, f in os.walk(drives[location] + "\\"):
            folder = r.split("\\", 2)[1].lower()
            if any(exception in folder for exception in self.exceptions):
                self.items_excluded += 1
            else:
                for file in f:
                    filepath = os.path.join(r, file)
                    if self.read_images(file, r):
                        print(filepath + " has been read")
                        self.items_scanned += 1
                        self.images_scanned += 1
                    else:
                        print(filepath + " has not been read!")
                        self.items_scanned += 1
                     
    def scan_path(self, location):  #when file path is specified
        for r, d, f in os.walk(location):
                folder = r.split("\\", 2)[1].lower()
                if any(exception in folder for exception in self.exceptions):
                    self.items_excluded += 1
                else:
                    for file in f:
                        filepath = os.path.join(r, file)
                        if "." not in filepath:
                            continue
                        if self.read_images(file, r):
                            print(filepath + " has been read")
                            self.items_scanned += 1
                            self.images_scanned += 1
                        else:
                            print(filepath + " has not been read!")
                            self.items_scanned += 1

    def hash_image(self, temp_image, img_object):    #hash image using dHash. Grayscale, compare, assign 
        hashsize = 32
        image_hash = 0
        ham_value = ""

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
                image_hash += 2** index  #if true add 5^index to image_hash
                ham_value += "1"
            else:
                ham_value += "0"

        img_object.set_ham_distance(ham_value)
        return image_hash

    def hamming_distance(self, first_image, second_image):
        return sum(c1 != c2 for c1, c2 in zip(first_image.get_ham_value(), second_image.get_ham_value()))

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

    def get_duplicate_range(self, images, image, index):     #generates range of duplicate hash values to loop through
        first_index = hasher.binary_search(hasher.images, len(hasher.images), image, True)   #get first occurence
        last_index = hasher.binary_search(hasher.images, len(hasher.images), image, False)   #get last occurence

        if (last_index - first_index) + 1 > 1:  #if multiple duplicates

            for x in range(first_index, last_index + 1):

                if images[index].get_path() == images[x].get_path():  #if looking at same image go to next iteration
                    images[index].set_is_duplicate(True)
                    hasher.dpl_images.append(images[index])
                    continue

                elif image.get_image_shape() == hasher.images[x].get_image_shape():
                    if image.get_image_channels() == hasher.images[x].get_image_channels():    #if not looking at same image and shape and channels are the same
                        if not images[index].get_is_duplicate():
                            hasher.dpl_images.append(image)

                        image.append_group(images[x])
                        hasher.images[x].set_is_duplicate(True)
                        image.set_is_duplicate(True)
                        hasher.dpl_images.append(images[x])
    
    def del_group(self):
        for img in hasher.get_images():
            if len(img.get_group()) > 0:
                img.get_group().clear()
                       

#main window
deduplicator = tk.Tk()
deduplicator.title("UOH: Image de-duplicator")
deduplicator.iconbitmap('idd icon.ico')
deduplicator.geometry("1200x680")
#instantiate hash

hasher = Hash()
if __name__ == "__main__":
    root = Root(deduplicator, hasher)
    deduplicator.mainloop()