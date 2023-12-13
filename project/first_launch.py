# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:17:23 2023

@author: Utilisateur
"""

import os 
from pathlib import Path, PurePath
import tkinter as tk
from tkinter import filedialog
import sys 

def find_path():
    file_found=0
    for root, dirs, files in os.walk("."):
        for name in files:
            if name == "first_launch.py":
                file_found=1
                #return os.path.abspath(root)
    if file_found==0:
        for root, dirs, files in os.walk(".."):
            for name in files:
                if name == "first_launch.py":
                    file_found=1
                    #return os.path.abspath(root)
    file_found=0
    if file_found==0:
        gui_win = tk.Tk()
        gui_win.withdraw()
        gui_win.attributes("-topmost", True)
        tk.messagebox.showinfo(parent=gui_win,title="Unable to find CALWIC folder",message= "Unable to find automatically the CALWIC folder, will ask you to indicate it manually, please select the CALWIC-main folder or you might have issues later")
        a=filedialog.askdirectory(parent=gui_win)
        for root, dirs, files in os.walk(a):
            for name in files:
                if name == "first_launch.py":
                    file_found=1
                    return root
    tk.messagebox.showinfo(title="Unable to find CALWIC folder manually", message="Unable to find CALWIC folder manually, quitting...")
    sys.exit()

def create_directory(root):
    root=Path(root)
    folder_path=root.parent
    folder_path=folder_path.parent
    folder_path=PurePath(folder_path,Path("CALWIC_files/"))
    try:
        os.mkdir(folder_path)
        return folder_path
    except FileExistsError:
        return folder_path
    except PermissionError:
        tk.messagebox.showwarning(title="Permission denied", message="Permission has been denied, the folder couldn't been created check your authorisations")

def create_file_already_treated_file(folder_path):
    already_treated_filename="already_treated_files.txt"
    Path(str(folder_path)+"/"+already_treated_filename).touch(exist_ok=True)
    return

root=find_path()
folder_path=create_directory(root)
create_file_already_treated_file(folder_path)