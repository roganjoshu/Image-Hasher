import tkinter as tk
import tkinter.messagebox
from time import time
import os
import sys
import concurrent.futures

class Root:

    #constructor
    def __init__(self, root, hasher):

        self.hasher = hasher

        #user input and file path frame
        fr_scan = tk.LabelFrame(root, text="Enter path to the folder you wish to scan")
        fr_scan.grid(columnspan=3, row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_path = tk.Label(fr_scan, text="Path to folder", height=10)
        self.lbl_path.grid(row=0,column=0, padx=5)

        self.entr_path = tk.Entry(fr_scan, width=99)
        self.entr_path.grid(row=0, column=1)

        self.btn_scan = tk.Button(fr_scan, text="Scan!", command= lambda: self.scan(self.entr_path.get(), hasher))
        self.btn_scan.grid(row=0, column=2, padx=5, pady=5)

        #file path results frame
        fr_results = tk.LabelFrame(root, text="Possible duplicate images")
        fr_results.grid(columnspan=1, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_scrllbr = tk.Scrollbar(fr_results)
        self.lstbx_scrllbr.grid(row=1, column=0, padx=5, pady=5)

        self.lstbx_results = tk.Listbox(fr_results, width=120, height=19)
        self.lstbx_results.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.lstbx_results.config(yscrollcommand=self.lstbx_scrllbr.set)
        self.lstbx_scrllbr.config(command=self.lstbx_results.yview)

        self.lbl_instructions = tk.Label(fr_results, text="Here you can see groups of duplicate images, select the item you wish to manage and it will appear in the 'Selected file' tab on the right.")
        self.lbl_instructions.grid(row=2, column=0, padx=5, pady=5, sticky="n")

        #selected file frame
        fr_selected_file = tk.LabelFrame(root, text="*Selected file name*")
        fr_selected_file.grid(rowspan=3,row=0, column=1, padx=5, pady=5, sticky="n")

        self.lbl_img = tk.Label(fr_selected_file, text="*selected file*", width=60, height=40)
        self.lbl_img.grid( row=1,column=1)

    def scan(self, path_to_file, hasher):
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
                    hasher.images.sort(key=lambda x: x.get_hash(), reverse=False)

                    for index, image in enumerate(hasher.images):
                        duplicate_count += hasher.get_duplicate_range(hasher.images, image)

                time2 = time()
                print("Program duration: " + str(time2-time1))
                print("Items: " + str(hasher.get_images_length()))
                print("Duplicates: " + str(duplicate_count))

                if hasher.get_images_length() == 0:
                    tkinter.messagebox.showinfo("Error", "No images found, please check the directory for images and then try again.")
                self.update_lstbx(hasher)

            except:
                tkinter.messagebox.showinfo("Invalid path", path_to_file + " is invalid, please try again.")
    
    def update_lstbx(self, hasher):
        for index, img, in enumerate(hasher.get_images()):  #update list box
                    if len(img.get_group()) > 0:
                        self.lstbx_results.insert(index, img.get_name())
                        for duplicate in img.get_group():
                            self.lstbx_results.insert(index + 1, duplicate.get_name())