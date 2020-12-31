import tkinter as tk
import tkinter.messagebox


class Root:

    #constructor
    def __init__(self, master_window, Hash):

        self.Hash = Hash
        self.master_window = master_window

        #user input and file path frame
        fr_scan = tk.LabelFrame(master_window, text="Enter path to the folder you wish to scan")
        fr_scan.grid(columnspan=3, row=0, column=0, padx=5, pady=5, sticky="nw")

        self.lbl_path = tk.Label(fr_scan, text="Path to folder", height=10)
        self.lbl_path.grid(row=0,column=0, padx=5)

        self.entr_path = tk.Entry(fr_scan, width=99)
        self.entr_path.grid(row=0, column=1)

        self.btn_scan = tk.Button(fr_scan, text="Scan!", command= lambda: Hash.scan(self.entr_path.get(), Hash, self.master_window))
        self.btn_scan.grid(row=0, column=2, padx=5, pady=5)

        #file path results frame
        fr_results = tk.LabelFrame(master_window, text="Possible duplicate images")
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
        fr_selected_file = tk.LabelFrame(master_window, text="*Selected file name*")
        fr_selected_file.grid(rowspan=3,row=0, column=1, padx=5, pady=5, sticky="n")

        self.lbl_img = tk.Label(fr_selected_file, text="*selected file*", width=60, height=40)
        self.lbl_img.grid( row=1,column=1)