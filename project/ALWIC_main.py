# -*- coding: utf-8 -*-
"""
Created on Friday May 19 2023

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

#Import of packages 

import numpy as np
import pandas as pd
import platform
import tkinter as tk
import os
import webbrowser
from tkinter import filedialog
import shutil as stl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from functools import partial
import PIL

#import from local files 

import parameters_calculations as param_calc
import plots as plots
import loading_files as lf
import save_results as sr
import table_results_p2 as table_res2
import table_results_p1 as table_res_1
import Calibration as cal
import memory_correction_van_Geldern_method as MC_calc_VG
import memory_correction_Groning_method as MC_calc_G
import prefill as pref
import check_errors

pd.options.mode.chained_assignment = None

class Main_Window():
    def __init__(self):
        ##################DEFINITION OF MAIN WINDOW'S WIDGETS##################
        # Instances variables 
        
        self.std_values_file, self.std_short_names_list = lf.load_standard_csv_file()
        self.groning_params_file,self.instruments_names_list=lf.load_groning_params_file()
        
        # Master Window definition 
        
        self.master_window = tk.Tk()
        self.master_window.title("ALWIC-tool")
        if platform.system()=="Linux":
            self.master_window.state('normal')
        else:
            self.master_window.state("zoomed")
        self.master_window.configure(bg="#BEE7E8")
        self.master_window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Head of window

        self.message_text_1_1 = tk.Message(self.master_window, text="Welcome to ALWIC-tool !",
                                      font=("Helvetica Neue", 18),  width=500,
                                      bg="#D11F00", fg="white", relief="ridge", bd=3)
        self.message_text_1_1.place(relx=0.5, rely=0.05, anchor="center")
        
        # Panned window 1 (Protocol)

        self.pw1 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#327D94")
        self.pw1.grid(row=2, column=1)
        self.label_1_1 = tk.Label(self.pw1, text="Protocol to follow :", font=("Helvetica Neue", 15), fg="white", bg="#327D94")
        self.label_1_1.grid(row=1, column=1)
        self.optionlist = ["van Geldern mode", "van Geldern d17O mode","Gröning mode", "Gröning d17O mode"]
        self.option_protocol = tk.StringVar(value="van Geldern mode") # change the default protocol here 
        self.optionmenu_1_1 = tk.OptionMenu(self.pw1, self.option_protocol, *self.optionlist,command= lambda _:self.define_groning_parameters_table())
        self.optionmenu_1_1["menu"].configure(font=("Helvetica Neue", 15))
        self.optionmenu_1_1.configure(font=("Helvetica Neue", 15), fg="white", bg="#327D94", activebackground="#327D94", activeforeground="white")
        self.optionmenu_1_1.grid(row=2, column=1, sticky="NSEW")
        self.pw1.place(relx=0.125, rely=0.15, anchor="center")

        # Panned window 2 (file directory)

        self.pw2 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#327D94")
        self.pw2.grid(row=2, column=1)
        self.label_2_1 = tk.Label(self.pw2, text="Choose the type of directory :", font=("Helvetica Neue", 15), bg="#327D94", fg="white")
        self.label_2_1.grid(row=1, column=1 )
        self.optionlist1 = ["Local directory", "Google drive"]
        self.option_protocol1 = tk.StringVar(value="Google drive") # Value should not be changed in order to function properly 
        self.optionmenu_2_1 = tk.OptionMenu(self.pw2, self.option_protocol1, *self.optionlist1, command= lambda _:self.copy_paste_local_dir())
        self.optionmenu_2_1["menu"].configure(font=("Helvetica Neue", 15))
        self.optionmenu_2_1.configure(font=("Helvetica Neue", 15), fg="white", bg="#327D94", activebackground="#327D94", activeforeground="white")
        self.optionmenu_2_1.grid(row=2, column=1, sticky="NSEW")
        self.pw2.place(relx=0.3, rely=0.15, anchor="center")
                
        # Panned window 3 (filename)

        self.pw3 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#327D94")
        self.pw3.grid(row=1, column=3)
        self.label_3_1 = tk.Label(self.pw3, font=("Helvetica Neue", 15), text="Enter the filename :", fg="white", bg="#327D94")
        self.label_3_1.grid(row=1, column=1)
        self.entry_3_1 = tk.Entry(self.pw3, font=("Helvetica Neue", 15), width=40)
        self.entry_3_1.grid(row=1, column=2)
        self.prefill_button = tk.Button(self.pw3, text="Prefill", command=self.command_prefil, font=("Helvetica Neue", 15), width=5, relief="raised", fg="white", bg="#327D94")
        self.prefill_button.grid(row=1, column=3)
        self.pw3.place(relx=0.51, rely=0.15, anchor="w")
                
        # Panned window 4 (standards values table)

        self.pw4 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#056CF2")
        self.pw4.grid(row=1, column=3)
        self.entry_4_1 = tk.Entry(self.pw4, font=("Helvetica Neue", 12), width=2)
        self.entry_4_1.grid(row=1, column=2, padx=10)
        self.label_4_1 = tk.Label(self.pw4, text="Number of standard injected", font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
        self.label_4_1.grid(row=1, column=1, sticky="NSEW")
        self.button_4_1 = tk.Button(self.pw4, text="Update", command=self.define_table, font=("Helvetica Neue", 15), height=3, width=6, relief="raised", bg="#056CF2", fg="white")
        self.button_4_1.grid(row=1, column=3)
        self.pw4.place(relx=0.18, rely=0.35, anchor="center")
        
        # Panned window 5 (Known sample positions)

        self.pw5 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#056CF2")
        self.pw5.grid(row=2, column=3)
        self.label_5_1 = tk.Label(self.pw5, text="Spy samples ?", font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
        self.label_5_1.grid(row=1, column=1)
        self.var_5_1 = tk.IntVar()
        self.check_button_5_1 = tk.Checkbutton(self.pw5, variable=self.var_5_1, onvalue=1, offvalue=0, bg="#056CF2", activebackground="#056CF2")
        self.check_button_5_1.grid(row=1, column=2)
        self.entry_5_1 = tk.Entry(self.pw5, font=("Helvetica Neue", 12), width=2)
        self.entry_5_1.grid(row=2, column=2)
        self.label_5_2 = tk.Label(self.pw5, text="Number of known samples", font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
        self.label_5_2.grid(row=2, column=1, sticky="NSEW")
        self.button_5_1 = tk.Button(self.pw5, text="Update", command=self.define_known_sample_table, font=("Helvetica Neue", 15), height=2, width=6, relief="raised", bg="#056CF2", fg="white")
        self.button_5_1.grid(row=2, column=3)
        self.pw5.place(relx=0.5, rely=0.35, anchor="center")
        
        # Panned window 6 (Injections and removed injections for samples)

        self.pw6 = tk.PanedWindow(self.master_window, orient="vertical",  bg="#17E8C2", relief="solid")
        self.pw6.grid(row=3, column=2)
        self.label_6_1 = tk.Label(self.pw6, text="Number of samples injected : ", font=("Helvetica Neue", 14), bg="#17E8C2")
        self.label_6_1.grid(row=1, column=1, sticky="NSEW")
        self.entry_6_1 = tk.Entry(self.pw6, width=4, font=("Helvetica Neue", 12))
        self.entry_6_1.grid(row=1, column=2, sticky="NSEW")
        self.label_6_2 = tk.Label(self.pw6, text="Number of injections per sample : ", font=("Helvetica Neue", 14), bg="#17E8C2")
        self.label_6_2.grid(row=2, column=1, sticky="NSEW")
        self.entry_6_2 = tk.Entry(self.pw6, width=4, font=("Helvetica Neue", 12))
        self.entry_6_2.grid(row=2, column=2, sticky="NSEW")
        self.label_6_3 = tk.Label(self.pw6, text="Number of injections removed per sample : ", font=("Helvetica Neue", 14), bg="#17E8C2")
        self.label_6_3.grid(row=3, column=1, sticky="NSEW")
        self.entry_6_3 = tk.Entry(self.pw6, width=4, font=("Helvetica Neue", 12))
        self.entry_6_3.grid(row=3, column=2, sticky="NSEW")
        self.pw6.place(relx=0.8, rely=0.35, anchor="center")
        
        # Panned window 7 (Injections and removed injections for standards)

        self.pw7 = tk.PanedWindow(self.master_window, orient="vertical", bg="#17E8C2", relief="solid")
        self.pw7.grid(row=2, column=2)
        self.label_7_1 = tk.Label(self.pw7, text="Number of injections per standard : ", font=("Helvetica Neue", 14), bg="#17E8C2")
        self.label_7_1.grid(row=1, column=1)
        self.entry_7_1 = tk.Entry(self.pw7, font=("Helvetica Neue", 12), width=4)
        self.entry_7_1.grid(row=1, column=2, sticky="NSEW")
        self.label_7_2 = tk.Label(self.pw7, text="Number of injections removed per standard : ", font=("Helvetica Neue", 14), bg="#17E8C2")
        self.label_7_2.grid(row=2, column=1)   
        self.entry_7_2 = tk.Entry(self.pw7, font=("Helvetica Neue", 12), width=4)
        self.entry_7_2.grid(row=2, column=2, sticky="NSEW")
        self.pw7.place(relx=0.8, rely=0.5, anchor="center")
        
        # Panned window 8 (Identities of users)

        self.pw8 = tk.PanedWindow(self.master_window, orient="vertical", relief="solid", bg="#17E8C2")
        self.pw8.grid(row=2, column=2)
        self.label_8_1=tk.Label(self.pw8, text="Operator ID :", font=("Helvetica Neue", 15), bg="#17E8C2")
        self.label_8_1.grid(row=1, column=1)
        self.entry_8_1=tk.Entry(self.pw8, font=("Helvetica Neue", 15), width=17)
        self.entry_8_1.grid(row=1, column=2)
        self.label_8_2=tk.Label(self.pw8, text="Processor ID :", font=("Helvetica Neue", 15), bg="#17E8C2")
        self.label_8_2.grid(row=2,column=1) 
        self.entry_8_2=tk.Entry(self.pw8, font=("Helvetica Neue", 15), width=17)
        self.entry_8_2.grid(row=2, column=2)
        self.pw8.place(relx=0.18, rely=0.9,anchor="center")
        
        # Processing Button 

        self.button_processing = tk.Button(self.master_window, text="Processing", command=self.processing, font=("Helvetica Neue", 18), bg="#FE4000",relief="raised", height=3, width=9, activebackground="#80669d", activeforeground="white")
        self.button_processing.place(relx=0.8, rely=0.7, anchor="center")
        
        # Menu (links to documentation online and offline)
        
        self.Menus = tk.Menu(self.master_window)
        self.master_window.config(menu=self.Menus)
        self.helpmenu = tk.Menu(self.Menus, tearoff=0)
        self.Menus.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='Github', command=self.open_github)
        self.helpmenu.add_command(label="Document", command=self.open_pdf_documentation)
        
        self.master_window.mainloop()
        
##################END OF DEFINITION OF MAIN WINDOW'S WIDGETS###################
        
##################METHODS USED TO MODIFY MAIN WINDOW###########################

    # Delete temporary files before quiting the app 
        
    def close_window(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            files = os.listdir("./files/raw_files_temp/")
            if files != []:
                for file in files:
                    os.remove("./files/raw_files_temp/"+file)
            files = os.listdir("./files/saving_temp/")
            if files != []:
                for file in files:
                    os.remove("./files/saving_temp/"+file)
            self.master_window.destroy()
        return
    
    # Commands to open the documentation (used in the menu bar)

    def open_github(self):
        # open a new window in default navigator 
        url = "https://github.com/baptistebordet1/ALWIC-tool/blob/main/README.md"
        webbrowser.open_new(url)
        return

    def open_pdf_documentation(self):
        # open pdf with default application 
        os.system("start " + "./files/user_documentation.pdf")
        return
    
    # Function to define parameters for the groning method

    def define_groning_parameters_table(self):
        if self.option_protocol.get()== "van Geldern mode" or self.option_protocol.get()=="van Geldern d17O mode":
            try:
                self.pw9.destroy()
                self.button_evaluation_groning_params.destroy()
            except AttributeError:
                self.first_time=1
        if self.option_protocol.get()=="Gröning mode" or self.option_protocol.get()=="Gröning d17O mode":
            self.button_evaluation_groning_params=tk.Button(self.master_window,text="Evaluate \n Parameters", command=self.open_evaluate_parameters_page, font=("Helvetica Neue", 15), relief="raised", bg="#056CF2", fg="white")
            self.button_evaluation_groning_params.place(relx=0.65, rely=0.86)
            try:
                self.pw9.destroy()
            except NameError:
                self.first_time = 1
            except AttributeError:
                self.first_time = 1
            except tk.TclError:
                self.first_time = 1
            self.pw9=tk.PanedWindow(self.master_window,orient="vertical", bg="#056CF2",relief="solid")
            self.pw9.grid(row=4, column=3)
            self.pw9.place(relx=0.5, rely=0.9, anchor="center")
            self.label_9_4 = tk.Label(self.pw9, text="\u03B418O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_9_4.grid(row=1, column=3, sticky="NSEW")
            self.label_9_5 = tk.Label(self.pw9, text="\u03B4D", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_9_5.grid(row=1, column=4, sticky="NSEW")
            if self.option_protocol.get()=="Gröning d17O mode":
                self.label_9_6=tk.Label(self.pw9, text="\u03B417O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
                self.label_9_6.grid(row=1, column=5, sticky="NSEW")
            self.label_9_1=tk.Label(self.pw9, text="\u03B1", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_9_1.grid(row=2,column=2)
            self.label_9_2=tk.Label(self.pw9, text="\u03B2", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_9_2.grid(row=3,column=2)
            self.label_9_3=tk.Label(self.pw9, text="balance", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_9_3.grid(row=4,column=2)
            self.groning_params={}
            for i in range(0,3):
                self.entry=tk.Text(self.pw9,height=1, width=10,state="disabled")
                self.entry.grid(row=i+2, column=3, sticky="NSEW")
                self.groning_params["entry_9_2_"+str(i+2)] = self.entry
                self.entry=tk.Text(self.pw9,height=1, width=10,state="disabled")
                self.entry.grid(row=i+2, column=4, sticky="NSEW")
                self.groning_params["entry_9_3_"+str(i+2)] = self.entry
                if self.option_protocol.get()=="Gröning d17O mode":
                    self.entry=tk.Text(self.pw9,height=1, width=10,state="disabled")
                    self.entry.grid(row=i+2, column=5, sticky="NSEW")
                    self.groning_params["entry_9_4_"+str(i+2)] = self.entry
            self.option_name_9 = tk.StringVar(value="INSTRUMENT NAME")
            self.option_menu_9 = tk.OptionMenu(self.pw9, self.option_name_9, *self.instruments_names_list, command=lambda _: self.change_groning_params())
            self.option_menu_9.config(bg="#056CF2", activebackground="#056CF2", bd=0, fg="white", font=("Helvetica Neue", 10))
            self.option_menu_9.grid(row=1, column=2)
    
    # Open the evaluation parameters page
    
    def open_evaluate_parameters_page(self):
        self.open_eval_page=evaluate_parameters_page(self)
        
    # Function to change the groning's parameters values in the table 
    
    def change_groning_params(self):
        m=0
        for i in range(0,3):
            m=m+1
            for k in range(0, len(self.instruments_names_list)):
                if self.option_name_9.get()==self.instruments_names_list[k]:
                    self.groning_params["entry_9_2_"+str(i+2)].config(state="normal")
                    self.groning_params["entry_9_2_"+str(i+2)].delete("1.0", "end")
                    self.groning_params["entry_9_2_"+str(i+2)].insert("1.0",str(self.groning_params_file[self.groning_params_file.columns[m]].iloc[k]))
                    self.groning_params["entry_9_2_"+str(i+2)].config(state="disabled")
                    m=m+3
                    self.groning_params["entry_9_3_"+str(i+2)].config(state="normal")
                    self.groning_params["entry_9_3_"+str(i+2)].delete("1.0", "end")
                    self.groning_params["entry_9_3_"+str(i+2)].insert("1.0",str(self.groning_params_file[self.groning_params_file.columns[m]].iloc[k]))
                    self.groning_params["entry_9_3_"+str(i+2)].config(state="disabled")
                    if self.option_protocol.get()=="Gröning mode": 
                        m=m-3
                    if self.option_protocol.get()=="Gröning d17O mode":
                        m=m+3
                    if self.option_protocol.get()=="Gröning d17O mode":
                        self.groning_params["entry_9_4_"+str(i+2)].config(state="normal")
                        self.groning_params["entry_9_4_"+str(i+2)].delete("1.0", "end")
                        self.groning_params["entry_9_4_"+str(i+2)].insert("1.0",str(self.groning_params_file[self.groning_params_file.columns[m]].iloc[k]))
                        self.groning_params["entry_9_4_"+str(i+2)].config(state="disabled")
                        m=m-6
                        
    # Function to copy paste the working file into the raw_files_temp directory if local_directory is choosen (aswell as writting the filenaem in entry_3_1)

    def copy_paste_local_dir(self):
        if self.option_protocol1.get() == "Local directory":
            filepath = filedialog.askopenfilename()
            filepath_splitted = os.path.split(filepath)
            directory_file = filepath_splitted[0]
            filename_long = filepath_splitted[1].rpartition(".")
            filename = filename_long[0]
            dest = "./files/raw_files_temp/"+filename+".csv"
            stl.copyfile(directory_file+"/"+filename+".csv", dest)
            self.entry_3_1.delete(0, "end")
            self.entry_3_1.insert(0, filename)
                        
    # Function to set some entries used in prefill 

    def set_prefill(self):
        self.entry_4_1.delete(0, "end")
        self.entry_4_1.insert(0, self.std_nbr)
        self.entry_7_1.delete(0, "end")
        self.entry_7_1.insert(0, self.inj_per_std)
        self.entry_6_1.delete(0, "end")
        self.entry_6_1.insert(0, self.spl_nbr)
        self.entry_6_2.delete(0, "end")
        self.entry_6_2.insert(0, self.inj_per_spl)
        if self.is_spy == 1:
            self.check_button_5_1.select()
            self.entry_5_1.delete(0, "end")
            self.entry_5_1.insert(0, self.known_sample_nbr)

    # Function which commands the prefil

    def command_prefil(self):
        if self.entry_3_1.get()=="":
            tk.messagebox.showerror("Error", "Error : You haven't filled any filename. ",parent=self.master_window)
            return
        self.result_file_df, self.inj_nbr_df, self.id1_df, self.id2_df, self.port_df = pref.get_identifiers(self.option_protocol1, self.entry_3_1)
        if self.id2_df.dropna(how='all').empty == True:
            tk.messagebox.showerror("Error", "Error : Your file can't be prefilled (see documentation to know how to set-up the prefill) ",parent=self.master_window)
            return
        self.error,*b = pref.counter(self.id1_df, self.id2_df, self.inj_nbr_df, self.port_df)
        if self.error==0:
            self.error,self.inj_per_std, self.std_nbr, self.inj_per_spl, self.spl_nbr, self.is_spy, self.known_sample_nbr, self.spy_port, self.spy_name_found, self.std_name_found=pref.counter(self.id1_df, self.id2_df, self.inj_nbr_df,self.port_df)
        if self.error==1:
            tk.messagebox.showerror("Error","No injection labelled with STD found",parent=self.master_window)
            return
        if self.error==2:
            tk.messagebox.showerror("Error","No injection labelled with SAMPLE found",parent=self.master_window)
            return
        if self.error==3:
            tk.messagebox.showerror("Error", "No injection labelled with SPY found",parent=self.master_window)
        self.set_prefill()
        self.define_table()
        self.define_known_sample_table()
        for i, j in enumerate(self.option_name_std_table_dict):
            self.option_name_std_table_dict[j].set(self.std_name_found[i])
            self.change_std_values(i,self.option_name_std_table_dict[j].get())
        if self.is_spy == True:
            for i, j in enumerate(self.option_port_spy_table_dict):
                self.option_port_spy_table_dict[j].set(self.spy_port[i])
            for i, j in enumerate(self.option_name_spy_table_dict):
                self.option_name_spy_table_dict[j].set(self.spy_name_found[i])
                self.change_spy_values(i,self.option_name_spy_table_dict[j].get())

    # Function to define the standards value's table

    def define_table(self):
        # get the number of standard used and check if it's a int 
        self.std_nbr = self.entry_4_1.get()
        if self.std_nbr.isdigit() == False:
            tk.messagebox.showwarning("Warning", "You entered a non-authorized value !")
            return
        self.std_nbr = int(self.std_nbr)
        if self.std_nbr > 8: # change the value here when you add more standards 
            tk.messagebox.showinfo( "Info", "Your number of standard seems high (more than 8) please verify if you made a typo.")
        # Create the table widget (it doesn't exits in TKinter so it's just a paned window)
        # First part is fixed independant from std_nbr
        
        try:
            self.pw10.destroy()
        except NameError:
            self.first_time = 1
        except AttributeError:
            self.first_time = 1
        self.pw10 = tk.PanedWindow(self.master_window, orient="vertical", bg="#056CF2" ,relief="solid")
        self.pw10.grid(row=8, column=6)  # change here the rows' number to add more standards and don't forget to change te condition above
        self.pw10.place(relx=0.18, rely=0.65, anchor="center")
        self.label_10_4 = tk.Label(self.pw10, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_10_4.grid(row=1, column=4, sticky="NSEW")
        self.label_10_5 = tk.Label(self.pw10, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_10_5.grid(row=1, column=5, sticky="NSEW")
        if self.option_protocol.get() == "van Geldern d17O mode" or self.option_protocol.get() == "Gröning d17O mode":
            self.label_10_10 = tk.Label(self.pw10, text="\u03B417O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_10_10.grid(row=1, column=6, sticky="NSEW") 
            
        # Second part is mutable dependant on std_nbr 
        
        self.label_std_table_dict = {}
        self.entry_std_table_dict = {}
        self.var_checkbox_std_table_dict = {}
        self.checkbox_std_table_dict = {}
        self.option_name_std_table_dict = {}
        self.option_menu_std_table_dict = {}
        for i in range(0,self.std_nbr):
            self.label = tk.Label(self.pw10, text='std '+str(i+1)+' : ',bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label.grid(row=i+2, column=1, sticky='NSEW')
            self.label_std_table_dict["label_10_"+str(i+1)]=self.label
            self.entry = tk.Text(self.pw10, height=1, width=10)
            self.entry.grid(row=i+2, column=4, sticky="NSEW")
            self.entry.config(state="disabled")
            self.entry_std_table_dict["entry_10_"+str(3*i+1)] = self.entry
            self.entry = tk.Text(self.pw10, height=1, width=10)
            self.entry.grid(row=i+2, column=5, sticky="NSEW")
            self.entry.config(state="disabled")
            self.entry_std_table_dict["entry_10_"+str(3*i+2)] = self.entry
            if self.option_protocol.get() == "van Geldern d17O mode" or self.option_protocol.get()=="Gröning d17O mode":
                self.entry = tk.Text(self.pw10, height=1, width=10)
                self.entry.grid(row=i+2, column=6, sticky="NSEW")
                self.entry.config(state="disabled")
                self.entry_std_table_dict["entry_10_"+str(3*(i+1))] = self.entry # note that str(3*(i+1) is equivalent to str(3*i+3))
            if i !=0:
                self.var = tk.IntVar(value=1)
                self.var_checkbox_std_table_dict["var_10_"+str(i)] = self.var
                self.checkbox = tk.Checkbutton( self.pw10, variable=self.var_checkbox_std_table_dict["var_10_"+str(i)], bg="#056CF2", activebackground="#056CF2")
                self.checkbox.grid(row=i+2, column=2)
                self.checkbox_std_table_dict["checkbox_10_"+str(i)] = self.checkbox
            self.option_name = tk.StringVar(value="Select STD")
            self.option_name_std_table_dict["option_name"+str(i+1)] = self.option_name
            self.option_menu = tk.OptionMenu(self.pw10, self.option_name_std_table_dict["option_name"+str(i+1)], *self.std_short_names_list, command=partial(self.change_std_values,i))
            self.option_menu.config(bg="#056CF2", activebackground="#056CF2", bd=0, fg="white", font=("Helvetica Neue", 10))
            self.option_menu.grid(row=i+2, column=3)
            self.option_menu_std_table_dict["option_menu_10_"+str(i+1)] = self.option_menu
                
    # Function to change values of standards printed

    def change_std_values(self,i,option_name):
        for k in range(0, len(self.std_short_names_list)):
            if option_name == self.std_short_names_list[k]:
                self.entry_std_table_dict["entry_10_"+str(3*i+1)].config(state="normal")
                self.entry_std_table_dict["entry_10_"+str(3*i+1)].delete("1.0", "end")
                self.entry_std_table_dict["entry_10_"+str(3*i+1)].insert("1.0", str(self.std_values_file["d18O"].iloc[k]))
                self.entry_std_table_dict["entry_10_"+str(3*i+1)].config(state="disabled")
                self.entry_std_table_dict["entry_10_"+str(3*i+2)].config(state="normal")
                self.entry_std_table_dict["entry_10_"+str(3*i+2)].delete("1.0", "end")
                self.entry_std_table_dict["entry_10_"+str(3*i+2)].insert("1.0", str(self.std_values_file["dD"].iloc[k]))
                self.entry_std_table_dict["entry_10_"+str(3*i+2)].config(state="disabled")
                if self.option_protocol.get() == 'van Geldern d17O mode' or self.option_protocol.get()=="Gröning d17O mode":
                    self.entry_std_table_dict["entry_10_"+str(3*(i+1))].config(state="normal")
                    self.entry_std_table_dict["entry_10_"+str(3*(i+1))].delete("1.0", "end")
                    self.entry_std_table_dict["entry_10_"+str(3*(i+1))].insert("1.0", str(self.std_values_file["d17O"].iloc[k]))
                    self.entry_std_table_dict["entry_10_"+str(3*(i+1))].config(state="disabled")
                break
    
    # Function to define the spy samples values table
    
    def define_known_sample_table(self):
        self.port_list, self.result_file_df = lf.loading_file(self.option_protocol1, self.entry_3_1)
        self.known_sample_nbr = self.entry_5_1.get()
        if self.known_sample_nbr.isdigit() == False:
            tk.messagebox.showwarning("Warning", "You entered a non-authorized value !")
            return
        self.known_sample_nbr = int(self.known_sample_nbr)
        if self.known_sample_nbr > 8: # change the value here when you add more spy samples  
            tk.messagebox.showinfo( "Info", "Your number of spy samples seems high (more than 8) please verify if you made a typo.")
        try:
            self.pw11.destroy()
        except AttributeError:
            self.first_time = 1
        self.pw11 = tk.PanedWindow(self.master_window, orient="vertical", bg="#056CF2", relief="solid")
        self.pw11.grid(row=8, column=6) # change here the rows' number to add more spy samples
        self.pw11.place(relx=0.5, rely=0.65, anchor="center")
        self.label_11_4 = tk.Label(self.pw11, text="\u03B418O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_11_4.grid(row=1, column=4, sticky="NSEW")
        self.label_11_5 = tk.Label(self.pw11, text="\u03B4D", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_11_5.grid(row=1, column=5, sticky="NSEW")
        if self.option_protocol.get() == "van Geldern d17O mode" or self.option_protocol.get()=="Gröning d17O mode":
            self.label_11_6 = tk.Label(self.pw11, text="d17O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_11_6.grid(row=1, column=6, sticky="NSEW")
        
        # Second part is mutable dependant on known_sample_nbr 
        
        self.label_spy_table_dict = {}
        self.entry_spy_table_dict = {}
        self.var_checkbox_spy_table_dict = {}
        self.checkbox_spy_table_dict = {}
        self.option_port_spy_table_dict = {}
        self.option_port_menu_spy_table_dict ={}
        self.option_name_spy_table_dict = {}
        self.option_menu_spy_table_dict = {}
        
        for i in range(0,self.known_sample_nbr):
            self.label = tk.Label(self.pw11, text='spy '+str(i+1)+' : ',bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label.grid(row=i+2, column=1, sticky='NSEW')
            self.label_spy_table_dict["label_11_"+str(i+1)]=self.label
            self.entry = tk.Text(self.pw11, height=1, width=10)
            self.entry.grid(row=i+2, column=4, sticky="NSEW")
            self.entry.config(state="disabled")
            self.entry_spy_table_dict["entry_11_"+str(3*i+1)] = self.entry
            self.entry = tk.Text(self.pw11, height=1, width=10)
            self.entry.grid(row=i+2, column=5, sticky="NSEW")
            self.entry.config(state="disabled")
            self.entry_spy_table_dict["entry_11_"+str(3*i+2)] = self.entry
            self.option_port = tk.StringVar(value=self.port_list[i])
            self.option_port_spy_table_dict["option_port_11_"+str(i+1)] = self.option_port
            self.option_port_menu = tk.OptionMenu(self.pw11, self.option_port_spy_table_dict["option_port_11_"+str(i+1)], *self.port_list)
            self.option_port_menu.config(bg="#056CF2", activebackground="#056CF2",bd=0, fg="white", font=("Helvetica Neue", 10))
            self.option_port_menu.grid(row=i+2, column=2)
            self.option_port_menu_spy_table_dict["option_port_menu_11_"+str(i+1)] = self.option_port_menu
            if self.option_protocol.get() == "van Geldern d17O mode" or self.option_protocol.get()=="Gröning d17O mode":
                self.entry = tk.Text(self.pw11, height=1, width=10)
                self.entry.grid(row=i+2, column=6, sticky="NSEW")
                self.entry.config(state="disabled")
                self.entry_spy_table_dict["entry_11_"+str(3*(i+1))] = self.entry # note that str(3*(i+1) is equivalent to str(3*i+3))
            self.option_name = tk.StringVar(value="Select SPY")
            self.option_name_spy_table_dict["option_name_11_"+str(i+1)] = self.option_name
            self.option_menu = tk.OptionMenu(self.pw11, self.option_name_spy_table_dict["option_name_11_"+str(i+1)], *self.std_short_names_list, command=partial(self.change_spy_values,i))
            self.option_menu.config(bg="#056CF2", activebackground="#056CF2", bd=0, fg="white", font=("Helvetica Neue", 10))
            self.option_menu.grid(row=i+2, column=3)
            self.option_menu_spy_table_dict["option_menu_11_"+str(i+1)] = self.option_menu
    
    # Function to change values of known samples printed
    
    def change_spy_values(self,i,option_name):
        for k in range(0, len(self.std_short_names_list)):
            if option_name == self.std_short_names_list[k]:
                self.entry_spy_table_dict["entry_11_"+str(3*i+1)].config(state="normal")
                self.entry_spy_table_dict["entry_11_"+str(3*i+1)].delete("1.0", "end")
                self.entry_spy_table_dict["entry_11_"+str(3*i+1)].insert("1.0", str(self.std_values_file["d18O"].iloc[k]))
                self.entry_spy_table_dict["entry_11_"+str(3*i+1)].config(state="disabled")
                self.entry_spy_table_dict["entry_11_"+str(3*i+2)].config(state="normal")
                self.entry_spy_table_dict["entry_11_"+str(3*i+2)].delete("1.0", "end")
                self.entry_spy_table_dict["entry_11_"+str(3*i+2)].insert("1.0", str(self.std_values_file["dD"].iloc[k]))
                self.entry_spy_table_dict["entry_11_"+str(3*i+2)].config(state="disabled")
                if self.option_protocol.get() == 'van Geldern d17O mode' or self.option_protocol.get()=="Gröning d17O mode":
                    self.entry_spy_table_dict["entry_11_"+str(3*(i+1))].config(state="normal")
                    self.entry_spy_table_dict["entry_11_"+str(3*(i+1))].delete("1.0", "end")
                    self.entry_spy_table_dict["entry_11_"+str(3*(i+1))].insert("1.0", str(self.std_values_file["d17O"].iloc[k]))
                    self.entry_spy_table_dict["entry_11_"+str(3*(i+1))].config(state="disabled")
                break

##################METHODS USED FOR PROCESSING##################################
    
    # Function to process data. Opens the first page of results at the end of processing. 
    
    def processing(self):
        self.error_user_inputs=check_errors.check_errors(self)
        if self.error_user_inputs==1:
            return
        self.init_variables_processing()
        if self.option_protocol.get() == "van Geldern mode":
            self.protocol_type = 0
            outliers_top_lvl=outliers_top_level(self)
            self.idx_std_to_use=outliers_top_lvl.idx_std_to_use
            self.master_window.wait_window(outliers_top_lvl.outliers_check_page)
            self.MC_one = np.ones((self.inj_per_std))
            self.last_injections=MC_calc_VG.create_last_injections(self.result_file_df, self.iso_type_list)
            self.corrected_file_df,self.MCs=MC_calc_VG.wrapper_memory_coefficient_van_geldern(self.iso_type_list, self.MC_one, self.inj_per_std, self.last_injections, self.result_file_df, self.len_std_injections, self.std_nbr,self.idx_std_to_use)
            self.final_value_file_df,self.calibration_param_list,self.calibration_vectors=cal.wrapper_calibration(self.corrected_file_df, self.iso_type_list, self.std_idx_norm, self.std_values, self.inj_per_std, self.result_file_df, self.removed_inj_per_std,self.std_nbr,self.protocol_type)
            self.slope_MC_list, self.p_values_MC_list, self.avg_std_list, self.std_dev_std_list, self.std_col1_list, self.residuals_std, self.std_uncheck, self.spl_results, self.known_sample_results=param_calc.wrapper_parameters_calculation(self.final_value_file_df, self.protocol_type, self.removed_inj_per_std, self.std_nbr, self.inj_per_std, self.iso_type_list, self.is_residuals_results_table, self.is_spy_results_table, self.var_checkbox_std_table_dict, self.std_values, self.removed_inj_per_spl, self.spl_nbr, self.inj_per_spl, self.len_std_injections, self.port_known_samples_list, self.idx_known_sample,self.std_idx_norm)
            self.change_page_result()
        if self.option_protocol.get() == "van Geldern d17O mode":
            self.protocol_type = 1
            outliers_top_lvl=outliers_top_level(self)
            self.idx_std_to_use=outliers_top_lvl.idx_std_to_use
            self.master_window.wait_window(outliers_top_lvl.outliers_check_page)
            self.MC_one = np.ones((self.inj_per_std))
            self.last_injections=MC_calc_VG.create_last_injections(self.result_file_df, self.iso_type_list)
            self.corrected_file_df,self.MCs=MC_calc_VG.wrapper_memory_coefficient_van_geldern_d17O(self.iso_type_list, self.MC_one, self.inj_per_std, self.last_injections, self.result_file_df, self.len_std_injections, self.std_nbr,self.idx_std_to_use)    
            self.final_value_file_df,self.calibration_param_list,self.calibration_vectors=cal.wrapper_calibration(self.corrected_file_df, self.iso_type_list, self.std_idx_norm, self.std_values, self.inj_per_std, self.result_file_df, self.removed_inj_per_std,self.std_nbr,self.protocol_type)
            self.slope_MC_list, self.p_values_MC_list, self.avg_std_list, self.std_dev_std_list, self.std_col1_list, self.residuals_std, self.std_uncheck, self.spl_results, self.known_sample_results=param_calc.wrapper_parameters_calculation(self.final_value_file_df, self.protocol_type, self.removed_inj_per_std, self.std_nbr, self.inj_per_std, self.iso_type_list, self.is_residuals_results_table, self.is_spy_results_table, self.var_checkbox_std_table_dict, self.std_values, self.removed_inj_per_spl, self.spl_nbr, self.inj_per_spl, self.len_std_injections, self.port_known_samples_list, self.idx_known_sample,self.std_idx_norm)
            self.change_page_result()
        if self.option_protocol.get() == "Gröning mode":
            self.protocol_type=2
            self.corrected_file_df,self.single_factor_mean,self.exp_params=MC_calc_G.wrapper_memory_correction_groning_method(self.iso_type_list, self.result_file_df, self.len_std_injections, self.groning_params_array, self.inj_per_std)
            self.final_value_file_df,self.calibration_param_list,self.calibration_vectors=cal.wrapper_calibration(self.corrected_file_df, self.iso_type_list, self.std_idx_norm, self.std_values, self.inj_per_std, self.result_file_df, self.removed_inj_per_std,self.std_nbr,self.protocol_type)
            self.slope_MC_list, self.p_values_MC_list, self.avg_std_list, self.std_dev_std_list, self.std_col1_list, self.residuals_std, self.std_uncheck, self.spl_results, self.known_sample_results=param_calc.wrapper_parameters_calculation(self.final_value_file_df, self.protocol_type, self.removed_inj_per_std, self.std_nbr, self.inj_per_std, self.iso_type_list, self.is_residuals_results_table, self.is_spy_results_table, self.var_checkbox_std_table_dict, self.std_values, self.removed_inj_per_spl, self.spl_nbr, self.inj_per_spl, self.len_std_injections, self.port_known_samples_list, self.idx_known_sample,self.std_idx_norm)
            self.change_page_result()
        if self.option_protocol.get() == "Gröning d17O mode":
            self.protocol_type=3
            self.corrected_file_df,self.single_factor_mean,self.exp_params=MC_calc_G.wrapper_memory_correction_groning_method(self.iso_type_list, self.result_file_df, self.len_std_injections, self.groning_params_array, self.inj_per_std)
            self.final_value_file_df,self.calibration_param_list,self.calibration_vectors=cal.wrapper_calibration(self.corrected_file_df, self.iso_type_list, self.std_idx_norm, self.std_values, self.inj_per_std, self.result_file_df, self.removed_inj_per_std,self.std_nbr,self.protocol_type)
            self.slope_MC_list, self.p_values_MC_list, self.avg_std_list, self.std_dev_std_list, self.std_col1_list, self.residuals_std, self.std_uncheck, self.spl_results, self.known_sample_results=param_calc.wrapper_parameters_calculation(self.final_value_file_df, self.protocol_type, self.removed_inj_per_std, self.std_nbr, self.inj_per_std, self.iso_type_list, self.is_residuals_results_table, self.is_spy_results_table, self.var_checkbox_std_table_dict, self.std_values, self.removed_inj_per_spl, self.spl_nbr, self.inj_per_spl, self.len_std_injections, self.port_known_samples_list, self.idx_known_sample,self.std_idx_norm)
            self.change_page_result()
             
    # Function to set some variables for processing 

    def init_variables_processing(self):
        self.get_index_std_normalisation()
        self.filename = lf.downloading_file(self.option_protocol1, self.entry_3_1)
       
        self.iso_type_list=["d18O","dD"]
        if self.option_protocol.get()=="van Geldern d17O mode" or self.option_protocol.get()=="Gröning d17O mode":
            self.iso_type_list.append("d17O")
        self.iso_nbr=len(self.iso_type_list)
        self.is_residuals_results_table, self.is_spy_results_table = table_res_1.is_spy_and_is_residuals( self.var_checkbox_std_table_dict, self.var_5_1)
        self.read_user_inputs()
        self.result_file_df, self.len_std_injections, self.len_spl_injections = lf.load_csv_file_into_DF(self.filename, self.std_nbr, self.inj_per_std, self.spl_nbr, self.inj_per_spl)
        self.MCs=[]
        self.slope_MC_list=[]
        self.p_values_MC_list=[]
        self.single_factor_mean=[]
        self.exp_params=[]
        length_file_user=self.std_nbr*self.inj_per_std+self.spl_nbr*self.inj_per_spl
        if length_file_user>len(self.result_file_df):
            error=1
            tk.messagebox.showwarning("Warning", "You have filled more injections than what your file actually contains", parent=self.master_window)
            return error
        if length_file_user<len(self.result_file_df):
            result=tk.messagebox.askokcancel("Information", " You have filled less injections than what your file actually contains. \n Do you want to continue ? ")
            if result==False:
                error=1
                return error
    
    # Function that gather the index of standards used to normalise data

    def get_index_std_normalisation(self):
        self.std_idx_norm = []
        for i, j in enumerate(self.var_checkbox_std_table_dict):
            if self.var_checkbox_std_table_dict[j].get() == 1:
                self.std_idx_norm.append(i+1)
    
    # Function to read user inputs
        
    def read_user_inputs(self):
        self.std_nbr=int(self.entry_4_1.get())
        self.inj_per_std=int(self.entry_7_1.get())
        self.removed_inj_per_std=int(self.entry_7_2.get())
        self.spl_nbr=int(self.entry_6_1.get())
        self.inj_per_spl=int(self.entry_6_2.get())
        self.removed_inj_per_spl=int(self.entry_6_3.get())
        self.std_values = np.zeros((self.std_nbr, self.iso_nbr))
        self.operator_id=self.entry_8_1.get()
        self.processor_id=self.entry_8_2.get()
        for i in range(0, self.std_nbr):
            self.std_values[i, 0] = float(self.entry_std_table_dict["entry_10_"+str(3*i+1)].get("1.0", "end"))
            self.std_values[i, 1] = float(self.entry_std_table_dict["entry_10_"+str(3*i+2)].get("1.0", "end"))
            if self.iso_nbr == 3:
                self.std_values[i, 2] = float(self.entry_std_table_dict["entry_10_"+str(3*(i+1))].get("1.0", "end"))
        self.port_known_samples_list = []
        self.idx_known_sample = []
        self.known_values=[]
        if self.var_5_1.get() == 1:
            self.known_values = np.zeros((self.known_sample_nbr, self.iso_nbr))
            for j in self.option_port_spy_table_dict:
                self.port_known_samples_list.append(self.option_port_spy_table_dict[j].get())
            for i in range(0, self.known_sample_nbr):
                self.known_values[i, 0] = float(self.entry_spy_table_dict["entry_11_"+str(3*i+1)].get("1.0", "end"))
                self.known_values[i, 1] = float(self.entry_spy_table_dict["entry_11_"+str(3*i+2)].get("1.0", "end"))
                if self.iso_nbr == 3:
                    self.known_values[i, 2] = float(self.entry_spy_table_dict["entry_11_"+str(3*(i+1))].get("1.0", "end"))
            self.get_lines_known_samples() 
        if self.option_protocol.get() == "Gröning mode" or self.option_protocol.get() == "Gröning d17O mode":
            self.groning_params_array=np.zeros((3,self.iso_nbr))
            for i in range(0,3):
                self.groning_params_array[i,0]=float(self.groning_params["entry_9_2_"+str(i+2)].get("1.0", "end"))
                self.groning_params_array[i,1]=float(self.groning_params["entry_9_3_"+str(i+2)].get("1.0", "end"))
                if self.iso_nbr==3:
                    self.groning_params_array[i,2]=float(self.groning_params["entry_9_4_"+str(i+2)].get("1.0", "end"))
        else:
            self.groning_params_array=[]
            
    # Function to get lines of the known samples

    def get_lines_known_samples(self):
        for i in range(0, len(self.result_file_df)):
            if any(self.result_file_df["Port"].iloc[i] == port_known_sample for port_known_sample in self.port_known_samples_list):
                self.idx_known_sample.append(i)  
                
    # Function to open the first page of results 
    
    def change_page_result(self):
        self.open_page_results_1=page_result_1(self)
    
    
class evaluate_parameters_page():
    
    
    def __init__(self,Main_Window):
        
        # import the main window class and all the variables contained in it 
        
        self.main_window=Main_Window
        
        # check if evaluation of Groning's parameters can be done
        
        self.error=check_errors.check_errors(self.main_window)
        if self.error==1:
            return
        
        # Window definition
        
        self.page_evaluation_groning_params= tk.Toplevel(self.main_window.master_window)
        self.page_evaluation_groning_params.state('zoomed')
        self.page_evaluation_groning_params.configure(bg="#BEE7E8") 
        self.page_evaluation_groning_params.title("Evaluation Parameters")
        self.message_text_eval = tk.Message(master=self.page_evaluation_groning_params, text="Evaluation of the Gröning parameters",font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
        self.message_text_eval.place(relx=0.5, rely=0.05, anchor="center")
        self.pw_eval=tk.PanedWindow(self.page_evaluation_groning_params,orient="vertical", bg="#056CF2",relief="solid")
        self.pw_eval.grid(row=4, column=6)
        self.pw_eval.place(relx=0.8, rely=0.5, anchor="center")
        self.label_eval_4 = tk.Label(self.pw_eval, text="\u03B418O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_eval_4.grid(row=1, column=3, sticky="NSEW")
        self.label_eval_5 = tk.Label(self.pw_eval, text="\u03B4D", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_eval_5.grid(row=1, column=4, sticky="NSEW")
        if self.main_window.option_protocol.get()=="Gröning d17O mode":
            self.label_eval_6=tk.Label(self.pw_eval, text="\u03B417O", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
            self.label_eval_6.grid(row=1, column=5, sticky="NSEW")
        self.label_eval_1=tk.Label(self.pw_eval, text="\u03B1", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_eval_1.grid(row=2,column=2)
        self.label_eval_2=tk.Label(self.pw_eval, text="\u03B2", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_eval_2.grid(row=3,column=2)
        self.label_eval_3=tk.Label(self.pw_eval, text="balance", bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        self.label_eval_3.grid(row=4,column=2)
        self.groning_params_eval={}
        for i in range(0,3):
            self.entry=tk.Entry(self.pw_eval, width=12)
            self.entry.grid(row=i+2, column=3, sticky="NSEW")
            self.groning_params_eval["entry_eval_2_"+str(i+2)] = self.entry
            self.groning_params_eval["entry_eval_2_"+str(i+2)].delete(0, "end")
            self.groning_params_eval["entry_eval_2_"+str(i+2)].insert(0, self.main_window.groning_params["entry_9_2_"+str(i+2)].get("1.0","end"))
            self.entry=tk.Entry(self.pw_eval,width=12)
            self.entry.grid(row=i+2, column=4, sticky="NSEW")
            self.groning_params_eval["entry_eval_3_"+str(i+2)] = self.entry
            self.groning_params_eval["entry_eval_3_"+str(i+2)].delete(0, "end")
            self.groning_params_eval["entry_eval_3_"+str(i+2)].insert(0, self.main_window.groning_params["entry_9_3_"+str(i+2)].get("1.0","end"))
            if self.main_window.option_protocol.get()=="Gröning d17O mode":
                self.entry=tk.Entry(self.pw_eval, width=12)
                self.entry.grid(row=i+2, column=5, sticky="NSEW")
                self.groning_params_eval["entry_eval_4_"+str(i+2)] = self.entry
                self.groning_params_eval["entry_eval_4_"+str(i+2)].delete(0, "end")
                self.groning_params_eval["entry_eval_4_"+str(i+2)].insert(0, self.main_window.groning_params["entry_9_4_"+str(i+2)].get("1.0","end"))
        self.Button_run_eval=tk.Button(self.page_evaluation_groning_params,text="Run \n Evaluation",command=self.run, font=("Helvetica Neue", 15), relief="raised", bg="#056CF2", fg="white")
        self.Button_run_eval.place(relx=0.8, rely=0.8,anchor="center")
        self.pw_eval_2=tk.PanedWindow(self.page_evaluation_groning_params,orient="vertical")
        self.pw_eval_2.grid(row=1,column=2)
        self.pw_eval_2.place(relx=0.8,rely=0.2,anchor="center")
        self.label_eval_2_1=tk.Label(self.pw_eval_2,text="Name of the new set of parameters :",  bg="#327D94",fg="white",font=("Helvetica Neue", 13))
        self.label_eval_2_1.grid(row=1,column=1)
        self.text_2_1=tk.Text(self.pw_eval_2,height=1, width=10)
        self.text_2_1.grid(row=1,column=2)
        self.save_button_eval_params=tk.Button(self.page_evaluation_groning_params,text="Save \n Parameters", font=("Helvetica Neue", 15), relief="raised", bg="#056CF2", fg="white",command=self.save_groning_params)
        self.save_button_eval_params.place(relx=0.8,rely=0.3,anchor="center")
        
    # Evaluation of the groning's parameters 
     
    def run(self):
        for i, j in enumerate(self.groning_params_eval):
            if self.groning_params_eval[j].get()=="":
                tk.messagebox.showerror("Error","Error : One of the Entry is blank, please fill it",parent=self.page_evaluation_groning_params)
                return
        if self.main_window.option_protocol.get() == "Gröning mode" or self.main_window.option_protocol.get() == "Gröning d17O mode":
            self.iso_nbr=2
            if self.main_window.option_protocol.get()=="Gröning d17O mode":
                self.iso_nbr=3
            self.groning_params_array_eval=np.zeros((3,self.iso_nbr))
            for i in range(0,3):
                self.groning_params_array_eval[i,0]=float(self.groning_params_eval["entry_eval_2_"+str(i+2)].get())
                self.groning_params_array_eval[i,1]=float(self.groning_params_eval["entry_eval_3_"+str(i+2)].get())
                if self.iso_nbr==3:
                    self.groning_params_array_eval[i,2]=float(self.groning_params_eval["entry_eval_4_"+str(i+2)].get())  
        self.processing_eval_groning()
        
    # Function to process the data with groning parameters but it doesn't load the first page of results 
    
    def processing_eval_groning(self):
        self.main_window.init_variables_processing()
        if self.main_window.option_protocol.get() == "Gröning mode":
            self.protocol_type=2
        if self.main_window.option_protocol.get() == "Gröning d17O mode":
            self.protocol_type=3   
        self.corrected_file_df,self.single_factor_mean,self.exp_params=MC_calc_G.wrapper_memory_correction_groning_method(self.main_window.iso_type_list, self.main_window.result_file_df, self.main_window.len_std_injections, self.groning_params_array_eval, self.main_window.inj_per_std)
        self.final_value_file_df,self.calibration_param_list,self.calibration_vectors=cal.wrapper_calibration(self.corrected_file_df, self.main_window.iso_type_list, self.main_window.std_idx_norm, self.main_window.std_values, self.main_window.inj_per_std, self.main_window.result_file_df, self.main_window.removed_inj_per_std,self.main_window.std_nbr,self.protocol_type)
        self.slope_MC_list, self.p_values_MC_list, self.avg_std_list, self.std_dev_std_list, self.std_col1_list, self.residuals_std, self.std_uncheck, self.spl_results, self.known_sample_results=param_calc.wrapper_parameters_calculation(self.final_value_file_df, self.protocol_type, self.main_window.removed_inj_per_std, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.iso_type_list,self.main_window.is_residuals_results_table, self.main_window.is_spy_results_table, self.main_window.var_checkbox_std_table_dict, self.main_window.std_values, self.main_window.removed_inj_per_spl, self.main_window.spl_nbr, self.main_window.inj_per_spl, self.main_window.len_std_injections, self.main_window.port_known_samples_list, self.main_window.idx_known_sample,self.main_window.std_idx_norm)
        self.list_plots = plots.create_list_plots(self.main_window.std_nbr, self.protocol_type,self.main_window.iso_type_list)
        self.fig, ax = plots.creation_all_plots(self.list_plots, self.corrected_file_df,self.main_window.iso_type_list, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.option_name_std_table_dict, self.calibration_vectors, self.calibration_param_list)
        self.canvas = plots.all_plots_canvas_creator(self.fig,  self.page_evaluation_groning_params)
   
    # Function to save groning parameters into the file
    
    def save_groning_params(self):
        if self.text_2_1.get("1.0","end-1c")=="":
            tk.messagebox.showwarning("Warning","Please put a name for this new set of parameters")
            return
        for i in range(0,len(self.main_window.instruments_names_list)):
            if self.text_2_1.get("1.0","end-1c")==self.main_window.instruments_names_list[i]:
                tk.messagebox.showwarning("Warning","Name already used",parent=self.page_evaluation_groning_params)
                return
        try:
            self.groning_params_array_eval
        except AttributeError:
            tk.messagebox.showerror("Error","You need to run at least once the evaluation of the parameters ",parent=self.page_evaluation_groning_params)
            return
        list_to_save=[self.text_2_1.get("1.0","end-1c")]
        for j in range(0,self.iso_nbr):
            for i in range(0,3):
                list_to_save.append(self.groning_params_array_eval[i,j])
        if self.iso_nbr==2:
            for i in range(0,3):
                list_to_save.append(np.nan)
        self.main_window.groning_params_file.loc[-1]=list_to_save
        self.main_window.groning_params_file.to_csv("./files/groning_exp_parameters.csv",sep=",",index=False)
        tk.messagebox.showinfo("Info", "Parameters saved",parent=self.page_evaluation_groning_params)
        
        
class outliers_top_level():
    def __init__(self,Main_Window):
      
        # import the main window class and all the variables contained in it 
        
        self.main_window=Main_Window
        
        # Window definition
        
        self.outliers_check_page=tk.Toplevel(self.main_window.master_window)
        self.outliers_check_page.wm_state('zoomed')
        self.outliers_check_page.configure(bg="#E8B300")
        self.outliers_check_page.title("Check processing")
        plots.memory_correction_parameters_plot(self.main_window.protocol_type, self.main_window.iso_type_list, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.result_file_df, self.outliers_check_page, self.main_window.option_name_std_table_dict)
        self.message_text_outliers = tk.Message(master=self.outliers_check_page, text="Plots of the standards", font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
        self.message_text_outliers.place(relx=0.3, rely=0.1, anchor="center")
        self.pw_outliers = tk.PanedWindow(self.outliers_check_page, relief="solid")
        self.pw_outliers.grid(row=1, column=2)
        self.label_outliers = tk.Label(self.pw_outliers, text="File : ", font=("Helvetica Neue", 14))
        self.label_outliers.grid(row=1, column=1)
        self.message_text_filename = tk.Entry(self.pw_outliers, font=("Helvetica Neue", 14), width=40, disabledforeground="black")
        self.message_text_filename.insert(0, self.main_window.filename)
        self.message_text_filename.configure(state="disabled")
        self.message_text_filename.grid(row=1, column=2, padx=5, pady=5)
        self.pw_outliers.place(relx=0.55, rely=0.03, anchor="center")
        self.pw2_outliers=tk.PanedWindow(self.outliers_check_page,relief="solid")
        self.pw2_outliers.grid(row=self.main_window.std_nbr+3,column=2)
        self.label_outliers_1_1=tk.Label(self.pw2_outliers,text="Are there outlayers ? ")
        self.label_outliers_1_1.grid(row=1,column=1)
        self.option_list_outliers=["No","Only one Injection","More than one Injection"]
        self.option_values_outliers=tk.StringVar()
        self.option_values_outliers.set("No")
        self.option_menu_outliers=tk.OptionMenu(self.pw2_outliers,self.option_values_outliers,*self.option_list_outliers,command=lambda _: self.change_table_outliers_page())
        self.option_menu_outliers.grid(row=1,column=2)
        self.pw2_outliers.place(relx=0.75,rely=0.4,anchor="center")
        self.continue_button=tk.Button(self.outliers_check_page, text="Next page", font=("Helvetica Neue", 18), relief="raised",command=self.change_outliers_page)
        self.continue_button.place(relx=0.77, rely=0.1, anchor="center")
        self.idx_std_to_use=np.arange(self.main_window.std_nbr*self.main_window.inj_per_std)
        
        
    # Function to change table outliers page 

    def change_table_outliers_page(self):
        if self.option_values_outliers.get()=="Only one Injection":
            try: 
                for i in range(1, self.main_window.std_nbr):
                    self.label_outliers_dict["label_"+str(i)].destroy()
                    self.checkbox_outliers_dict["checkbox_"+str(i)].destroy()
            except AttributeError:
                self.first_time=1
            self.label_outliers_1_1=tk.Label(self.pw2_outliers,text="Please indicate the problematic standard : ")
            self.label_outliers_1_1.grid(row=3,column=1)
            self.label_outliers_1_2=tk.Label(self.pw2_outliers,text="Please indicate the problematic injection :")
            self.label_outliers_1_2.grid(row=4,column=1)
            self.entry_outliers_2_1=tk.Entry(self.pw2_outliers)
            self.entry_outliers_2_1.grid(row=3,column=2,sticky="NSEW")
            self.entry_outliers_2_2=tk.Entry(self.pw2_outliers)
            self.entry_outliers_2_2.grid(row=4,column=2,sticky="NSEW")
        if self.option_values_outliers.get()=="More than one Injection":
            try: 
                self.label_outliers_1_1.destroy()
                self.label_outliers_1_2.destroy()
                self.entry_outliers_2_1.destroy()
                self.entry_outliers_2_2.destroy()
            except AttributeError: 
                self.first_time=1
            self.label_outliers_dict={}
            self.var_outliers_dict={}
            self.checkbox_outliers_dict={}
            for i in range(1,self.main_window.std_nbr):
                self.label = tk.Label(self.pw2_outliers, text='STD ' + str(i+1)+' : ', font=("Helvetica Neue", 11))
                self.label.grid(row=i+5, column=1, sticky='NSEW')
                self.label_outliers_dict["label_"+str(i)] = self.label
                self.var = tk.IntVar(value=0)
                self.var_outliers_dict["var_"+str(i)] = self.var
                self.checkbox = tk.Checkbutton(self.pw2_outliers, variable=self.var_outliers_dict["var_"+str(i)])
                self.checkbox.grid(row=i+5, column=2)
                self.checkbox_outliers_dict["checkbox_"+str(i)] = self.checkbox
        if self.option_values_outliers.get()=="No":
            try: 
                self.label_outliers_1_1.destroy()
                self.label_outliers_1_2.destroy()
                self.entry_outliers_2_1.destroy()
                self.entry_outliers_2_2.destroy()
            except AttributeError: 
                self.first_time=1
            try: 
                for i in range(1, self.main_window.std_nbr):
                    self.label_outliers_dict["label_"+str(i)].destroy()
                    self.checkbox_outliers_dict["checkbox_"+str(i)].destroy()
            except AttributeError:
                self.first_time=1
                
    # Function to change the outliers window to first result page 

    def change_outliers_page(self):        
        if self.option_values_outliers.get()=="Only one Injection":
            if self.entry_outliers_2_1.get().isdigit() == False:
                tk.messagebox.showwarning("Warning", "Not a Number inserted")
                return
            if self.entry_outliers_2_1.get().isdigit() == True:
                if int(self.entry_outliers_2_1.get())<=0:
                    tk.messagebox.showwarning("Warning", "Negative value inserted")
                    return
                if int(self.entry_outliers_2_1.get())==1:
                    tk.messagebox.showwarning("Warning", "STD 1 is not used in memory correction")
                    return
            if self.entry_outliers_2_2.get().isdigit() == False:
                tk.messagebox.showwarning("Warning", "Not a Number inserted")
                return
            if self.entry_outliers_2_2.get().isdigit() == True:
                if int(self.entry_outliers_2_2.get())<=0:
                    tk.messagebox.showwarning("Warning", "Negative value inserted")
                    return
            self.injection_to_remove=(int(self.entry_outliers_2_1.get())-1)*self.main_window.inj_per_std+int(self.entry_outliers_2_2.get())-1
            self.idx_std_to_use=np.delete(self.idx_std_to_use,self.injection_to_remove)
        if self.option_values_outliers.get()=="More than one Injection":
            self.start_inj_to_remove=[]
            for i, j in enumerate(self.var_outliers_dict):
                if self.var_outliers_dict[j].get() == 1:
                    self.start_inj_to_remove.append(self.main_window.inj_per_std*(i+1))
            self.injection_to_remove=[]
            for i in range(0,len(self.start_inj_to_remove)):
                self.std_inj_to_remove=np.arange(self.start_inj_to_remove[i],self.start_inj_to_remove[i]+self.main_window.inj_per_std)
                for j in range(0,self.main_window.inj_per_std):
                    self.injection_to_remove.append(self.std_inj_to_remove[j])
            self.idx_std_to_use=np.delete(self.idx_std_to_use,self.injection_to_remove)
        self.outliers_check_page.destroy()
        
class page_result_1():
    def __init__(self,Main_Window):
        
        # import the main window class and all the variables contained in it 
        
        self.main_window=Main_Window
        
        # Window creation 
        
        self.page_results_1 = tk.Toplevel(self.main_window.master_window)
        self.page_results_1.state('zoomed')
        self.page_results_1.configure(bg="#E8B300")
        self.page_results_1.title("Results Plots 1")
        self.pw_results = tk.PanedWindow(self.page_results_1, relief="solid")
        self.pw_results.grid(row=1, column=2)
        self.pw_results.place(relx=0.55, rely=0.03, anchor="center")
        self.label_page_results_1 = tk.Label(self.pw_results, text="File : ",font=("Helvetica Neue", 14))
        self.label_page_results_1.grid(row=1, column=1)
        self.message_text_filename = tk.Entry(self.pw_results, font=("Helvetica Neue", 14), width=40, disabledforeground="black")
        self.message_text_filename.insert(0, self.main_window.filename)
        self.message_text_filename.configure(state="disabled")
        self.message_text_filename.grid(row=1, column=2, padx=5, pady=5)
        self.message_text_page_results_1 = tk.Message(master=self.page_results_1, text="Plots of the results", font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
        self.message_text_page_results_1.place(relx=0.3, rely=0.1, anchor="center")
        self.list_plots = plots.create_list_plots(self.main_window.std_nbr, self.main_window.protocol_type,self.main_window.iso_type_list)
        self.fig, self.ax = plots.creation_all_plots(self.list_plots, self.main_window.corrected_file_df, self.main_window.iso_type_list, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.option_name_std_table_dict, self.main_window.calibration_vectors, self.main_window.calibration_param_list)
        self.canvas = plots.all_plots_canvas_creator(self.fig, self.page_results_1)
        table_res_1.create_calibration_results_table(self.main_window.calibration_param_list, self.page_results_1, self.main_window.protocol_type, self.main_window.is_residuals_results_table, self.main_window.is_spy_results_table)
        table_res_1.create_MC_results_table(self.main_window.std_col1_list,self.main_window.protocol_type,self.page_results_1,self.main_window.is_residuals_results_table,self.main_window.is_spy_results_table, self.main_window.slope_MC_list, self.main_window.p_values_MC_list, self.main_window.iso_type_list, self.main_window.single_factor_mean, self.main_window.exp_params)
        table_res_1.create_standards_results(self.main_window.avg_std_list, self.main_window.std_dev_std_list, self.main_window.std_col1_list, self.main_window.protocol_type, self.page_results_1, self.main_window.is_residuals_results_table, self.main_window.is_spy_results_table)       
        table_res_1.create_residuals_standard_results_table(self.main_window.residuals_std, self.main_window.std_values, self.main_window.std_uncheck, self.page_results_1, self.main_window.protocol_type, self.main_window.is_residuals_results_table,self.main_window. is_spy_results_table)
        table_res_1.create_known_sample_results_table(self.main_window.known_sample_results, self.page_results_1, self.main_window.known_values, self.main_window.protocol_type, self.main_window.is_residuals_results_table, self.main_window.is_spy_results_table)
        self.option_plots = tk.StringVar(value="All plots")
        self.optionmenu_plots = tk.OptionMenu(self.page_results_1, self.option_plots, *self.list_plots,command=lambda _: self.change_plots())         
        self.optionmenu_plots.configure(font=("Helvetica Neue", 11))
        self.optionmenu_plots["menu"].configure(font=("Helvetica Neue", 11))
        self.optionmenu_plots.place(rely=0.1, relx=0.5, anchor="center")
        self.next_page_btn = tk.Button(self.page_results_1, text="Next page", font=("Helvetica Neue", 18), relief="raised", command=self.change_page_result_2)
        self.next_page_btn.place(relx=0.77, rely=0.1, anchor="center")
        
    # Function to change plots 
    
    def change_plots(self):
        self.canvas.get_tk_widget().destroy()
        try:
            self.canvas1.get_tk_widget().destroy()
        except AttributeError:
            self.doesnt_exits=1
        try:
            self.canvas2.get_tk_widget().destroy()
        except AttributeError:
            self.doesnt_exits=1
        if self.option_plots.get() == "All plots":
            self.figure1,self.ax1=plots.creation_all_plots(self.list_plots,  self.main_window.corrected_file_df, self.main_window.iso_type_list, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.option_name_std_table_dict, self.main_window.calibration_vectors, self.main_window.calibration_param_list)
            self.canvas = plots.all_plots_canvas_creator(self.figure1, self.page_results_1)
        else:
            self.figure1,self.figure2 = plots.create_two_figures(self.list_plots, self.option_plots, self.main_window.corrected_file_df, self.main_window.iso_type_list, self.main_window.std_nbr, self.main_window.inj_per_std, self.main_window.option_name_std_table_dict, self.main_window.calibration_vectors, self.main_window.calibration_param_list)
            self.canvas1, self.canvas2 = plots.other_plots_canvas_creator(self.figure1, self.figure2, self.page_results_1)
    
    # Function to open the second page of results 
    
    def change_page_result_2(self):
        self.open_page_result_2=page_result_2(self)
            
class page_result_2():
    def __init__(self,page_result_1):
        
        # import the main window class and all the variables contained in it 
        
        self.main_window=page_result_1.main_window
        
        # Window definition 
        
        self.page_results_2 = tk.Toplevel(self.main_window.master_window)
        self.page_results_2.state('zoomed')
        self.page_results_2.configure(bg="#E8B300")
        self.page_results_2.title("Results Plots 2")
        self.pw_results_2 = tk.PanedWindow(self.page_results_2, relief="solid")
        self.pw_results_2.grid(row=1, column=2)
        self.label_page_results_2 = tk.Label(self.pw_results_2, text="File : ", font=("Helvetica Neue", 14))
        self.label_page_results_2.grid(row=1, column=1)
        self.message_text_filename = tk.Entry(self.pw_results_2, font=("Helvetica Neue", 14), width=40, disabledforeground="black")
        self.message_text_filename.insert(0, self.main_window.filename)
        self.message_text_filename.configure(state="disabled")
        self.message_text_filename.grid(row=1, column=2, padx=5, pady=5)
        self.pw_results_2.place(relx=0.55, rely=0.05, anchor="center")
        self.message_text_page_results_2 = tk.Message(master=self.page_results_2, text="Plots of the results",font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
        self.message_text_page_results_2.place(relx=0.3, rely=0.05, anchor="center")
        self.fig, self.ax = plots.make_raws_plots(self.main_window.protocol_type, self.main_window.result_file_df)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.page_results_2)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.5)
        table_res2.create_samples_results_table(self.page_results_2, self.main_window.spl_results, self.main_window.protocol_type)
        self.saving_button = tk.Button(self.page_results_2, text="Save data", font=("Helvetica Neue", 18), relief="raised",command=self.saving_folder_window)
        self.saving_button.place(relx=0.74, rely=0.02)
        
        
    # Verify if a value has not been corrected (due to the lack of at least one of injection in the sample)    
    
    def check_correction_flag(self):
        self.replaced_values=0
        i=0
        while self.replaced_values==0 and i<self.main_window.final_value_file_df.index[-1]:
            if self.main_window.final_value_file_df["Correction Flag"].iloc[i]==2:
                self.replaced_values=1
            i=i+1
        if self.replaced_values==1:
            tk.messagebox.showwarning("Warning", "There is at least one sample which has not been corrected ! Check the Correction Flag in the final file and look for lines with 2 in this column", parent=self.page_results_2)    
    
    # Function to save the data. Opens a messagebox to select where to save the data. 
    
    def saving_folder_window(self):
        self.saving_place=""
        self.directory_path=""
        self.saved=0
        self.where_to_save=tk.Toplevel(self.page_results_2)
        where_to_save_width = 330
        where_to_save_height = 110
        x = int(int(self.where_to_save.winfo_screenwidth()/2) - int(where_to_save_width/2))
        y = int(int(self.where_to_save.winfo_screenheight()/2) - int(where_to_save_height/2))
        self.where_to_save.geometry(f"{where_to_save_width}x{where_to_save_height}+{x}+{y}")
        self.where_to_save.title("location of save")
        self.frame_1=tk.Frame(self.where_to_save,bg="white",height=70,width=330)
        self.frame_1.place(relx=0,rely=0)
        img=PIL.Image.open("GUI_images/question_mark.png")
        self.img1=img.resize((40, 40))
        self.image_1=PIL.ImageTk.PhotoImage(self.img1)
        self.label_1=tk.Label(self.where_to_save, image = self.image_1,height=50,width=50,bg="white")
        self.label_1.image=self.image_1 # to keep a reference see https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
        self.label_1.place(relx=0.05,rely=0.1)
        self.label_2=tk.Label(self.where_to_save, text="Where do you want to save your results ?",font=("Calibri", 10),bg="white")
        self.label_2.place(relx=0.25, rely=0.25)
        self.local_saving=tk.Button(self.where_to_save,text="Local folder",bg="white",font=("Calibri", 9),command=self.set_local)
        self.local_saving.place(relx=0.3,rely=0.7)
        self.drive_saving=tk.Button(self.where_to_save,text="Google Drive folder",bg="white",font=("Calibri", 9),command=self.set_drive)
        self.drive_saving.place(relx=0.6,rely=0.7)
        self.where_to_save.transient(self.page_results_2)
        self.where_to_save.grab_set()
        self.page_results_2.wait_window(self.where_to_save)
        sr.save_all_files(self)
        
    def set_local(self):
        self.saving_place="local"
        self.where_to_save.destroy()
        
    def set_drive(self):
        self.saving_place="drive"
        self.where_to_save.destroy()
        
        
        
if __name__=="__main__":
    App=Main_Window()
         