from time import time
import tkinter as tk
import tkinter as ttk
import tkinter.messagebox
import PIL
from PIL import ImageTk
import os
import sys
import win32api

class Root:

    def __init__(self, root, hasher):   #initialises GUI by drawing labels and storing reference to hasher and master window
        self.drives = [x[:2] for x in win32api.GetLogicalDriveStrings().split('\x00')[:-1]]
        self.radio_btns = list()
        self.option_btns = list()
        self.root = root
        self.root.grid_rowconfigure(0, weight=1)
        self.hasher = hasher
        self.init_labels()
        self.image_path_list = list()

    def init_labels(self):  #draws GUI elements
        #user input and file path frame
        self.fr_scan = tk.LabelFrame(self.root, text="Enter path to the folder you wish to scan")
        self.fr_scan.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_path = tk.Label(self.fr_scan, text="Path to folder:")
        self.lbl_path.grid(row=0,column=0, padx=5, pady=5)

        self.entr_path = tk.Entry(self.fr_scan, width=113)
        self.entr_path.grid(row=0, column=1, pady=5)

        self.btn_scan = tk.Button(self.fr_scan, text="Scan!", command= lambda: self.scan(self.entr_path.get(), self.hasher))
        self.btn_scan.grid(row=0, column=2, padx=5, pady=5)

        self.similar = tk.IntVar()
        self.chkbx_similar = tk.Checkbutton(self.fr_scan, variable=self.similar, text="Check for similar images")
        self.chkbx_similar.grid(columnspan=2, row=2, column=0, padx=5, pady=5, sticky="nw")

        self.full_drive_scan = tk.IntVar()
        self.chkbx_full = tk.Checkbutton(self.fr_scan, variable=self.full_drive_scan, text="Full Drive Scan", command=lambda:self.disable_entry())
        self.chkbx_full.grid(columnspan=2, row=4, column=0, padx=5, pady=5, sticky="nw")

        self.drive_var = tk.IntVar()
        for index, drive in enumerate(self.drives):
            self.radbtn = tk.Radiobutton(self.fr_scan, text=drive, variable=self.drive_var, value=index, state='disabled')
            self.radbtn.grid(row=5+index, column=0, padx=5, pady=5, sticky="nw")
            self.radio_btns.append(self.radbtn)

        #file path results frame

        fr_results = tk.LabelFrame(self.root, text="... ")
        fr_results.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_scrllbr = tk.Scrollbar(fr_results)
        self.lstbx_scrllbr.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.lstbx_results = tk.Listbox(fr_results, width=135, height=19)
        self.lstbx_results.config(yscrollcommand=self.lstbx_scrllbr.set)
        self.lstbx_results.bind("<<ListboxSelect>>", lambda x: self.update_label(self.hasher))

        self.lstbx_scrllbr.config(command=self.lstbx_results.yview)
        self.lstbx_results.grid(columnspan=2, row=1, column=0, padx=5, pady=5, sticky="nw")

        self.btn_del_img = tk.Button(fr_results, text="Delete selection", command= self.del_selection)
        self.btn_del_img.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        self.btn_mov_items = tk.Button(fr_results, text = "Move items to new directory",  command=lambda:self.move_images())
        self.btn_mov_items.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.lbl_instructions = tk.Label(fr_results, text="Here you can see groups of duplicate images,"
            " select the item you wish to manage and it will appear in the 'Selected item' tab on the right.\nPlease be aware, the images identified may not be exact duplicates, review each image before taking any action.")
        self.lbl_instructions.grid(row=4, column=0, padx=5, pady=5, sticky="nw")


        #selected file frame
        fr_selected_file = tk.LabelFrame(self.root, text="Selected item")
        fr_selected_file.grid(rowspan=3, row=0, column=1, padx=5, pady=5, sticky="nw")

        self.lbl_img_name = tk.Label(fr_selected_file, text="File name: ")
        self.lbl_img_name.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

        self.lbl_img_location = tk.Label(fr_selected_file, text="File path: ")
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

        self.open_btn = tk.Button(fr_selected_file, text = "Open Image",  command=lambda:self.open_image())
        self.open_btn.grid(row=10, column=0, padx=5, pady=10, sticky="nw")


#Initate scan and duplciate identification   
    def reset(self, hasher):    #resets data
        self.lstbx_results.delete(0, tk.END)    #clear listbox and images list for next 
        self.clear_sel_lbl()
        hasher.images.clear()
        hasher.dpl_images.clear()
        hasher.images_scanned = 0
        hasher.items_scanned = 0
        self.hasher.check_similar = self.similar.get()

    def scan(self, path_to_file, hasher):   #Initates scan for images
        self.reset(hasher)

        if self.full_drive_scan.get() == 1: #full drive scan
            confirm_scan = tk.messagebox.askquestion("Warning", "Scanning an entire drive is not recommended as it may identify system files necessary for software operation, you may also experience longer than usual search times. Would you like to continue?")
            
            if confirm_scan == "yes":
                self.hasher.scan_drive(self.drive_var.get(), self.drives)
            else:
                return

        else:   #directory scan
            if len(path_to_file) != 0:
                if os.path.exists(path_to_file):                    
                    self.hasher.scan_path(path_to_file)

                else:
                    tk.messagebox.showinfo("Error", "Invalid path, please try again.")
                    return
            else:
                tk.messagebox.showinfo("Error","No path given, please try again.")
                return
                
        self.identify_duplicates()
        self.update_lstbx(self.hasher)
        self.fr_results.configure(text="Possible duplicate images: " + str(len(self.hasher.get_dpl_images())))

    def identify_duplicates(self):  #Initiates duplicate/similar image identification
        if self.hasher.get_images_length() == 0:    #no images
            tkinter.messagebox.showinfo("Error", "No images found, please check the directory for images and then try again.")
            return

        elif self.hasher.get_images_length() > 1:   #images found

            self.hasher.get_images().sort(key=lambda x: x.get_hash(), reverse=False)    #sort images based on hash value

            for index, image in enumerate(self.hasher.get_images()):
                if self.hasher.check_similar == 0:  #look for duplicates
                    if  not image.get_is_duplicate():
                        self.hasher.get_duplicate_range(self.hasher.images, image, index) 

                else:   #look for similar images
                    if not image.get_is_similar():
                        self.hasher.similar_search(image, self.hasher.get_images(), index)                            
        
        if self.hasher.get_dpl_images_length() < 1 and self.hasher.check_similar == 0:
            tk.messagebox.showinfo("No duplicates", "No duplicates were found!")
        elif self.hasher.get_dpl_images_length() < 1 and self.hasher.check_similar == 1:
            tk.messagebox.showinfo("No duplicates", "No similar images found!")

#update, interact and modify widgets

    def disable_entry(self):    #disables entry box if user decided to scan whole drive
        if self.full_drive_scan.get() == 1:
            self.entr_path.config(state='disabled')
            for btn in self.radio_btns:
                btn.config(state='normal')
        else:
            self.entr_path.config(state='normal')
            for btn in self.radio_btns:
                btn.config(state = 'disabled')

    def update_lstbx(self, hasher): #updates contents of listbox to show duplicates found.
        self.lstbx_results.delete(0, tk.END)
        group = 0
        for img in hasher.get_dpl_images():
            if len(img.get_group()) > 0:
                group += 1
                self.lstbx_results.insert(tk.END, "------------------------------------------- Group " + str(group) + " - Items(" + str(len(img.get_group()) + 1)+") -------------------------------------------")
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
                img.thumbnail((512,256))
                ph_img = ImageTk.PhotoImage(img)
                self.lbl_img_name['text'] = "File name: " + image.get_name()
                self.lbl_img_location['text'] = "File path: " + image.get_location()
                if image.get_date_taken() == None:
                    self.lbl_taken_date['text'] = "Date taken: Unavailable"
                else:
                    self.lbl_taken_date['text'] = "Date taken: " + str(image.get_date_taken())
                self.lbl_img_creation_date['text'] = "Creation date : " + str(image.get_date())
                self.lbl_mod_time['text'] = "Date modified: " + str(image.get_mod_date())
                self.lbl_size['text'] = "Size: " + str(image.get_size()) + " KB"
                self.lbl_img_shape['text'] = "Resolution: "  + str(image.get_image_shape()[0]) + " x" + str(image.get_image_shape()[1])
                if image.get_image_channels() == "L":
                    self.lbl_img_chnls['text'] = "Colour channels: GRAYSCALE"
                elif image.get_image_channels() != None:
                    self.lbl_img_chnls['text'] = "Colour channels: " + str(image.get_image_channels()) 
                self.img_thumb.config(image=ph_img)
                self.img_thumb.img = ph_img

    def del_selection(self):    #identifies selection from listbox, deletes from machine and removes from listbox
        try:
            selected_index = self.lstbx_results.curselection()[0]   #get selected index
            selected_img = self.lstbx_results.get(selected_index)   #convert index into string

            confirm_deletion = tk.messagebox.askquestion("Delete selected item: " + selected_img + "?", 
                "Are you sure you want to delete " + selected_img + "?" + " This operation cannot be reversed.")    #get input from the user confirming action

            if confirm_deletion == "yes":
                for image in self.hasher.get_dpl_images():  #loop through hasher duplicate images looking for string above
                    if image.get_path() == selected_img:    #if found, check exists in windows, remove item from windows and dynamic lists
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
        except:
            tk.messagebox.showinfo("Error", "You have not selected an item.")

    def open_image(self):   #displays image in windows photo viewer so user can compare images
        try:
            selected_index = self.lstbx_results.curselection()[0]   #get selected index
            selected_img = self.lstbx_results.get(selected_index)   #convert index into string
            image = PIL.Image.open(selected_img)
            image.show(title=selected_img)
        except:
            tk.messagebox.showinfo("Error", "You have not selected an image.")

    def move_images(self):  #move all but one duplicate from scanned directory to new directory at root of drive        
        if self.lstbx_results.size() > 1:
            conf_move = tk.messagebox.askquestion("Warning!", "This will remove duplicate images from the chosen directory leaving behind one of each image."
                " They will be moved to a new directory named IDDDuplicates located at the root directory of the specified drive. Do you wish to continue?")
            if conf_move == "yes":
                if self.full_drive_scan.get() == 1: #if user selected full drive scan get drive from logical drives
                    drive = self.drives[self.drive_var.get()] + "\\" + "IDDDuplicates"
                else:   #else get the drive from the path user entered at beginning
                    path = self.entr_path.get()
                    s = path.split("\\", 1)
                    drive = s[0] + "\\" + "IDDDuplicates"
                if not os.path.exists(drive):   #if path does not exist then create a new folder
                    os.makedirs(drive)
                for index, image in enumerate(self.hasher.get_dpl_images()):    #loop through hasher duplicate images and if the image does not have a group i.e. it is not an original move to folder
                    if len(image.get_group()) == 0:
                        os.rename(image.get_path(), drive + "\\" + "dupe" + str(index) + "__" + image.get_name())
                tk.messagebox.showinfo("Success", "Duplicates have successfully been moved.")
                self.hasher.del_group()
                self.update_lstbx(self.hasher)
                self.clear_sel_lbl()
                return
            else:
                tk.messagebox.showinfo("Operation cancelled", "The operation has been cancelled.")
        else:
            tk.messagebox.showinfo("Error", "No items have been found, you either have no duplicates or have not scanned a directory. Please try again.")

    def clear_sel_lbl(self):    #clears the selected item label when a new scan is run
        self.lbl_img_name['text'] = "File name: "
        self.lbl_img_location['text'] = "File path: "
        self.lbl_taken_date['text'] = "Date taken: "
        self.lbl_img_creation_date['text'] = "Creation date: "
        self.lbl_mod_time['text'] = "Date modified: "
        self.lbl_size['text'] = "Size: "
        self.lbl_img_shape['text'] = "Resolution: "
        self.lbl_img_chnls['text'] = "Colour channels: "
        self.img_thumb.config(image=None)
        self.img_thumb.img = None