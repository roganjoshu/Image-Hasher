from time import time
import tkinter as tk
import tkinter.messagebox
import PIL
from PIL import ImageTk
import os
import sys

class Root:

    def __init__(self, root, hasher):   #initialises GUI by drawing labels and storing reference to hasher and master window

        self.root = root
        self.hasher = hasher
        self.init_labels()      

    def init_labels(self):  #draws GUI elements
        #user input and file path frame
        fr_scan = tk.LabelFrame(self.root, text="Enter path to the folder you wish to scan")
        fr_scan.grid( row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_path = tk.Label(fr_scan, text="Path to folder", height=10)
        self.lbl_path.grid(row=0,column=0, padx=5)

        self.entr_path = tk.Entry(fr_scan, width=99)
        self.entr_path.grid(row=0, column=1)

        self.btn_scan = tk.Button(fr_scan, text="Scan!", command= lambda: self.scan_directory(self.entr_path.get(), self.hasher))
        self.btn_scan.grid(row=0, column=2, padx=5, pady=5)

        #file path results frame
        fr_results = tk.LabelFrame(self.root, text="Possible duplicate images")
        fr_results.grid(columnspan=1, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_scrllbr = tk.Scrollbar(fr_results)
        self.lstbx_scrllbr.grid(row=1, column=0, padx=5, pady=5)

        self.lstbx_results = tk.Listbox(fr_results, width=120, height=19)
        self.lstbx_results.config(yscrollcommand=self.lstbx_scrllbr.set)
        self.lstbx_results.bind("<<ListboxSelect>>", lambda x: self.update_label(self.hasher))
        self.lstbx_scrllbr.config(command=self.lstbx_results.yview)
        self.lstbx_results.grid(columnspan=2, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_instructions = tk.Label(fr_results, text="Here you can see groups of duplicate images, select the item you wish to manage and it will appear in the 'Selected item' tab on the right.")
        self.lbl_instructions.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        #selected file frame
        fr_selected_file = tk.LabelFrame(self.root, text="Selected item")
        fr_selected_file.grid(rowspan=3, row=0, column=1, padx=5, pady=5, sticky="ne")

        self.lbl_img_name = tk.Label(fr_selected_file, text="File name: ")
        self.lbl_img_name.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        self.lbl_img_location = tk.Label(fr_selected_file, text="File location: ")
        self.lbl_img_location.grid(row=1, column=0, padx=5, pady=10, sticky="w")

        self.lbl_img_creation_date = tk.Label(fr_selected_file, text="Creation date: ")
        self.lbl_img_creation_date.grid(row=2, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_shape = tk.Label(fr_selected_file, text="Resolution: ")
        self.lbl_img_shape.grid(row=3, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_chnls = tk.Label(fr_selected_file, text="Colour channels: ")
        self.lbl_img_chnls.grid(row=4, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_thumb = tk.Label(fr_selected_file, text="Image: ")
        self.lbl_thumb.grid(row=5, column=0, padx=5, pady=10, sticky="nw")

        self.img_thumb = tk.Label(fr_selected_file)
        self.img_thumb.grid(row=6, column=0, padx=5, pady=10, sticky="nw")

    def scan_directory(self, path_to_file, hasher):   #begins scanning process of images, called by scan button
        self.lstbx_results.delete(0, tk.END)    #clear listbox and images list for next 
        hasher.images.clear()
        duplicate_count = 0
        time1 = time()

        if len(path_to_file) == 0:
            tkinter.messagebox.showinfo("No path", "Please enter a path!")

        else:

            try:  
                path_contents = os.listdir(path_to_file)

                if len(path_contents) == 0:       
                    print("Directory empty")

                else:
                    hasher.read_images(path_contents, path_to_file)

                    if hasher.get_images_length() == 0:
                        tkinter.messagebox.showinfo("Error", "No images found, please check the directory for images and then try again.")

                    elif hasher.get_images_length() > 0:
                        hasher.images.sort(key=lambda x: x.get_hash(), reverse=False)
                        for index, image in enumerate(hasher.get_images()):
                            duplicate_count += hasher.get_duplicate_range(hasher.images, image)

                        time2 = time()
                        print("Program duration: " + str(time2-time1))
                        print("Items: " + str(hasher.get_images_length()))
                        print("Duplicates: " + str(duplicate_count))
                
                self.update_lstbx(hasher)

            except Exception as e:
                tkinter.messagebox.showinfo("Invalid path", e)#path_to_file + " is invalid, please try again.")
    
    def update_lstbx(self, hasher): #updates contents of listbox to show duplicates found.
        group = 0
        for index, img, in enumerate(hasher.get_images()):
            if len(img.get_group()) > 0:
                group += 1
                self.lstbx_results.insert(tk.END, "Group " + str(group))
                self.lstbx_results.insert(tk.END, img.get_name())
                for duplicate in img.get_group():
                    self.lstbx_results.insert(tk.END, duplicate.get_name())

    def update_label(self, hasher): #updates labels in selected file frame with image data
        text = self.lstbx_results.curselection()[0]
        img_name = self.lstbx_results.get(text)

        for index, image in enumerate(hasher.get_images()):
            if image.get_name() == img_name:
                thumbnail = PIL.Image.open(image.get_path())
                resized = thumbnail.resize((192,128))
                ph_img = ImageTk.PhotoImage(resized)
                self.lbl_img_name['text'] = "File name: " + image.get_name()
                self.lbl_img_location['text'] = "File path: " + image.get_location()
                if image.get_date() == 0:
                    self.lbl_img_creation_date['text'] = "Creation date: Unavailable"
                else:
                    self.lbl_img_creation_date['text'] = "Creation date: " + str(image.get_date())
                self.lbl_img_shape['text'] = "Resolution: " + str(image.get_image_shape())
                self.lbl_img_chnls['text'] = "Colour channels: " + str(image.get_image_channels())      
                self.img_thumb.config(image=ph_img)
                self.img_thumb.img = ph_img