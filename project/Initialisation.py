# -*- coding: utf-8 -*-
"""
Created on Monday July 18 2022

@author: Baptiste Bordet, master thesis at GFI (Bergen) and 
University of Iceland.
"""

#import of modules 

import os 
import tkinter as tk 

# Function that supress tocken.pickle (to refresh the connexion to the drive) 

def tocken_supression():
    a=os.listdir()
    for file in a:
        if file=="token.pickle":
            os.remove("token.pickle")
    return
#tocken_supression()

# Function that get the screen resolution 

def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.
    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    root = tk.Tk()
    root.update_idletasks()
    root.state('zoomed')
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.destroy()
    return geometry