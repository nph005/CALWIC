# -*- coding: utf-8 -*-
"""
Created on Thursday 2nd November 2023

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses

"""


import re
from pathlib import Path

# Function to read configuration file and put in a dict 

def read_config_file():   
    filename=Path("./files/configuration_CALWIC.txt")
    dictionary =  {}
    with open(filename, "r") as f:
        lines=f.readlines()
        lines=lines[6:]
        for line in lines:
            line=re.sub(r"[\n\t\s]*", "",line)
            if line=="":
                continue
            line = line.strip().split("#")
            line=line[0]
            s = line.strip().split("=")
            dictionary[s[0]] = s[1]
    return dictionary

## Function to supress tocken.pickle (to refresh the connexion to google drive) 

# def tocken_supression():
#     a=os.listdir()
#     for file in a:
#         if file=="token.pickle":
#             os.remove("token.pickle")
#     return
# #tocken_supression()

# # Function to get the screen resolution 

# def get_curr_screen_geometry():
#     """
#     Workaround to get the size of the current screen in a multi-screen setup.
#     Returns:
#         geometry (str): The standard Tk geometry string.
#             [width]x[height]+[left]+[top]
#     """
#     root = tk.Tk()
#     root.update_idletasks()
#     root.state('zoomed')
#     root.state('iconic')
#     geometry = root.winfo_geometry()
#     root.destroy()
#     return geometry


