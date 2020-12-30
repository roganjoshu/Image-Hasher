from cv2 import cv2 as cv
from PIL import Image as image
from time import time
from Image import Image
import numpy as np
import tkinter as tk
import os
import sys

def read_images(path_contents, path_to_file):   #extract data from images using CBIR
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

                img_object.set_hash(hash_image(temp_image))
                images.append(img_object)

            except: #if no date, get following info and append to list
                image_shape = temp_image.shape
                colour_channels = image.open(image_path).mode
                img_object = Image(file_name, 0, image_shape, colour_channels)

                img_object.set_hash(hash_image(temp_image))
                images.append(img_object)
        else:
            continue

def hash_image(temp_image):    #hash image using dHash. Grayscale, normalize, compare, assign 
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

def binary_search(images, size, image, search_first):   #binary search finds first occurence then checks for first and last occurence
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

def get_duplicate_range(images, image):     #generates range of duplicate hash values to loop through
    count = 0
    first_index = binary_search(images, len(images), image, True)   #get first occurence
    last_index = binary_search(images, len(images), image, False)   #get last occurence

    if (last_index - first_index) + 1 > 1:  #get range of duplicates

        for x in range(first_index, last_index + 1):

            if image.get_name() == images[x].get_name() or images[x].is_duplicate == True:  #if looking at same image go to next iteration
                continue

            elif image.get_image_shape() == images[x].get_image_shape() and image.get_image_channels() == images[x].get_image_channels():    #if not looking at same image and shape and channels are the same
                image.append_group(images[x].get_name())
                images[x].set_is_duplicate(True)
                image.set_is_duplicate(True)

                print("Original= " + image.get_name() + "\n"" duplicate= " + images[x].get_name() + "\n\n")
                count += 1

    return count

def scan(path_to_file):
    images.clear()
    duplicate_count = 0
    time1 = time()
    try:  
        path_contents = os.listdir(path_to_file)
    except:
        print("No valid file path")

    if os.path.exists(path_to_file) and os.path.isdir(path_to_file):

        if len(path_contents) == 0:
            print("Directory empty")

        else:
            read_images(path_contents, path_to_file)
            images.sort(key=lambda x: x.get_hash(), reverse=False)  #sort images list ascending order based on hash value

            for index, image in enumerate(images):  #check for number of times an image appears
                duplicate_count += get_duplicate_range(images, image)
            print(str(duplicate_count))   

            time2 = time()
            time_taken = time2 - time1

            print(len(images)) 
            print("Program execution taken " + str(time_taken))

images = list()

#main window
deduplicator = tk.Tk()
deduplicator.title("Image de-duplicator")
deduplicator.iconbitmap('idd icon.ico')
deduplicator.geometry("1200x650")


#user input and file path frame
fr_scan = tk.LabelFrame(deduplicator, text="Enter path to folder you wish to scan")
fr_scan.grid(columnspan=3, row=0, column=0, padx=5, pady=5, sticky="nw")

lbl_path = tk.Label(fr_scan, text="Path to folder", height=10)
lbl_path.grid(row=0,column=0, padx=5)

entr_path = tk.Entry(fr_scan, width=99)
entr_path.grid(row=0, column=1)

button_scan = tk.Button(fr_scan, text="Scan!", command= lambda: scan(entr_path.get()))
button_scan.grid(row=0, column=2, padx=5, pady=5)

#file path results frame
fr_results = tk.LabelFrame(deduplicator, text="Results")
fr_results.grid(columnspan=1, row=1, column=0, padx=5, pady=5, sticky="nw")

lstbx_results = tk.Listbox(fr_results, width=120, height=19)
lstbx_results.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

lbl_instructions = tk.Label(fr_results, text="Here you can see groups of duplicate images, select the item you wish to manage and it will appear in the 'Selected file' tab on the right.")
lbl_instructions.grid(row=2, column=0, padx=5, pady=5, sticky="n")

#selected file frame
fr_selected_file = tk.LabelFrame(deduplicator, text="*Selected file name*")
fr_selected_file.grid(rowspan=3,row=0, column=1, padx=5, pady=5, sticky="n")

img_label = tk.Label(fr_selected_file, text="*selected file*", width=60, height=40)
img_label.grid( row=1,column=1)


deduplicator.mainloop()