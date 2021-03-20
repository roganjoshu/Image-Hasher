from PIL.ExifTags import TAGS
from cv2 import cv2 as cv
from PIL import Image as image
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
        self.file_types = [".jpg", ".png", ".jpeg", ".bmp", ".jp2", ".jpe", ".dib", ".tiff"]
        self.check_similar = False
    #getters
    def get_images_length(self):    #return length of images list
        return len(self.images)

    def get_dpl_images_length(self):
        return len(self.dpl_images) 

    def get_dpl_images(self):   #return strings of duplicate images
        return self.dpl_images
    
    def get_images(self):   #returns list of image objects
        return self.images



    def read_images(self, file_name, r):   #extract data from images using CBIR   
        path_to_file = r + "\\" + file_name
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

                creation_date = time.ctime(os.path.getctime(path_to_file))  #gets time item came into existence on machine
                modified_date = time.ctime(os.path.getmtime(path_to_file))  #gets time item was last modified
                image_shape = temp_image.shape  #gets resolution/dimensions of item
                image_size = round((os.path.getsize(path_to_file) / 1024), 1)   #gets size of file

                image_object = Image(file_name, creation_date, date_taken, image_shape, colour_channels, path_to_file, path_to_file, modified_date, image_size)   #instantiate new custom Image object
                image_object.set_hash(hasher.hash_image(temp_image, image_object, self.check_similar))  #dHash image and store in image object

                if image_object.get_hash() != 0:  #if the image has a suitable hash
                    hasher.images.append(image_object)    #append the image to the list of images
                    return True
            else:   #return false if the item was unreadable
                return False
    
    def scan_drive(self, location, drives): #when drive scan is requested this method is called
        for r, d, f in os.walk(drives[location] + "\\"):
            folder = r.split("\\", 2)[1].lower()
            if any(exception in folder for exception in self.exceptions):   #check to see if the string contains an exception
                self.items_scanned += 1
            else:
                for file in f:
                    for filetype in self.file_types:
                        if file.endswith(filetype):  # no exception then check file extension
                            self.items_scanned += 1 #increment counter and read if file extension is found
                            filepath = os.path.join(r, file)

                            if self.read_images(file, r):
                                print(filepath + " has been read successfully")
                                self.images_scanned += 1

    def scan_path(self, location):  #when file path is specified the method is called
        for r, d, f in os.walk(location):   #recursively walk through every dir available
            folder = r.split("\\", 2)[1].lower()    #split the string to get the drive
            if any(exception in folder for exception in self.exceptions):   #if any of the exceptions exist in folder string do nothing but increment counter
                self.items_scanned += 1
            else:
                for file in f:  #if exception not in string then check to see if file is of the same type as any of the extensions in file_types
                    for filetype in self.file_types:
                        if file.endswith(filetype):
                            self.items_scanned += 1 #increment counter and read file if the filetype is acceptable i.e. exists in the file_Types list
                            filepath = os.path.join(r, file)

                            if self.read_images(file, r):
                                print(filepath + " has been read successfully")
                                self.images_scanned += 1


    def hamming_distance(self, first_bin_val, second_bin_val):  #calculates the hamming distance between two image binary strings
        return sum(char1 != char2 for char1, char2 in zip(first_bin_val, second_bin_val))

    def hash_image(self, temp_image, img_object, similar):    #hash image using dHash. Grayscale, compare, assign
        if similar: #if the user has requested a to look for similar photos
            hashsize = 8
        else:
            hashsize = 32
        image_hash = 0
        binary_value = ""

        image_resized = cv.resize(temp_image, (hashsize + 1, hashsize)) #Image is already grayscaled, resize to 33x32
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
                image_hash += 2** index  #if true add 2^index to image_hash
                binary_value += "1"
            else:
                binary_value += "0"

        img_object.set_binary_value(binary_value)
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

    def get_duplicates(self, images, image, index):     #generates range of duplicate hash values to loop through
        first_index = self.binary_search(hasher.images, len(hasher.images), image, True)   #get first occurence
        last_index = self.binary_search(hasher.images, len(hasher.images), image, False)   #get last occurence
        duplicates = list()

        if (last_index - first_index) + 1 > 1:  #if multiple duplicates
            for x in range(first_index, last_index + 1):
                if image.get_image_shape() == hasher.images[x].get_image_shape():
                    if image.get_image_channels() == hasher.images[x].get_image_channels():
                        duplicates.append(hasher.images[x])

            duplicates.sort(key=lambda x: os.path.getctime(x.get_path()))   #sort items based on creation date on system
            
            for indexs, image in enumerate(duplicates):
                if indexs == 0: #check to see if checking first image, which will be original, if so set duplicate tag true and move on to nect index
                    image.set_is_duplicate(True)
                else:   #if we're not checking first index then do this
                    duplicates[0].append_group(image)
                    image.set_is_duplicate(True)
                    hasher.dpl_images.append(image)
            hasher.dpl_images.append(duplicates[0])    #assign duplicates[0] which will always be the original to the dpl_images list of hasher

    def del_group(self):    #deletes the group of duplicates attached to an image
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