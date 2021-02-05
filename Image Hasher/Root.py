from time import time
import tkinter as tk
import tkinter.messagebox
import PIL
from PIL import ImageTk
import os
import sys
import win32api
import shutil

class Root:

    def __init__(self, root, hasher):   #initialises GUI by drawing labels and storing reference to hasher and master window
        self.drives = [x[:2] for x in win32api.GetLogicalDriveStrings().split('\x00')[:-1]]
        self.radio_btns = list()
        self.root = root
        self.root.grid_rowconfigure(0, weight=1)
        #self.root.grid_columnconfigure(0, weight=1)
        self.hasher = hasher
        self.init_labels()
        self.image_path_list = list()
           

    def init_labels(self):  #draws GUI elements
        #user input and file path frame
        self.fr_scan = tk.LabelFrame(self.root, text="Enter path to the folder you wish to scan")
        self.fr_scan.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_path = tk.Label(self.fr_scan, text="Path to folder:")
        self.lbl_path.grid(row=0,column=0, padx=5, pady=5)

        self.entr_path = tk.Entry(self.fr_scan, width=100)
        self.entr_path.grid(row=0, column=1, pady=5)

        self.btn_scan = tk.Button(self.fr_scan, text="Scan!", command= lambda: self.scan_directory(self.entr_path.get(), self.hasher))
        self.btn_scan.grid(row=0, column=2, padx=5, pady=5)

        self.checked = tk.IntVar()
        self.chkbx_full = tk.Checkbutton(self.fr_scan, variable=self.checked, text="Scan entire drive (Note: This is not recommended as it will scan system files and identify necessary files for system operation)", command=lambda:self.disable_entry())
        self.chkbx_full.grid(columnspan=2, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.drive_var = tk.IntVar()

        for index, drive in enumerate(self.drives):
            self.radbtn = tk.Radiobutton(self.fr_scan, text=drive, variable=self.drive_var, value=index, state='disabled')
            self.radbtn.grid(row=3+index, column=0, padx=5, pady=5, sticky="nw")
            self.radio_btns.append(self.radbtn)



        #file path results frame
        fr_results = tk.LabelFrame(self.root, text="Possible duplicate images")
        fr_results.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_scrllbr = tk.Scrollbar(fr_results)
        self.lstbx_scrllbr.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_results = tk.Listbox(fr_results, width=127, height=19)
        self.lstbx_results.config(yscrollcommand=self.lstbx_scrllbr.set)
        self.lstbx_results.bind("<<ListboxSelect>>", lambda x: self.update_label(self.hasher))
        self.lstbx_scrllbr.config(command=self.lstbx_results.yview)
        self.lstbx_results.grid(columnspan=2, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.btn_del_img = tk.Button(fr_results, text="Delete selection", command= self.del_selection)
        self.btn_del_img.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        self.btn_mov_items = tk.Button(fr_results, text = "Move items to new directory", command= self.move_items)
        self.btn_mov_items.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.lbl_instructions = tk.Label(fr_results, text="Here you can see groups of duplicate images,"
            " select the item you wish to manage and it will appear in the 'Selected item' tab on the right.\nPlease be aware, the images identified may not be exact duplicates, review each image before taking any action.")
        self.lbl_instructions.grid(row=4, column=0, padx=5, pady=5, sticky="nw")



        #selected file frame
        fr_selected_file = tk.LabelFrame(self.root, text="Selected item")
        fr_selected_file.grid(rowspan=3, row=0, column=1, padx=5, pady=5, sticky="nw")

        self.lbl_img_name = tk.Label(fr_selected_file, text="File name: ")
        self.lbl_img_name.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_location = tk.Label(fr_selected_file, text="File location: ")
        self.lbl_img_location.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_taken_date = tk.Label(fr_selected_file, text="Date taken: ")
        self.lbl_taken_date.grid(row=2, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_creation_date = tk.Label(fr_selected_file, text="Creation date: ")
        self.lbl_img_creation_date.grid(row=3, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_mod_time = tk.Label(fr_selected_file, text="Date modified: ")
        self.lbl_mod_time.grid(row=4, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_size = tk.Label(fr_selected_file, text="Size: ")
        self.lbl_size.grid(row=5, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_shape = tk.Label(fr_selected_file, text="Resolution: ")
        self.lbl_img_shape.grid(row=6, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_chnls = tk.Label(fr_selected_file, text="Colour channels: ")
        self.lbl_img_chnls.grid(row=7, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_thumb = tk.Label(fr_selected_file, text="Image: ")
        self.lbl_thumb.grid(row=8, column=0, padx=5, pady=10, sticky="nw")

        self.img_thumb = tk.Label(fr_selected_file, image=None)
        self.img_thumb.grid(row=9, column=0, padx=5, pady=10, sticky="nw")

    def disable_entry(self):
        if self.checked.get() == 1:
            self.entr_path.config(state='disabled')
            for btn in self.radio_btns:
                btn.config(state='normal')
        else:
            self.entr_path.config(state='normal')
            for btn in self.radio_btns:
                btn.config(state = 'disabled')
        
    def scan_directory(self, path_to_file, hasher):   #begins scanning process of images, called by scan button
        self.lstbx_results.delete(0, tk.END)    #clear listbox and images list for next 
        hasher.images.clear()

        if self.checked.get() == 1: #end-user request for whole drive search
            self.hasher.scan_drive(self.drive_var.get(), self.drives)
            
        elif self.checked.get() == 0:   #end user request folder search
            if len(path_to_file) == 0:
                tkinter.messagebox.showinfo("No path", "Please enter a path!")
            else:
                path_contents = os.listdir(path_to_file)
                if len(path_contents) == 0: #path contents empty
                    print("Directory empty.")
                else:
                    for file_name in path_contents:
                        image_path = path_to_file + "\\" + file_name
                        self.image_path_list.append(image_path)
                        self.hasher.read_images(file_name, path_to_file)

        try:     
            if self.hasher.get_images_length() == 0: #no images in path
                tkinter.messagebox.showinfo("Error", "No images found, please check the directory for images and then try again.")
                    
            elif self.hasher.get_images_length() > 1:    #multiple images, may be duplicates
                self.hasher.images.sort(key=lambda x: x.get_hash(), reverse=False)
                for index, image in enumerate(self.hasher.get_images()):
                    if not image.get_is_duplicate():
                        self.hasher.get_duplicate_range(self.hasher.images, image, index)
                        
            elif len(self.hasher.get_dpl_images()) < 1:  #no duplicates were found in the directory
                tk.messagebox.showinfo("No duplicates", "No duplicates were found!")
            self.update_lstbx(self.hasher)

        except Exception as e: #path given does not exist
            tkinter.messagebox.showinfo("Invalid path", e) #path_to_file + " is not a valid path, please try again.")
    
    def update_lstbx(self, hasher): #updates contents of listbox to show duplicates found.
        group = 0
        for index, img in enumerate(hasher.get_images()):
            if len(img.get_group()) > 0:
                group += 1
                self.lstbx_results.insert(tk.END, "------------------------------------------- Group " + str(group) + " -------------------------------------------")
                self.lstbx_results.insert(tk.END, img.get_path())
                for duplicate in img.get_group():
                    self.lstbx_results.insert(tk.END, duplicate.get_path())

    def update_label(self, hasher): #updates labels in selected file frame with image data
        try:
            text = self.lstbx_results.curselection()[0]
            img_name = self.lstbx_results.get(text)
        except:
            pass

        for image in hasher.get_images():
            if image.get_path() == img_name:
                img = PIL.Image.open(image.get_path())
                resized = img.thumbnail((256,256))
                ph_img = ImageTk.PhotoImage(img)
                self.lbl_img_name['text'] = "File name: " + image.get_name()
                self.lbl_img_location['text'] = "File path: " + image.get_location()
                if image.get_date_taken() == "Unavailable":
                    self.lbl_taken_date['text'] = "Date taken: Unavailable"
                else:
                    self.lbl_taken_date['text'] = "Date taken: " + str(image.get_date_taken())
                self.lbl_img_creation_date['text'] = "Creation date : " + str(image.get_date())
                self.lbl_mod_time['text'] = "Date modified: " + str(image.get_mod_date())
                self.lbl_size['text'] = "Size: " + str(image.get_size()) + " KB"
                self.lbl_img_shape['text'] = "Resolution: "  + str(image.get_image_shape()[0]) + " x" + str(image.get_image_shape()[1])
                if image.get_image_channels() == "L":
                    self.lbl_img_chnls['text'] = "Colour channels: GRAYSCALE"
                else:
                    self.lbl_img_chnls['text'] = "Colour channels: " + str(image.get_image_channels())      
                self.img_thumb.config(image=ph_img)
                self.img_thumb.img = ph_img
                break

    def del_selection(self):    #identifies selection from listbox, deletes from machine and removes from listbox
        try:

            selected_index = self.lstbx_results.curselection()[0]
            selected_img = self.lstbx_results.get(selected_index)

            confirm_deletion = tk.messagebox.askquestion("Delete selected item: " + selected_img + "?", 
                "Are you sure you want to delete " + selected_img + "?" + " This operation cannot be reversed.")

            if confirm_deletion == "yes":
                for image in self.hasher.get_images():
                    if image.get_name() == selected_img:
                        if os.path.exists(image.get_path()):
                            os.remove(image.get_path())
                            self.hasher.images.remove(image)
                            try:
                                self.hasher.dpl_images.remove(image)
                            except:
                                pass
                            self.lstbx_results.delete(selected_index)
                            self.lstbx_results.select_set(selected_index-1)
                            self.lstbx_results.event_generate("<<ListboxSelect>>")
                            tk.messagebox.showinfo("Success", selected_img + " was deleted successfully.")
                        else:
                            tk.messagebox.showinfo("Error", "There was a problem removing the image.")
            else:
                tk.messagebox.showinfo("Operation cancelled", selected_img + " was not deleted.")
        except Exception as e:
            print(e)

    def move_items(self):
        
        if self.lstbx_results.size() > 1:
            conf_move = tk.messagebox.askquestion("Warning!", "This will remove duplicate images from the chosen directory leaving behind the original images."
                " They will be moved to a new directory named IDDDuplicates located on the desktop. Do you wish to continue?")
            if conf_move == "yes":
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + "\\" + "IDDDuplicates" 
                if not os.path.exists(desktop):
                    os.makedirs(desktop)
                for image in self.hasher.get_dpl_images():
                    #os.rename(image.get_path(), desktop + "\\" + image.get_name())
                    shutil.move(image.get_path(), desktop + "\\" + image.get_name())
                tk.messagebox.showinfo("Success", "Duplicates has successfully been moved.")
            else:
                tk.messagebox.showinfo("Operation cancelled", "The operation has been cancelled.")
        else:
            tk.messagebox.showinfo("Error", "No items have been found, you either have no duplicates or have not scanned a directory. Please try again.")