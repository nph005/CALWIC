# -*- coding: utf-8 -*-
"""
Created on Tuesday May 10 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

#imports of packages 

import numpy as np
import pandas as pd
import tkinter as tk
import os
import webbrowser
from tkinter import filedialog
import shutil as stl
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

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
pd.options.mode.chained_assignment = None

global std_short_names_list

std_values_file, std_short_names_list = lf.load_standard_csv_file()

# Function to change values of standards printed

def change_std_values():
    global std_short_names_list, option_protocol, option_name_6_dict
    global entry_6_dict, text_list_6_col4, text_list_6_col5, text_list_6_col6
    if option_protocol.get() == "van Geldern mode" or option_protocol.get()=="Gröning mode":
        for i, j in enumerate(option_name_6_dict):
            for k in range(0, len(std_short_names_list)):
                if option_name_6_dict[j].get() == std_short_names_list[k]:
                    entry_6_dict[text_list_6_col4[i]].config(state="normal")
                    entry_6_dict[text_list_6_col4[i]].delete("1.0", "end")
                    entry_6_dict[text_list_6_col4[i]].insert(
                        "1.0", str(std_values_file["d18O"].iloc[k]))
                    entry_6_dict[text_list_6_col4[i]].config(state="disabled")
                    entry_6_dict[text_list_6_col5[i]].config(state="normal")
                    entry_6_dict[text_list_6_col5[i]].delete("1.0", "end")
                    entry_6_dict[text_list_6_col5[i]].insert(
                        "1.0", str(std_values_file["dD"].iloc[k]))
                    entry_6_dict[text_list_6_col5[i]].config(state="disabled")
    if option_protocol.get() == 'van Geldern d17O mode' or option_protocol.get()=="Gröning d17O mode":
        for i, j in enumerate(option_name_6_dict):
            for k in range(0, len(std_short_names_list)):
                if option_name_6_dict[j].get() == std_short_names_list[k]:
                    entry_6_dict[text_list_6_col4[i]].config(state="normal")
                    entry_6_dict[text_list_6_col4[i]].delete("1.0", "end")
                    entry_6_dict[text_list_6_col4[i]].insert(
                        "1.0", str(std_values_file["d18O"].iloc[k]))
                    entry_6_dict[text_list_6_col4[i]].config(state="disabled")
                    entry_6_dict[text_list_6_col5[i]].config(state="normal")
                    entry_6_dict[text_list_6_col5[i]].delete("1.0", "end")
                    entry_6_dict[text_list_6_col5[i]].insert(
                        "1.0", str(std_values_file["dD"].iloc[k]))
                    entry_6_dict[text_list_6_col5[i]].config(state="disabled")
                    entry_6_dict[text_list_6_col6[i]].config(state="normal")
                    entry_6_dict[text_list_6_col6[i]].delete("1.0", "end")
                    entry_6_dict[text_list_6_col6[i]].insert(
                        "1.0", str(std_values_file["d17O"].iloc[k]))
                    entry_6_dict[text_list_6_col6[i]].config(state="disabled")
    return

# Function to change the values of spy sample

def change_known_sample_values():
    global std_short_names_list, option_protocol, option_name_9_dict
    global entry_9_dict, text_list_9_col4, text_list_9_col5, text_list_9_col6
    if option_protocol.get() == "van Geldern mode" or option_protocol.get()=="Gröning mode":
        for i, j in enumerate(option_name_9_dict):
            for k in range(0, len(std_short_names_list)):
                if option_name_9_dict[j].get() == std_short_names_list[k]:
                    entry_9_dict[text_list_9_col4[i]].config(state="normal")
                    entry_9_dict[text_list_9_col4[i]].delete("1.0", "end")
                    entry_9_dict[text_list_9_col4[i]].insert(
                        "1.0", str(std_values_file["d18O"].iloc[k]))
                    entry_9_dict[text_list_9_col4[i]].config(state="disabled")
                    entry_9_dict[text_list_9_col5[i]].config(state="normal")
                    entry_9_dict[text_list_9_col5[i]].delete("1.0", "end")
                    entry_9_dict[text_list_9_col5[i]].insert(
                        "1.0", str(std_values_file["dD"].iloc[k]))
                    entry_9_dict[text_list_9_col5[i]].config(state="disabled")
    if option_protocol.get() == 'van Geldern d17O mode' or option_protocol.get()=="Gröning d17O mode":
        for i, j in enumerate(option_name_9_dict):
            for k in range(0, len(std_short_names_list)):
                if option_name_9_dict[j].get() == std_short_names_list[k]:
                    entry_9_dict[text_list_9_col4[i]].config(state="normal")
                    entry_9_dict[text_list_9_col4[i]].delete("1.0", "end")
                    entry_9_dict[text_list_9_col4[i]].insert(
                        "1.0", str(std_values_file["d18O"].iloc[k]))
                    entry_9_dict[text_list_9_col4[i]].config(state="disabled")
                    entry_9_dict[text_list_9_col5[i]].config(state="normal")
                    entry_9_dict[text_list_9_col5[i]].delete("1.0", "end")
                    entry_9_dict[text_list_9_col5[i]].insert(
                        "1.0", str(std_values_file["dD"].iloc[k]))
                    entry_9_dict[text_list_9_col5[i]].config(state="disabled")
                    entry_9_dict[text_list_9_col6[i]].config(state="normal")
                    entry_9_dict[text_list_9_col6[i]].delete("1.0", "end")
                    entry_9_dict[text_list_9_col6[i]].insert(
                        "1.0", str(std_values_file["d17O"].iloc[k]))
                    entry_9_dict[text_list_9_col6[i]].config(state="disabled")
    return

# Function that gather the index of standards used to normalise data

def get_index_std_normalisation():
    global var_6_dict
    std_idx_norm = []
    for i, j in enumerate(var_6_dict):
        if var_6_dict[j].get() == 1:
            std_idx_norm.append(i+1)
    return std_idx_norm

# Function to define the spy samples values table

def define_known_sample_table():
    global label_9_dict, entry_9_dict, option_name_9_dict, panned_w9, Entry_5_1
    global option_menu_9_dict, option_port_9_dict, option_port_menu_9_dict
    global text_list_9_col4, text_list_9_col5, text_list_9_col6, first_time
    port_list, result_file_df = lf.loading_file(option_protocol1, entry_1_1)
    known_sample_nbr = Entry_5_1.get()
    if known_sample_nbr.isdigit() == False:
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value !")
        return
    if known_sample_nbr != "" and known_sample_nbr.isdigit() == True:
        known_sample_nbr = int(known_sample_nbr)
    if known_sample_nbr > 6: # change the value here when you add more spy samples  
        tk.messagebox.showwarning(
            "Warning", "Too much spy samples reduce your number of spy samples !")
        return
    if option_protocol.get() == "van Geldern mode"  or option_protocol.get()=="Gröning mode":
        try:
            panned_w9.destroy()
        except NameError:
            first_time = 1
        panned_w9 = tk.PanedWindow(
            m, orient="vertical", bg="#056CF2", relief="solid")
        panned_w9.grid(row=8, column=5) # change here the number of rows to add more spy samples
        panned_w9.place(relx=0.5, rely=0.65, anchor="center")
        label_9_4 = tk.Label(panned_w9, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_9_4.grid(row=1, column=4, sticky="NSEW")
        label_9_5 = tk.Label(panned_w9, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_9_5.grid(row=1, column=5, sticky="NSEW")
    if option_protocol.get() == "van Geldern d17O mode" or option_protocol.get()=="Gröning d17O mode":
        try:
            panned_w9.destroy()
        except NameError:
            first_time = 1
        panned_w9 = tk.PanedWindow(m, orient="vertical", bg="#056CF2", relief="solid")
        panned_w9.grid(row=8, column=6) # change here the number of rows to add more spy samples
        panned_w9.place(relx=0.5, rely=0.65, anchor="center")
        label_9_4 = tk.Label(panned_w9, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_9_4.grid(row=1, column=4, sticky="NSEW")
        label_9_5 = tk.Label(panned_w9, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_9_5.grid(row=1, column=5, sticky="NSEW")
        label_9_6 = tk.Label(panned_w9, text="d17O", bg="#056CF2",
                             fg="white", font=("Helvetica Neue", 11))
        label_9_6.grid(row=1, column=6, sticky="NSEW")
    std_list = std_short_names_list
    #add a value in all the list below according to the patern to add more spy samples
    label_std_9_list = ["label_9_1", "label_9_2",
                        "label_9_3", "label_9_4", "label_9_5", "label_9_6"] 
    text_list_9_col4 = ["text_9_1", "text_9_4", "text_9_7",
                        "text_9_10", "text_9_13", "text_9_16"]
    text_list_9_col5 = ["text_9_2", "text_9_5", "text_9_8",
                        "text_9_11", "text_9_14", "text_9_17"]
    text_list_9_col6 = ["text_9_3", "text_9_6", "text_9_9",
                        "text_9_12", "text_9_15", "text_9_18"]
    option_port_9_list = ["option_port_9_1", "option_port_9_2", "option_port_9_3",
                          "option_port_9_4", "option_port_9_5", "option_port_9_6"]
    option_port_menu_9_list = ["option_port_menu_9_1", "option_port_menu_9_2", "option_port_menu_9_3",
                               "option_port_menu_9_4", "option_port_menu_9_5", "option_port_menu_9_6"]
    option_name_9_list = ["option_name_9_1", "option_name_9_2",
                          "option_name_9_3", "option_name_9_4", "option_name_9_5", "option_name_9_6"]
    option_menu_9_list = ["option_menu_9_1", "option_menu_9_2",
                          "option_menu_9_3", "option_menu_9_4", "option_menu_9_5", "option_menu_9_6"]
    # until there to add more spy samples 
    label_9_dict = {}
    entry_9_dict = {}
    option_name_9_dict = {}
    option_menu_9_dict = {}
    option_port_9_dict = {}
    option_port_menu_9_dict = {}
    for i in range(0, known_sample_nbr):
        label = tk.Label(panned_w9, text='spy sample ' +
                         str(i+1)+' : ', bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label.grid(row=i+2, column=1, sticky='NSEW')
        label_9_dict[label_std_9_list[i]] = label
    for i in range(0, known_sample_nbr):
        entry = tk.Text(panned_w9, height=1, width=10)
        entry.grid(row=i+2, column=4, sticky="NSEW")
        entry.config(state="disabled")
        entry_9_dict[text_list_9_col4[i]] = entry
        entry = tk.Text(panned_w9, height=1, width=10)
        entry.grid(row=i+2, column=5, sticky="NSEW")
        entry.config(state="disabled")
        entry_9_dict[text_list_9_col5[i]] = entry
        if option_protocol.get() == "van Geldern d17O mode" or option_protocol.get()=="Gröning d17O mode":
            entry = tk.Text(panned_w9, height=1, width=10)
            entry.grid(row=i+2, column=6, sticky="NSEW")
            entry.config(state="disabled")
            entry_9_dict[text_list_9_col6[i]] = entry
    for i in range(0, known_sample_nbr):
        option_port = tk.StringVar()
        option_port.set(port_list[i])
        option_port_9_dict[option_port_9_list[i]] = option_port
    for i in range(0, known_sample_nbr):
        option_port_menu = tk.OptionMenu(
            panned_w9, option_port_9_dict[option_port_9_list[i]], *port_list)
        option_port_menu.config(bg="#056CF2", activebackground="#056CF2",
                                bd=0, fg="white", font=("Helvetica Neue", 10))
        option_port_menu.grid(row=i+2, column=2)
        option_port_menu_9_dict[option_port_menu_9_list[i]] = option_port_menu
    for i in range(0, known_sample_nbr):
        option_name = tk.StringVar()
        option_name.set(std_list[i])
        option_name_9_dict[option_name_9_list[i]] = option_name
    for i in range(0, known_sample_nbr):
        option_menu = tk.OptionMenu(
            panned_w9, option_name_9_dict[option_name_9_list[i]], *std_list, command=lambda _: change_known_sample_values())
        option_menu.config(bg="#056CF2", activebackground="#056CF2",
                           bd=0, fg="white", font=("Helvetica Neue", 10))
        option_menu.grid(row=i+2, column=3)
        option_menu_9_dict[option_menu_9_list[i]] = option_menu

# Function that define the standards value's table

def define_table():
    std_nbr = Entry_3_1.get()
    if std_nbr.isdigit() == False:
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value !")
        return
    if std_nbr != "" and std_nbr.isdigit() == True:
        std_nbr = int(std_nbr)
    if std_nbr > 6: # change the value here when you add more standards 
        tk.messagebox.showwarning(
            "Warning", "Too much standards reduce your number of standards !")
        return
    global label_6_dict, entry_6_dict, option_name_6_dict
    global option_menu_6_dict, var_6_dict, checkbox_6_dict
    global text_list_6_col4, text_list_6_col5, text_list_6_col6, panned_w6,first_time
    if option_protocol.get() == "van Geldern mode" or option_protocol.get() == "Gröning mode":
        try:
            panned_w6.destroy()
        except NameError:
            first_time = 1
        panned_w6 = tk.PanedWindow(
            m, orient="vertical", bg="#056CF2" ,relief="solid")
        panned_w6.grid(row=8, column=5)  # change here the number of rows to add more standards
        panned_w6.place(relx=0.18, rely=0.65, anchor="center")
        label_6_4 = tk.Label(panned_w6, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_6_4.grid(row=1, column=4, sticky="NSEW")
        label_6_5 = tk.Label(panned_w6, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_6_5.grid(row=1, column=5, sticky="NSEW")
    if option_protocol.get() == "van Geldern d17O mode" or option_protocol.get() == "Gröning d17O mode":
        try:
            panned_w6.destroy()
        except NameError:
            first_time = 1
        panned_w6 = tk.PanedWindow(m, orient="vertical", bg="#056CF2", relief="solid")
        panned_w6.grid(row=8, column=6) # change here the number of rows to add more standards
        panned_w6.place(relx=0.18, rely=0.65, anchor="center")
        label_6_4 = tk.Label(panned_w6, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_6_4.grid(row=1, column=4, sticky="NSEW")
        label_6_5 = tk.Label(panned_w6, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_6_5.grid(row=1, column=5, sticky="NSEW")
        label_6_6 = tk.Label(panned_w6, text="d17O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_6_6.grid(row=1, column=6, sticky="NSEW")
    std_list = std_short_names_list
    # add a value in all the list below according to the patern to add more standards
    label_std_6_list = ["label_6_1", "label_6_2",
                        "label_6_3", "label_6_4", "label_6_5", "label_6_6"]
    text_list_6_col4 = ["text_6_1", "text_6_4", "text_6_7",
                        "text_6_10", "text_6_13", "text_6_16"]
    text_list_6_col5 = ["text_6_2", "text_6_5", "text_6_8",
                        "text_6_11", "text_6_14", "text_6_17"]
    text_list_6_col6 = ["text_6_3", "text_6_6", "text_6_9",
                        "text_6_12", "text_6_15", "text_6_18"]
    var_6_list = ["var_6_1", "var_6_2", "var_6_3",
                  "var_6_4", "var_6_5", "var_6_6"]
    checkbox_6_list = ["checkbox_6_1", "checkbox_6_2",
                       "checkbox_6_3", "checkbox_6_4", "checkbox_6_5", "checkbox_6_6"]
    option_name_6_list = ["option_name_6_1", "option_name_6_2",
                          "option_name_6_3", "option_name_6_4", "option_name_6_5", "option_name_6_6"]
    option_menu_6_list = ["option_menu_6_1", "option_menu_6_2",
                          "option_menu_6_3", "option_menu_6_4", "option_menu_6_5", "option_menu_6_6"]
    # until there to add more standards
    label_6_dict = {}
    entry_6_dict = {}
    option_name_6_dict = {}
    option_menu_6_dict = {}
    var_6_dict = {}
    checkbox_6_dict = {}
    for i in range(0, std_nbr):
        label = tk.Label(panned_w6, text='std '+str(i+1)+' : ',
                         bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label.grid(row=i+2, column=1, sticky='NSEW')
        label_6_dict[label_std_6_list[i]] = label
    for i in range(0, std_nbr):
        entry = tk.Text(panned_w6, height=1, width=10)
        entry.grid(row=i+2, column=4, sticky="NSEW")
        entry.config(state="disabled")
        entry_6_dict[text_list_6_col4[i]] = entry
        entry = tk.Text(panned_w6, height=1, width=10)
        entry.grid(row=i+2, column=5, sticky="NSEW")
        entry.config(state="disabled")
        entry_6_dict[text_list_6_col5[i]] = entry
        if option_protocol.get() == "van Geldern d17O mode" or option_protocol.get()=="Gröning d17O mode":
            entry = tk.Text(panned_w6, height=1, width=10)
            entry.grid(row=i+2, column=6, sticky="NSEW")
            entry.config(state="disabled")
            entry_6_dict[text_list_6_col6[i]] = entry
    for i in range(1, std_nbr):
        var = tk.IntVar()
        var.set(1)
        var_6_dict[var_6_list[i]] = var
    for i in range(1, std_nbr):
        checkbox = tk.Checkbutton(
            panned_w6, variable=var_6_dict[var_6_list[i]], bg="#056CF2", activebackground="#056CF2")
        checkbox.grid(row=i+2, column=2)
        checkbox_6_dict[checkbox_6_list[i]] = checkbox
    for i in range(0, std_nbr):
        option_name = tk.StringVar()
        option_name.set(std_list[i])
        option_name_6_dict[option_name_6_list[i]] = option_name
    for i in range(0, std_nbr):
        option_menu = tk.OptionMenu(
            panned_w6, option_name_6_dict[option_name_6_list[i]], *std_list, command=lambda _: change_std_values())
        option_menu.config(bg="#056CF2", activebackground="#056CF2",
                           bd=0, fg="white", font=("Helvetica Neue", 10))
        option_menu.grid(row=i+2, column=3)
        option_menu_6_dict[option_menu_6_list[i]] = option_menu
        
# Function to define parameters for the groning method

def define_groning_parameters_table():
    global groning_params, entry_12_list_col1, entry_12_list_col2, entry_12_list_col3
    if option_protocol.get()=="Gröning mode":
        try:
            panned_w12.destroy()
        except NameError:
            first_time = 1
        panned_w12=tk.PanedWindow(m,orient="vertical", bg="#056CF2")
        panned_w12.grid(row=4, column=3)
        panned_w12.place(relx=0.5, rely=0.9, anchor="center")
        label_12_4 = tk.Label(panned_w12, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_4.grid(row=1, column=2, sticky="NSEW")
        label_12_5 = tk.Label(panned_w12, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_5.grid(row=1, column=3, sticky="NSEW")
        entry_12_list_col1=["entry_12_2_2","entry_12_2_3","entry_12_2_4"]
        entry_12_list_col2=["entry_12_3_2","entry_12_3_3","entry_12_3_4"]
    if option_protocol.get()=="Gröning d17O mode":
        try:
            panned_w12.destroy()
        except NameError:
            first_time = 1
        panned_w12=tk.PanedWindow(m,orient="vertical", bg="#056CF2")
        panned_w12.grid(row=4, column=4)
        panned_w12.place(relx=0.5, rely=0.9, anchor="center")
        label_12_4 = tk.Label(panned_w12, text="\u03B418O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_4.grid(row=1, column=2, sticky="NSEW")
        label_12_5 = tk.Label(panned_w12, text="\u03B4D",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_5.grid(row=1, column=3, sticky="NSEW")
        label_12_6=tk.Label(panned_w12, text="\u03B417O",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_6.grid(row=1, column=4, sticky="NSEW")
        entry_12_list_col1=["entry_12_2_2","entry_12_2_3","entry_12_2_4"]
        entry_12_list_col2=["entry_12_3_2","entry_12_3_3","entry_12_3_4"]
        entry_12_list_col3=["entry_12_4_2","entry_12_4_3","entry_12_4_4"]
    if option_protocol.get()=="Gröning mode" or option_protocol.get()=="Gröning d17O mode":
        label_12_1=tk.Label(panned_w12, text="alpha",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_1.grid(row=2,column=1)
        label_12_2=tk.Label(panned_w12, text="beta",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_2.grid(row=3,column=1)
        label_12_3=tk.Label(panned_w12, text="balance",
                             bg="#056CF2", fg="white", font=("Helvetica Neue", 11))
        label_12_3.grid(row=4,column=1)
        groning_params={}
        for i in range(0,3):
            entry=tk.Entry(panned_w12,width=10)
            entry.grid(row=i+2, column=2, sticky="NSEW")
            groning_params[entry_12_list_col1[i]] = entry
            entry=tk.Entry(panned_w12,width=10)
            entry.grid(row=i+2, column=3, sticky="NSEW")
            groning_params[entry_12_list_col2[i]] = entry
            if option_protocol.get()=="Gröning d17O mode":
                entry=tk.Entry(panned_w12,width=10)
                entry.grid(row=i+2, column=4, sticky="NSEW")
                groning_params[entry_12_list_col3[i]] = entry
        
# Function to copy paste the working file into the raw_files_temp directory if local_directory is choosen (aswell as writting the filenaem in entry_1_1)

def copy_paste_local_dir(option_protocol1, entry_1_1):
    if option_protocol1 == "Local directory":
        filepath = filedialog.askopenfilename()
        filepath_splitted = os.path.split(filepath)
        directory_file = filepath_splitted[0]
        filename_long = filepath_splitted[1].rpartition(".")
        filename = filename_long[0]
        dest = "./files/raw_files_temp/"+filename+".csv"
        stl.copyfile(directory_file+"/"+filename+".csv", dest)
        entry_1_1.delete(0, "end")
        entry_1_1.insert(0, filename)

# function that set prefil basic

def set_prefill():
    Entry_3_1.delete(0, "end")
    Entry_3_1.insert(0, std_nbr)
    entry_4_1.delete(0, "end")
    entry_4_1.insert(0, inj_per_std)
    entry_7_1.delete(0, "end")
    entry_7_1.insert(0, nbr_spl)
    entry_7_2.delete(0, "end")
    entry_7_2.insert(0, inject_per_spl)
    if is_spy == 1:
        button_5_1.select()
        Entry_5_1.delete(0, "end")
        Entry_5_1.insert(0, spy_nbr)

# function that command the prefil


def command_prefil():
    global nbr_spl, inject_per_spl, is_spy, spy_nbr, std_nbr, inj_per_std, id2_df
    result_file_df, inj_nbr_df, id1_df, id2_df, port_df = pref.get_identifiers(
        option_protocol1, entry_1_1)
    if id2_df.dropna(how='all').empty == True:
        tk.messagebox.showerror("Error", "Error : Your file can't be prefilled (see documentation to know how to set-up the prefill) ")
        return
    error,*b = pref.counter(
        id1_df, id2_df, inj_nbr_df, port_df)
    if error==0:
        error,inj_per_std, std_nbr, inject_per_spl, nbr_spl, is_spy, spy_nbr, spy_port, spy_name_found, std_name_found=pref.counter(
            id1_df, id2_df, inj_nbr_df, port_df)
    if error==1:
        tk.messagebox.showerror("Error","No injection labelled with STD found")
        return
    if error==2:
        tk.messagebox.showerror("Error","No injection labelled with SAMPLE found")
        return
    if error==3:
        tk.messagebox.showerror("Error", "No injection labelled with SPY found")
    set_prefill()
    define_table()
    define_known_sample_table()
    for i, j in enumerate(option_name_6_dict):
        option_name_6_dict[j].set(std_name_found[i])
        change_std_values()
    if is_spy == True:
        for i, j in enumerate(option_port_9_dict):
            option_port_9_dict[j].set(spy_port[i])
            change_known_sample_values()
        for i, j in enumerate(option_name_9_dict):
            option_name_9_dict[j].set(spy_name_found[i])
            change_known_sample_values()
    return

# Function that check if there is format errors in the input from user

def check_errors():
    error=0
    global entry_4_1,entry_4_2,entry_7_1,entry_7_2,entry_7_3
    inject_per_std = entry_4_1.get()
    if inject_per_std.isdigit() == False:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of injection per standard !")
        return error
    if inject_per_std != "" and inject_per_std.isdigit() == True:
        inject_per_std = int(inject_per_std)
    if inject_per_std <= 0:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of injection per standard ! ")
        return error 
    removed_inject_per_std = entry_4_2.get()
    if removed_inject_per_std.isdigit() == False:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of removed injection per standard !")
        return error
    if removed_inject_per_std != "" and removed_inject_per_std.isdigit() == True:
        removed_inject_per_std = int(removed_inject_per_std)
    if removed_inject_per_std < 0:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of removed injection per standard !")
        return error
    nbr_spl = entry_7_1.get()
    if nbr_spl.isdigit() == False:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of sample !")
        return error
    if nbr_spl != "" and nbr_spl.isdigit() == True:
        nbr_spl = int(nbr_spl)
    if nbr_spl <= 0:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of sample ! ")
        return error
    inject_per_spl = entry_7_2.get()
    if inject_per_spl.isdigit() == False:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of injection per sample ! ")
        return error 
    if inject_per_spl != "" and inject_per_spl.isdigit() == True:
        inject_per_spl = int(inject_per_spl)
    if inject_per_spl <= 0:
        error = 1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of injection per sample ! ")
        return error
    removed_inject_per_spl = entry_7_3.get()
    if removed_inject_per_spl.isdigit() == False:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of removed injection per sample !")
        return error
    if removed_inject_per_spl != "" and removed_inject_per_spl.isdigit() == True:
        removed_inject_per_spl = int(removed_inject_per_spl)
    if removed_inject_per_spl < 0:
        error=1
        tk.messagebox.showwarning(
            "Warning", "You enter a non-authorized value in the number of removed injection per sample ! ")
        return error
    if removed_inject_per_spl>inject_per_spl:
        error=1
        tk.messagebox.showwarning("Warning","You can not remove more than you inject :) ")
        return error
    if removed_inject_per_std>inject_per_std:
        error=1
        tk.messagebox.showwarning("Warning","You can not remove more than you inject :) ")
        return error
# Function that read user inputs


def read_user_inputs():
    global Entry_3_1, entry_6_dict, text_list_6_col4, text_list_6_col5, text_list_6_col6
    global checkbox_var_5_1, option_protocol, std_short_names_list, port_list, protocol_type
    global Entry_5_1, var_5_1, known_values, port_known_samples_list, entry_11_1, entry_11_2,iso_type_list
    std_nbr = int(Entry_3_1.get())
    isotopes_nbr=len(iso_type_list)
    if var_5_1.get() == 1:
        known_sample_nbr = Entry_5_1.get()
        known_sample_nbr = int(known_sample_nbr)
        known_values = np.zeros((known_sample_nbr, isotopes_nbr))
        port_known_samples_list = []
        for i, j in enumerate(option_port_9_dict):
            port_known_samples_list.append(option_port_9_dict[j].get())
        for i in range(0, known_sample_nbr):
            known_values[i, 0] = float(
                entry_9_dict[text_list_9_col4[i]].get("1.0", "end"))
            known_values[i, 1] = float(
                entry_9_dict[text_list_9_col5[i]].get("1.0", "end"))
            if isotopes_nbr == 3:
                known_values[i, 2] = float(
                    entry_9_dict[text_list_9_col6[i]].get("1.0", "end"))
    std_values = np.zeros((std_nbr, isotopes_nbr))
    for i in range(0, std_nbr):
        std_values[i, 0] = float(
            entry_6_dict[text_list_6_col4[i]].get("1.0", "end"))
        std_values[i, 1] = float(
            entry_6_dict[text_list_6_col5[i]].get("1.0", "end"))
        if isotopes_nbr == 3:
            std_values[i, 2] = float(
                entry_6_dict[text_list_6_col6[i]].get("1.0", "end"))
    nbr_of_spl = int(entry_7_1.get())
    inj_per_std = int(entry_4_1.get())
    removed_inj_per_std = int(entry_4_2.get())
    inj_per_spl = int(entry_7_2.get())
    removed_inj_per_spl = int(entry_7_3.get())
    operator_id=entry_11_1.get()
    processor_id=entry_11_2.get()
    if option_protocol.get() == "Gröning mode" or option_protocol.get() == "Gröning d17O mode":
        groning_params_array=np.zeros((3,isotopes_nbr))
        for i in range(0,3):
            groning_params_array[i,0]=float(groning_params[entry_12_list_col1[i]].get())
            groning_params_array[i,1]=float(groning_params[entry_12_list_col2[i]].get())
            if isotopes_nbr==3:
                groning_params_array[i,2]=float(groning_params[entry_12_list_col3[i]].get())
    if option_protocol.get() == "van Geldern mode" or option_protocol.get() == "van Geldern d17O mode":
        groning_params_array=[]
    return std_nbr, std_values, inj_per_std, removed_inj_per_std, inj_per_spl, removed_inj_per_spl, nbr_of_spl, operator_id, processor_id,groning_params_array
# Function to get lines of the known samples


def get_lines_known_samples(result_file_df):
    global port_known_samples_list
    idx_known_sample = []
    for i in range(0, len(result_file_df)):
        if any(result_file_df["Port"].iloc[i] == port_known_sample for port_known_sample in port_known_samples_list):
            idx_known_sample.append(i)
    return idx_known_sample

# Function which changes plots (page 1)

def change_plots(dum, canvas,calibration_vectors,calibration_param_list):
    global page_results_1, option_plots, canvas1, canvas2, list_plots, corrected_file_df, std_nbr, inj_per_std
    canvas.get_tk_widget().destroy()
    if "canvas1" in globals():
        canvas1.get_tk_widget().destroy()
    if "canvas2" in globals():
        canvas2.get_tk_widget().destroy()
    if option_plots.get() == "All plots":
        figure1,ax1=plots.creation_all_plots(list_plots, corrected_file_df, iso_type_list, std_nbr, inj_per_std, option_name_6_dict, calibration_vectors, calibration_param_list)
        canvas = plots.all_plots_canvas_creator(figure1, page_results_1)
    else:
        figure1,figure2 = plots.create_two_figures(list_plots, option_plots, corrected_file_df, iso_type_list, std_nbr, inj_per_std, option_name_6_dict, calibration_vectors, calibration_param_list)
        canvas1, canvas2 = plots.other_plots_canvas_creator(figure1, figure2, page_results_1)

#Function to change table outliers page 

def change_table_outliers_page(option_menu_outliers,panned_w2_outliers):
    global Label_outliers_1_1,Label_outliers_1_2,entry_outliers_2_1, first_time, entry_outliers_2_2,label_outliers_list, var_outliers_list
    global label_outliers_dict,checkbox_outliers_dict, checkbox_outliers_list, var_outliers_dict,option_values_outliers
    if option_values_outliers.get()=="Only one Injection":
        try: 
            for i in range(1, std_nbr):
                label_outliers_dict[label_outliers_list[i-1]].destroy()
                checkbox_outliers_dict[checkbox_outliers_list[i-1]].destroy()
        except NameError:
            first_time=1
        Label_outliers_1_1=tk.Label(panned_w2_outliers,text="Please indicate the problematic standard : ")
        Label_outliers_1_1.grid(row=3,column=1)
        Label_outliers_1_2=tk.Label(panned_w2_outliers,text="Please indicate the problematic injection :")
        Label_outliers_1_2.grid(row=4,column=1)
        entry_outliers_2_1=tk.Entry(panned_w2_outliers)
        entry_outliers_2_1.grid(row=3,column=2,sticky="NSEW")
        entry_outliers_2_2=tk.Entry(panned_w2_outliers)
        entry_outliers_2_2.grid(row=4,column=2,sticky="NSEW")
    if option_values_outliers.get()=="More than one Injection":
        try: 
            Label_outliers_1_1.destroy()
            Label_outliers_1_2.destroy()
            entry_outliers_2_1.destroy()
            entry_outliers_2_2.destroy()
        except NameError: 
            first_time=1
        # in the lists below you need to add an item to add standards 
        label_outliers_list = ["label_1", "label_2",
                            "label_3", "label_4", "label_5", "label_6"]
        label_outliers_dict={}
        var_outliers_list = ["var_1", "var_2", "var_3",
                      "var_4", "var_5", "var_6"]
        checkbox_outliers_list = ["checkbox_1", "checkbox_2",
                           "checkbox_3", "checkbox_4", "checkbox_5", "checkbox_6"]
        #until there to add standards
        var_outliers_dict={}
        checkbox_outliers_dict={}
        for i in range(1,std_nbr):
            label = tk.Label(panned_w2_outliers, text='STD ' +
                             str(i+1)+' : ', font=("Helvetica Neue", 11))
            label.grid(row=i+5, column=1, sticky='NSEW')
            label_outliers_dict[label_outliers_list[i-1]] = label
            var = tk.IntVar()
            var.set(0)
            var_outliers_dict[var_outliers_list[i-1]] = var
        for i in range(1,std_nbr):
            checkbox = tk.Checkbutton(
                panned_w2_outliers, variable=var_outliers_dict[var_outliers_list[i-1]])
            checkbox.grid(row=i+5, column=2)
            checkbox_outliers_dict[checkbox_outliers_list[i-1]] = checkbox
    if option_values_outliers.get()=="No":
        try: 
            Label_outliers_1_1.destroy()
            Label_outliers_1_2.destroy()
            entry_outliers_2_1.destroy()
            entry_outliers_2_2.destroy()
        except NameError: 
            first_time=1
        try: 
            for i in range(1, std_nbr):
                label_outliers_dict[label_outliers_list[i-1]].destroy()
                checkbox_outliers_dict[checkbox_outliers_list[i-1]].destroy()
        except NameError:
            first_time=1
            
# Function to change the otuliers window to first result page 

def change_outliers_page():
    global option_menu_outliers,panned_w2_outliers, idx_std_to_use,len_std_injections, outliers_check_page
    idx_std_to_use=np.arange(std_nbr*inj_per_std)
    if option_values_outliers.get()=="Only one Injection":
        if entry_outliers_2_1.get().isdigit() == False:
            tk.messagebox.showwarning("Warning", "Not a Number inserted")
            return
        if entry_outliers_2_1.get().isdigit() == True:
            if int(entry_outliers_2_1.get())<=0:
                tk.messagebox.showwarning("Warning", "Negative value inserted")
                return
            if int(entry_outliers_2_1.get())==1:
                tk.messagebox.showwarning("Warning", "STD 1 is not used in memory correction")
                return
        if entry_outliers_2_2.get().isdigit() == False:
            tk.messagebox.showwarning("Warning", "Not a Number inserted")
            return
        if entry_outliers_2_2.get().isdigit() == True:
            if int(entry_outliers_2_2.get())<=0:
                tk.messagebox.showwarning("Warning", "Negative value inserted")
                return
        injection_to_remove=(int(entry_outliers_2_1.get())-1)*inj_per_std+int(entry_outliers_2_2.get())-1
        idx_std_to_use=np.delete(idx_std_to_use,injection_to_remove)
    if option_values_outliers.get()=="More than one Injection":
        start_inj_to_remove=[]
        for i, j in enumerate(var_outliers_dict):
            if var_outliers_dict[j].get() == 1:
                start_inj_to_remove.append(inj_per_std*(i+1))
        injection_to_remove=[]
        for i in range(0,len(start_inj_to_remove)):
            std_inj_to_remove=np.arange(start_inj_to_remove[i],start_inj_to_remove[i]+inj_per_std)
            for j in range(0,inj_per_std):
                injection_to_remove.append(std_inj_to_remove[j])
        idx_std_to_use=np.delete(idx_std_to_use,injection_to_remove)
    outliers_check_page.destroy()
        
# Function to open a new top level window (in the middle of the processing to check for memory correction)

def outliers_top_level():
    global outliers_check_page,option_menu_outliers,option_values_outliers
    outliers_check_page=tk.Toplevel(m)
    outliers_check_page.state('zoomed')
    outliers_check_page.configure(bg="#E8B300")
    outliers_check_page.title("Check processing")
    plots.memory_correction_parameters_plot(protocol_type, iso_type_list, std_nbr, inj_per_std, result_file_df, outliers_check_page,option_name_6_dict)
    message_text_outliers = tk.Message(master=outliers_check_page, text="Plots of the standards",
                                   font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
    message_text_outliers.place(relx=0.3, rely=0.1, anchor="center")
    panned_w_outliers = tk.PanedWindow(outliers_check_page, relief="solid")
    panned_w_outliers.grid(row=1, column=2)
    label_outliers = tk.Label(panned_w_outliers, text="File : ",
                          font=("Helvetica Neue", 14))
    label_outliers.grid(row=1, column=1)
    message_text_filename = tk.Entry(panned_w_outliers, font=(
        "Helvetica Neue", 14), width=40, disabledforeground="black")
    message_text_filename.insert(0, filename)
    message_text_filename.configure(state="disabled")
    message_text_filename.grid(row=1, column=2, padx=5, pady=5)
    panned_w_outliers.place(relx=0.55, rely=0.03, anchor="center")
    panned_w2_outliers=tk.PanedWindow(outliers_check_page,relief="solid")
    panned_w2_outliers.grid(row=std_nbr+3,column=2)
    label_outliers_1_1=tk.Label(panned_w2_outliers,text="Are there outlayers ? ")
    label_outliers_1_1.grid(row=1,column=1)
    option_list_outliers=["No","Only one Injection","More than one Injection"]
    option_values_outliers=tk.StringVar()
    option_values_outliers.set("No")
    option_menu_outliers=tk.OptionMenu(panned_w2_outliers,option_values_outliers,*option_list_outliers,command=lambda x,b=panned_w2_outliers: change_table_outliers_page(x,b))
    option_menu_outliers.grid(row=1,column=2)
    panned_w2_outliers.place(relx=0.75,rely=0.4,anchor="center")
    continue_button=tk.Button(outliers_check_page, text="Next page", font=("Helvetica Neue", 18), relief="raised",command=change_outliers_page)
    continue_button.place(relx=0.77, rely=0.1, anchor="center")
    
# Function to open a new top level window (first page results)

def change_page_result(calibration_vectors,is_residuals_results_table,is_spy_results_table,std_values, MCs, slope_MC_list,p_values_MC_list, operator_id, processor_id,starting_index_std,protocol_type,single_factor_mean,exp_params):
    global option_plots,list_plots,page_results_1
    page_results_1 = tk.Toplevel(m)
    page_results_1.state('zoomed')
    page_results_1.configure(bg="#E8B300")
    page_results_1.title("Results Plots 1")
    panned_w_pgr1 = tk.PanedWindow(page_results_1, relief="solid")
    panned_w_pgr1.grid(row=1, column=2)
    label_prg1 = tk.Label(panned_w_pgr1, text="File : ",
                          font=("Helvetica Neue", 14))
    label_prg1.grid(row=1, column=1)
    message_text_filename = tk.Entry(panned_w_pgr1, font=(
        "Helvetica Neue", 14), width=40, disabledforeground="black")
    message_text_filename.insert(0, filename)
    message_text_filename.configure(state="disabled")
    message_text_filename.grid(row=1, column=2, padx=5, pady=5)
    panned_w_pgr1.place(relx=0.55, rely=0.03, anchor="center")
    message_text_pgr1 = tk.Message(master=page_results_1, text="Plots of the results",
                                   font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
    list_plots = plots.create_list_plots(std_nbr, protocol_type,iso_type_list)
    fig, ax = plots.creation_all_plots(list_plots, corrected_file_df, iso_type_list, std_nbr, inj_per_std, option_name_6_dict, calibration_vectors, calibration_param_list)
    canvas = plots.all_plots_canvas_creator(fig, page_results_1)
    option_plots = tk.StringVar(m)
    option_plots.set("All plots")
    table_res_1.create_calibration_results_table(calibration_param_list, page_results_1, protocol_type, is_residuals_results_table, is_spy_results_table)
    if protocol_type==0 or protocol_type==1:
        single_factor_mean=[]
        exp_params=[]
    if protocol_type==2 or protocol_type==3:
        slope_MC_list=[]
        p_values_MC_list=[]
    table_res_1.create_MC_results_table(std_col1_list,protocol_type,page_results_1,is_residuals_results_table, is_spy_results_table,slope_MC_list,p_values_MC_list,iso_type_list,single_factor_mean,exp_params)
    table_res_1.create_standards_results(avg_std_list, std_dev_std_list, std_col1_list, protocol_type, page_results_1, is_residuals_results_table, is_spy_results_table)
    residuals_std=[]
    std_uncheck=[]
    if is_residuals_results_table == 1:
        residuals_std,std_uncheck=param_calc.calculate_residuals_standards(final_value_file_df, var_6_dict, std_values, inj_per_std, starting_index_std, protocol_type)
        table_res_1.create_residuals_standard_results_table(
            residuals_std, std_values, std_uncheck, page_results_1, protocol_type, is_residuals_results_table, is_spy_results_table)
    if is_spy_results_table == 1:
        table_res_1.create_known_sample_results_table(
            known_sample_results, page_results_1, known_values, protocol_type, is_residuals_results_table, is_spy_results_table)
    if is_spy_results_table == 1:
        next_page_btn = tk.Button(page_results_1, text="Next page", font=("Helvetica Neue", 18), relief="raised", command=lambda a=m, b=protocol_type, c=result_file_df,
                                  d=filename, e=spl_results, f=final_value_file_df,g=MCs,h=single_factor_mean,i=exp_params,j=std_uncheck,k=operator_id,l=processor_id,
                                  m=starting_index_std,n=residuals_std,o=std_values, p=known_sample_results, q=known_values, : change_page_result_2(a, b, c, d, e, f, g, h,i,j,k,l,m,n,o,p,q))
    if is_spy_results_table == 0:
        next_page_btn = tk.Button(page_results_1, text="Next page", font=("Helvetica Neue", 18), relief="raised", command=lambda a=m, b=protocol_type, c=result_file_df,
                                  d=filename, e=spl_results, f=final_value_file_df,g=MCs,h=single_factor_mean,i=exp_params,j=std_uncheck,k=operator_id,l=processor_id,
                                  m=starting_index_std,n=residuals_std,o=std_values: change_page_result_2(a, b, c, d, e, f,g,h,i,j,k,l,m,n,o))    
    optionmenu_plots = tk.OptionMenu(page_results_1, option_plots, *list_plots,
                                     command=lambda a,b=canvas,c=calibration_vectors,
                                     d=calibration_param_list: change_plots(a,b,c,d)) #a is a dum var only used bc it's in option menu need to be here for constietency of teh code only 
    optionmenu_plots.configure(font=("Helvetica Neue", 11))
    optionmenu_plots["menu"].configure(font=("Helvetica Neue", 11))
    message_text_pgr1.place(relx=0.3, rely=0.1, anchor="center")
    optionmenu_plots.place(rely=0.1, relx=0.5, anchor="center")
    next_page_btn.place(relx=0.77, rely=0.1, anchor="center")

# Function that open a new top level window (second page results)

def change_page_result_2(m, protocol_type, result_file_df, filename, spl_results, final_value_file_df, MCs, single_factor_mean, exp_params,std_uncheck, operator_id, processor_id, starting_index_std,residuals_std,std_values,known_sample_results=None, known_values=None):
    page_results_2 = tk.Toplevel(m)
    page_results_2.state('zoomed')
    page_results_2.configure(bg="#E8B300")
    page_results_2.title("Results Plots 2")
    panned_w_pgr2 = tk.PanedWindow(page_results_2, relief="solid")
    panned_w_pgr2.grid(row=1, column=2)
    label_prg2 = tk.Label(panned_w_pgr2, text="File : ",
                          font=("Helvetica Neue", 14))
    label_prg2.grid(row=1, column=1)
    message_text_filename = tk.Entry(panned_w_pgr2, font=(
        "Helvetica Neue", 14), width=40, disabledforeground="black")
    message_text_filename.insert(0, filename)
    message_text_filename.configure(state="disabled")
    message_text_filename.grid(row=1, column=2, padx=5, pady=5)
    panned_w_pgr2.place(relx=0.55, rely=0.05, anchor="center")
    message_text_pgr2 = tk.Message(master=page_results_2, text="Plots of the results",
                                   font=("Helvetica Neue", 18), bg="#D11F00", fg="white", relief="ridge", bd=3, width=500)
    message_text_pgr2.place(relx=0.3, rely=0.05, anchor="center")
    fig, ax = plots.make_raws_plots(protocol_type, result_file_df)
    canvas = FigureCanvasTkAgg(fig, master=page_results_2)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.03, rely=0.1, relheight=0.8, relwidth=0.5)
    table_res2.create_samples_results_table(
        page_results_2, spl_results, protocol_type)
    if type(known_sample_results) == list:
        saving_button = tk.Button(page_results_2, text="Save data", font=("Helvetica Neue", 18), relief="raised",
                                  command=lambda a=filename, b=spl_results, c=final_value_file_df, d=protocol_type,
                                  e=calibration_param_list, f=inj_per_std, g=page_results_2,
                                  h=MCs, i=single_factor_mean, j=exp_params,k=std_uncheck, l=operator_id, m=processor_id, n=option_protocol,o=std_nbr,
                                  p=starting_index_std, q=residuals_std,r=std_values,s=known_sample_results,t=known_values: sr.save_all_files(a, b, c, d, e, f, g, h, i, j, k, l, m, n,o,p,q,r,s,t))
    elif known_sample_results == None:
        saving_button = tk.Button(page_results_2, text="Save data", font=("Helvetica Neue", 18), relief="raised",
                                  command=lambda a=filename, b=spl_results, c=final_value_file_df, d=protocol_type,
                                  e=calibration_param_list, f=inj_per_std, g=page_results_2,
                                  h=MCs, i=single_factor_mean, j=exp_params, k=std_uncheck, l=operator_id, m=processor_id, n=option_protocol,o=std_nbr,
                                  p=starting_index_std, q=residuals_std,r=std_values,: sr.save_all_files(a, b, c, d, e, f, g, h, i, j, k,l,m,n,o,p,q,r))
    saving_button.place(relx=0.74, rely=0.02)
    replaced_values=0
    i=0
    while replaced_values==0 and i<final_value_file_df.index[-1]:
        if final_value_file_df["Correction Flag"].iloc[i]==2:
            replaced_values=1
        i=i+1
    if replaced_values==1:
        tk.messagebox.showwarning("Warning", "There is at least one sample which has not been corrected ! Check the Correction Flag in the final file and look for lines with 2 in this column", parent=page_results_2)    

#Function to set some variables for processing 

def init_variables_processing():
    global iso_type_list
    std_idx_norm = get_index_std_normalisation()
    filename = lf.downloading_file(option_protocol1, entry_1_1)
    iso_type_list=["d18O","dD"]
    if option_protocol.get()=="van Geldern d17O mode" or option_protocol.get()=="Gröning d17O mode":
        iso_type_list.append("d17O")
    std_nbr, std_values, inj_per_std, removed_inj_per_std, inj_per_spl, removed_inj_per_spl, spl_nbr,operator_id, processor_id,groning_params_array = read_user_inputs()
    is_residuals_results_table, is_spy_results_table = table_res_1.is_spy_and_is_residuals(
        var_6_dict, var_5_1)
    starting_index_std = removed_inj_per_std
    starting_index_spl = removed_inj_per_spl
    result_file_df, len_std_injections, len_spl_injections = lf.load_csv_file_into_DF(
        filename, std_nbr, inj_per_std, spl_nbr, inj_per_spl)
    MCs=[]
    slope_MC_list=[]
    p_values_MC_list=[]
    single_factor_mean=[]
    exp_params=[]
    return std_idx_norm,filename,iso_type_list,std_nbr, std_values, inj_per_std, removed_inj_per_std, inj_per_spl, removed_inj_per_spl, spl_nbr,is_residuals_results_table, is_spy_results_table,starting_index_std,starting_index_spl,result_file_df, len_std_injections, len_spl_injections,MCs,slope_MC_list,p_values_MC_list,operator_id,processor_id, groning_params_array, single_factor_mean, exp_params

# Function that apply procedure of correction

def proceeding():
    global protocol_type, result_file_df, entry_5_2, checkbox_var_5_1, std_short_names_list, list_plots, canvas, canvas1, canvas2, option_plots, corrected_file_df, std_nbr, inj_per_std, std_short_name_list, page_results_1
    global slope_MC_list, p_values_MC_list, avg_std_list, std_dev_std_list, std_col1_list, protocol_type, page_results_2, exp_params
    global spl_results, known_sample_results, port_known_samples_list, filename, final_value_file_df, MC_list, calibration_param_list, iso_type_list
    error=check_errors()
    if error==1:
        return
    std_idx_norm,filename,iso_type_list,std_nbr, std_values, inj_per_std, removed_inj_per_std, inj_per_spl, removed_inj_per_spl, spl_nbr,is_residuals_results_table, is_spy_results_table,starting_index_std,starting_index_spl,result_file_df, len_std_injections, len_spl_injections,MCs,slope_MC_list,p_values_MC_list,operator_id,processor_id,groning_params_array, single_factor_mean, exp_params=init_variables_processing()
    if var_5_1.get() == 1:
        idx_known_sample = get_lines_known_samples(result_file_df) 
    if option_protocol.get() == "van Geldern mode":
        protocol_type = 0
        outliers_top_level()
        m.wait_window(outliers_check_page)
        MC_one = np.ones((inj_per_std))
        last_injections=MC_calc_VG.create_last_injections(result_file_df, iso_type_list)
        corrected_file_df,MCs=MC_calc_VG.wrapper_memory_coefficient_van_geldern(iso_type_list, MC_one, inj_per_std, last_injections, result_file_df, len_std_injections, std_nbr,idx_std_to_use)
        final_value_file_df,calibration_param_list,calibration_vectors=cal.wrapper_calibration(corrected_file_df, iso_type_list, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std,std_nbr)
        slope_MC_list, p_values_MC_list, avg_std_list, std_dev_std_list, std_col1_list = param_calc.calculate_parameters_standards(final_value_file_df, protocol_type, starting_index_std, std_nbr, inj_per_std, removed_inj_per_std,iso_type_list)
        if is_residuals_results_table == 1:
            residuals_std, std_uncheck = param_calc.calculate_residuals_standards(
                final_value_file_df, var_6_dict, std_values, inj_per_std, starting_index_std, protocol_type)
        if is_spy_results_table == 1:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections, port_known_samples_list, idx_known_sample)
        if is_spy_results_table == 0:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections)
        change_page_result(calibration_vectors,is_residuals_results_table,is_spy_results_table,std_values, MCs, slope_MC_list,p_values_MC_list, operator_id, processor_id,starting_index_std,protocol_type,single_factor_mean,exp_params)
    if option_protocol.get() == "van Geldern d17O mode":
        protocol_type = 1
        outliers_top_level()
        m.wait_window(outliers_check_page)
        MC_one = np.ones((inj_per_std))
        last_injections=MC_calc_VG.create_last_injections(result_file_df, iso_type_list)
        corrected_file_df,MCs=MC_calc_VG.wrapper_memory_coefficient_van_geldern_d17O(iso_type_list, MC_one, inj_per_std, last_injections, result_file_df, len_std_injections, std_nbr,idx_std_to_use)    
        final_value_file_df,calibration_param_list,calibration_vectors=cal.wrapper_calibration(corrected_file_df, iso_type_list, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std,std_nbr)
        slope_MC_list, p_values_MC_list, avg_std_list, std_dev_std_list, std_col1_list = param_calc.calculate_parameters_standards(final_value_file_df, protocol_type, starting_index_std, std_nbr, inj_per_std, removed_inj_per_std,iso_type_list)
        if is_residuals_results_table == 1:
            residuals_std, std_uncheck = param_calc.calculate_residuals_standards(
                final_value_file_df, var_6_dict, std_values, inj_per_std, starting_index_std, protocol_type)
        if is_spy_results_table == 1:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections, port_known_samples_list, idx_known_sample)
        if is_spy_results_table == 0:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections)
        change_page_result(calibration_vectors,is_residuals_results_table,is_spy_results_table,std_values, MCs, slope_MC_list,p_values_MC_list, operator_id, processor_id,starting_index_std,protocol_type,single_factor_mean,exp_params)
    if option_protocol.get() == "Gröning mode":
        protocol_type=2
        corrected_file_df,single_factor_mean,exp_params=MC_calc_G.wrapper_memory_correction_groning_method(iso_type_list, result_file_df, len_std_injections,groning_params_array, inj_per_std)
        final_value_file_df,calibration_param_list,calibration_vectors=cal.wrapper_calibration(corrected_file_df, iso_type_list, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std,std_nbr)
        avg_std_list, std_dev_std_list, std_col1_list = param_calc.calculate_parameters_standards(final_value_file_df, protocol_type, starting_index_std, std_nbr, inj_per_std, removed_inj_per_std,iso_type_list)
        if is_residuals_results_table == 1:
            residuals_std, std_uncheck = param_calc.calculate_residuals_standards(
                final_value_file_df, var_6_dict, std_values, inj_per_std, starting_index_std, protocol_type)
        if is_spy_results_table == 1:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections, port_known_samples_list, idx_known_sample)
        if is_spy_results_table == 0:
            spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections)
        slope_MC_list=[]
        p_values_MC_list=[]
        change_page_result(calibration_vectors,is_residuals_results_table,is_spy_results_table,std_values, MCs, slope_MC_list,p_values_MC_list, operator_id, processor_id,starting_index_std,protocol_type,single_factor_mean,exp_params)
    if option_protocol.get() == "Gröning d17O mode":
         protocol_type=3
         corrected_file_df,single_factor_mean,exp_params=MC_calc_G.wrapper_memory_correction_groning_method(iso_type_list, result_file_df, len_std_injections,groning_params_array, inj_per_std)
         final_value_file_df,calibration_param_list,calibration_vectors=cal.wrapper_calibration(corrected_file_df, iso_type_list, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std,std_nbr)
         avg_std_list, std_dev_std_list, std_col1_list = param_calc.calculate_parameters_standards(final_value_file_df, protocol_type, starting_index_std, std_nbr, inj_per_std, removed_inj_per_std,iso_type_list)
         if is_residuals_results_table == 1:
             residuals_std, std_uncheck = param_calc.calculate_residuals_standards(
                 final_value_file_df, var_6_dict, std_values, inj_per_std, starting_index_std, protocol_type)
         if is_spy_results_table == 1:
             spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                 final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections, port_known_samples_list, idx_known_sample)
         if is_spy_results_table == 0:
             spl_results, known_sample_results = param_calc.calculate_spl_parameters(
                 final_value_file_df, protocol_type, starting_index_spl, spl_nbr, inj_per_spl, len_std_injections)
         slope_MC_list=[]
         p_values_MC_list=[]
         change_page_result(calibration_vectors,is_residuals_results_table,is_spy_results_table,std_values, MCs, slope_MC_list,p_values_MC_list, operator_id, processor_id,starting_index_std,protocol_type,single_factor_mean,exp_params)

# definition of root window

m = tk.Tk()
m.title("ALWIC-tool")
m.state('zoomed')
m.configure(bg="#BEE7E8")

# Panned window 5 (Known sample positions)

global panned_w9, Entry_5_1
panned_w5 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#056CF2")
panned_w5.grid(row=2, column=3)
label_5_1 = tk.Label(panned_w5, text="Spy samples ? ",
                     font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
label_5_1.grid(row=1, column=1)
var_5_1 = tk.IntVar()
button_5_1 = tk.Checkbutton(panned_w5, variable=var_5_1, onvalue=1,
                            offvalue=0, bg="#056CF2", activebackground="#056CF2")
button_5_1.grid(row=1, column=2)
Entry_5_1 = tk.Entry(panned_w5, font=("Helvetica Neue", 12), width=2)
Entry_5_1.grid(row=2, column=2)
label_5_2 = tk.Label(panned_w5, text="Number of known samples",
                     font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
label_5_2.grid(row=2, column=1, sticky="NSEW")
panned_w9 = tk.PanedWindow(m)
button_9_1 = tk.Button(panned_w5, text="Update", command=define_known_sample_table,
                       font=("Helvetica Neue", 15), height=2, width=6,
                       relief="raised", bg="#056CF2", fg="white")
button_9_1.grid(row=2, column=3)

# Panned window 8 (Process)

panned_w8 = tk.PanedWindow(m, orient="vertical", bg="#BEE7E8")
panned_w8.grid(row=1, column=1)
button_8_1 = tk.Button(panned_w8, bg="#FE4000", text="Processing", font=("Helvetica Neue", 18),
                       command=proceeding, relief="raised", height=3, width=9, activebackground="#80669d", activeforeground="white")
button_8_1.grid(row=1, column=1, sticky="NSEW", pady=40)

# Panned window 7 (injections and removed injections for samples)

panned_w7 = tk.PanedWindow(m, orient="vertical",  bg="#17E8C2", relief="solid")
panned_w7.grid(row=3, column=2)
entry_7_1 = tk.Entry(panned_w7, width=4, font=("Helvetica Neue", 12))
entry_7_1.grid(row=1, column=2, sticky="NSEW")
entry_7_2 = tk.Entry(panned_w7, width=4, font=("Helvetica Neue", 12))
entry_7_2.grid(row=2, column=2, sticky="NSEW")
entry_7_3 = tk.Entry(panned_w7, width=4, font=("Helvetica Neue", 12))
entry_7_3.grid(row=3, column=2, sticky="NSEW")

label_7_1 = tk.Label(panned_w7, text="Number of samples injected : ",
                     font=("Helvetica Neue", 14), bg="#17E8C2")
label_7_1.grid(row=1, column=1, sticky="NSEW", )
label_7_2 = tk.Label(panned_w7, text="Number of injections per sample : ",
                     font=("Helvetica Neue", 14), bg="#17E8C2")
label_7_2.grid(row=2, column=1, sticky="NSEW", )
label_7_3 = tk.Label(panned_w7, text="Number of injections removed per sample : ",
                     font=("Helvetica Neue", 14), bg="#17E8C2")
label_7_3.grid(row=3, column=1, sticky="NSEW", )

# Panned window 3 (values of standards with number of standards injected)

panned_w3 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#056CF2")
panned_w3.grid(row=1, column=3)
Entry_3_1 = tk.Entry(panned_w3, font=("Helvetica Neue", 12), width=2)
Entry_3_1.grid(row=1, column=2)
label_3_1 = tk.Label(panned_w3, text="Number of standard injected",
                     font=("Helvetica Neue", 14), bg="#056CF2", fg="white")
label_3_1.grid(row=1, column=1, sticky="NSEW", )
button_3_1 = tk.Button(panned_w3, text="Update", command=define_table,
                       font=("Helvetica Neue", 15), height=3, width=6, relief="raised", bg="#056CF2", fg="white")
button_3_1.grid(row=1, column=3)

# Panned window 4 (injections and removed injections for standards)

panned_w4 = tk.PanedWindow(m, orient="vertical", bg="#17E8C2", relief="solid")
panned_w4.grid(row=2, column=2)
label_4_1 = tk.Label(panned_w4, text="Number of injections per standard : ",
                     font=("Helvetica Neue", 14), bg="#17E8C2")
label_4_1.grid(row=1, column=1)
entry_4_1 = tk.Entry(panned_w4, font=("Helvetica Neue", 12), width=4)
entry_4_1.grid(row=1, column=2, sticky="NSEW")
entry_4_2 = tk.Entry(panned_w4, font=("Helvetica Neue", 12), width=4)
entry_4_2.grid(row=2, column=2, sticky="NSEW")
label_4_2 = tk.Label(panned_w4, text="Number on injections removed per standard : ",
                     font=("Helvetica Neue", 14), bg="#17E8C2")
label_4_2.grid(row=2, column=1)

# Head of window

message_text_1_1 = tk.Message(text="Welcome to ALWIC-tool !",
                              font=("Helvetica Neue", 18),  width=500,
                              bg="#D11F00", fg="white", relief="ridge", bd=3)

# Panned window 1 (filename)

panned_w1 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#327D94")
panned_w1.grid(row=1, column=3)
label_1_1 = tk.Label(panned_w1, font=("Helvetica Neue", 15),
                     text="Enter the filename :", fg="white", bg="#327D94")
label_1_1.grid(row=1, column=1, )
entry_1_1 = tk.Entry(panned_w1, font=("Helvetica Neue", 15), width=40)
entry_1_1.grid(row=1, column=2)
prefill_button = tk.Button(panned_w1, text="Prefill", command=command_prefil,
                           font=("Helvetica Neue", 15), width=5, relief="raised", fg="white", bg="#327D94")
prefill_button.grid(row=1, column=3)

# Panned window 2 (Protocol)

panned_w2 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#327D94")
panned_w2.grid(row=2, column=1)
label_2_1 = tk.Label(
    panned_w2, text="Protocol to follow :", font=("Helvetica Neue", 15), fg="white", bg="#327D94")
label_2_1.grid(row=1, column=1,)
optionlist = ["van Geldern mode", "van Geldern d17O mode","Gröning mode", "Gröning d17O mode"]
option_protocol = tk.StringVar(m)
option_protocol.set("van Geldern mode") # here you can change the default protocol 
optionmenu_2_1 = tk.OptionMenu(panned_w2, option_protocol, *optionlist,command= lambda _:define_groning_parameters_table())
optionmenu_2_1["menu"].configure(
    font=("Helvetica Neue", 15))
optionmenu_2_1.configure(font=("Helvetica Neue", 15), fg="white",
                         bg="#327D94", activebackground="#327D94", activeforeground="white")
optionmenu_2_1.grid(row=2, column=1, sticky="NSEW")

# Panned window 10 (file directory)

panned_w10 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#327D94")
panned_w10.grid(row=2, column=1)
label_10_1 = tk.Label(
    panned_w10, text="Choose the type of directory :", font=("Helvetica Neue", 15), bg="#327D94", fg="white")
label_10_1.grid(row=1, column=1 )
optionlist1 = ["Local directory", "Google drive"]
option_protocol1 = tk.StringVar(m)
option_protocol1.set("Google drive") 
optionmenu_10_1 = tk.OptionMenu(panned_w10, option_protocol1, *optionlist1,
                                command=lambda a=option_protocol1, b=entry_1_1: copy_paste_local_dir(a, b))
optionmenu_10_1["menu"].configure(
    font=("Helvetica Neue", 15))
optionmenu_10_1.configure(font=("Helvetica Neue", 15), fg="white",
                          bg="#327D94", activebackground="#327D94", activeforeground="white")
optionmenu_10_1.grid(row=2, column=1, sticky="NSEW")

# Panned window 11 (ids)

panned_w11 = tk.PanedWindow(m, orient="vertical", relief="solid", bg="#17E8C2")
panned_w11.grid(row=2, column=2)
label_11_1=tk.Label(panned_w11, text="Operator ID :", font=("Helvetica Neue", 15), bg="#17E8C2")
label_11_1.grid(row=1, column=1)
label_11_2=tk.Label(panned_w11, text="Processor ID :", font=("Helvetica Neue", 15), bg="#17E8C2")
label_11_2.grid(row=2,column=1)
entry_11_1=tk.Entry(panned_w11, font=("Helvetica Neue", 15), width=17)
entry_11_1.grid(row=1, column=2)
entry_11_2=tk.Entry(panned_w11, font=("Helvetica Neue", 15), width=17)
entry_11_2.grid(row=2, column=2)

# menu bar help

def open_github():
    url = "https://github.com/baptistebordet1/ALWIC-tool/blob/main/README.md"
    webbrowser.open_new(url)
    return


def open_pdf_documentation():
    os.system("start " + "./files/user_documentation.pdf")
    return


Menus = tk.Menu(m)
m.config(menu=Menus)
helpmenu = tk.Menu(Menus, tearoff=0)
Menus.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='Github', command=open_github)
helpmenu.add_command(label="Document", command=open_pdf_documentation)

# Disposition of the pannels

message_text_1_1.place(relx=0.5, rely=0.05, anchor="center")
panned_w1.place(relx=0.51, rely=0.15, anchor="w")
panned_w2.place(relx=0.125, rely=0.15, anchor="center")
panned_w4.place(relx=0.8, rely=0.5, anchor="center")
panned_w3.place(relx=0.18, rely=0.35, anchor="center")
panned_w7.place(relx=0.8, rely=0.35, anchor="center")
panned_w5.place(relx=0.5, rely=0.35, anchor="center")
panned_w8.place(relx=0.8, rely=0.8, anchor="center")
panned_w10.place(relx=0.3, rely=0.15, anchor="center")
panned_w11.place(relx=0.18, rely=0.9,anchor="center")

def close_window():
    if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
        files = os.listdir("./files/raw_files_temp/")
        if files != []:
            if "temp.txt" in files:
                os.remove("./files/raw_files_temp/temp.txt")
            for file in files:
                os.remove("./files/raw_files_temp/"+file)
        files = os.listdir("./files/saving_temp/")
        if files != []:
            if "temp.txt" in files:
                os.remove("./files/saving_temp/temp.txt")
            for file in files:
                os.remove("./files/saving_temp/"+file)
        m.destroy()
    return


m.protocol("WM_DELETE_WINDOW", close_window)
m.mainloop()
