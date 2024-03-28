# -*- coding: utf-8 -*-
"""
Created on Sunday May 21 2023

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

import tkinter as tk 
from pathlib import Path, PurePath
import os
import Initialisation

config_dict=Initialisation.read_config_file()

# Function to check if there is format errors in the input from user

def check_errors(Main_window):
    error=0
    Main_window.std_nbr = Main_window.entry_4_1.get()
    if Main_window.std_nbr.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "Please enter a number of standards  !",parent=Main_window.master_window)
        return error
    Main_window.std_nbr = int(Main_window.std_nbr)
    if Main_window.std_nbr <= 0:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a negative value in the number of standard ! ",parent=Main_window.master_window)
        return error
    Main_window.inj_per_std = Main_window.entry_7_1.get()
    if Main_window.inj_per_std.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a non-authorized value in the number of injection per standard !",parent=Main_window.master_window)
        return error
    Main_window.inj_per_std = int(Main_window.inj_per_std)
    if Main_window.inj_per_std <= 0:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a negative value in the number of injection per standard ! ",parent=Main_window.master_window)
        return error 
    Main_window.removed_inj_per_std = Main_window.entry_7_2.get()
    if Main_window.removed_inj_per_std.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a non-authorized value in the number of removed injection per standard !",parent=Main_window.master_window)
        return error
    Main_window.removed_inj_per_std = int(Main_window.removed_inj_per_std)
    if Main_window.removed_inj_per_std < 0:
        error=1
        tk.messagebox.showwarning( "Warning", "You entered a negative value in the number of removed injection per standard !",parent=Main_window.master_window)
        return error
    Main_window.spl_nbr = Main_window.entry_6_1.get()
    if Main_window.spl_nbr.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a non-authorized value in the number of sample !",parent=Main_window.master_window)
        return error
    Main_window.spl_nbr = int(Main_window.spl_nbr)
    if Main_window.spl_nbr <= 0:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a negative value in the number of sample ! ",parent=Main_window.master_window)
        return error
    Main_window.inj_per_spl = Main_window.entry_6_2.get()
    if Main_window.inj_per_spl.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a non-authorized value in the number of injection per sample ! ",parent=Main_window.master_window)
        return error 
    Main_window.inj_per_spl = int(Main_window.inj_per_spl)
    if Main_window.inj_per_spl <= 0:
        error = 1
        tk.messagebox.showwarning("Warning", "You entered a negative value in the number of injection per sample ! ",parent=Main_window.master_window)
        return error
    Main_window.removed_inj_per_spl = Main_window.entry_6_3.get()
    if Main_window.removed_inj_per_spl.isdigit() == False:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a non-authorized value in the number of removed injection per sample !",parent=Main_window.master_window)
        return error
    Main_window.removed_inj_per_spl = int(Main_window.removed_inj_per_spl)
    if Main_window.removed_inj_per_spl < 0:
        error=1
        tk.messagebox.showwarning("Warning", "You entered a negative value in the number of removed injection per sample ! ",parent=Main_window.master_window)
        return error
    if Main_window.removed_inj_per_spl>=Main_window.inj_per_spl:
        error=1
        tk.messagebox.showwarning("Warning","You can not remove more than you inject :) ",parent=Main_window.master_window)
        return error
    if Main_window.removed_inj_per_std>=Main_window.inj_per_std:
        error=1
        tk.messagebox.showwarning("Warning","You can not remove more than you inject :) ",parent=Main_window.master_window)
        return error
    if Main_window.var_5_1.get()==1:
        if Main_window.entry_5_1.get().isdigit()==False: 
            error=1
            tk.messagebox.showwarning("Warning", "Please enter a number of spy samples !",parent=Main_window.master_window)
            return error
        if int(Main_window.entry_5_1.get()) <= 0:
            error=1
            tk.messagebox.showwarning("Warning", "You entered a negative value in the number of standard ! ",parent=Main_window.master_window)
            return error
        for i in Main_window.option_name_spy_table_dict:
            if Main_window.option_name_spy_table_dict[i].get()=="Select STD":
                error=1
                tk.messagebox.showwarning("Warning", "You haven't filled a known sample in the known sample table ",parent=Main_window.master_window)
                return error
    if Main_window.entry_3_1.get()=="":
        error=1
        tk.messagebox.showwarning("Warning", "You haven't filled a filename ",parent=Main_window.master_window)
        return error
    for i in Main_window.option_name_std_table_dict:
        if Main_window.option_name_std_table_dict[i].get()=="Select STD":
            error=1
            tk.messagebox.showwarning("Warning", "You haven't filled a standard in the standard table ",parent=Main_window.master_window)
            return error
    if Main_window.option_protocol.get()=="Gröning_mode" or Main_window.option_protocol.get()=="Gröning_d17O_mode":
        if Main_window.option_name_9.get()=="INSTRUMENT NAME":
            error=1
            tk.messagebox.showwarning("Warning", "You forgot to fill parameters for the exponential correction ",parent=Main_window.master_window)
            return error
    
def set_working_directory():
    path_file=Path(__file__).absolute()
    path_folder=path_file.parent
    os.chdir(path_folder)
    
def check_errors_batch_processing(Main_window): 
    error=0
    if config_dict["batch_processing_mode"] in ["Automatic","Manual"]==False:
        tk.messagebox.showwarning("Warning","invalid batch processing mode, please check the configuration file",parent=Main_window.master_window)
        error=1
        return error
    if os.path.isdir(Path(config_dict["directory_input_files"]))!=True or os.path.isdir(Path(config_dict["directory_saving_files"]))!=True :
        tk.messagebox.showwarning("Warning", "invalid path for files",parent=Main_window.master_window)
        error=1
        return error
    if config_dict["batch_processing_mode"]=="Automatic":
        if os.path.isdir(Path(config_dict["directory_saving_figures"]))!=True:
            tk.messagebox.showwarning("Warning","invalid path for figures",parent=Main_window.master_window)
            error=1
            return error