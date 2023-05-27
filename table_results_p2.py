# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:52:09 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""
from tkinter import ttk

# Function to print results of the samples (pages results 2)

def create_samples_results_table(page_results_2, spl_results, protocol_type):
    """
    Print the samples result table on Page 2.

    Parameters
    ----------
    page_results_2 :  tkinter.Toplevel()
        Second result page
    spl_results : list
        Mean and std deviation on all samples
    protocol_type : int
        Which method of correction is used 

    Returns
    -------
    None. Only prints the table 

    """
    style = ttk.Style()
    style.theme_use("alt")
    table = ttk.Treeview(page_results_2)
    if protocol_type == 0 or protocol_type==2:
        table['columns'] = ('Sample position', 'd18 mean', 'dD mean', 'd-excess')
        table.heading("#0", text="Sample position", anchor="center")
        table.heading("Sample position",
                      text="Sample position", anchor="center")
        table.heading("d18 mean", text="\u03B4\u00B9\u2078O mean", anchor="center")
        table.heading("dD mean", text="\u03B4D mean", anchor="center")
        table.heading("d-excess", text="d-excess",anchor="center")
        table.column("#0", width=0,  stretch="NO")
        table.column("Sample position", anchor="center", width=80)
        table.column("d18 mean", anchor="center", width=80)
        table.column("dD mean", anchor="center", width=80)
        table.column("d-excess",anchor="center",width=80)
        count = 0
        for j in range(0, len(spl_results[0])):
            table.insert(parent='', index='end', iid=count, text='',
                         values=(str(spl_results[1][j]), str(spl_results[2][j]), str(spl_results[4][j]), str(spl_results[6][j])))
            count = count+1
    if protocol_type == 1 or protocol_type==3 :
        table['columns'] = ('Sample position', 'd18 mean',
                            'dD mean', "d17 mean","d-excess")
        table.heading("#0", text="Sample position", anchor="center")
        table.heading("Sample position",
                      text="Sample position", anchor="center")
        table.heading("d18 mean", text="\u03B4\u00B9\u2078O mean", anchor="center")
        table.heading("dD mean", text="\u03B4D mean", anchor="center")
        table.heading("d17 mean", text="\u03B4\u00B9\u2077O mean", anchor="center")
        table.heading("d-excess", text="d-excess",anchor="center")
        table.column("#0", width=0,  stretch="NO")
        table.column("Sample position", anchor="center", width=80)
        table.column("d18 mean", anchor="center", width=80)
        table.column("dD mean", anchor="center", width=80)
        table.column("d17 mean", anchor="center", width=80)
        table.column("d-excess",anchor="center",width=80)
        count = 0
        for j in range(0, len(spl_results[0])):
            table.insert(parent='', index='end', iid=count, text='',
                         values=(str(spl_results[1][j]), str(spl_results[2][j]), str(spl_results[4][j]), str(spl_results[6][j]), str(spl_results[8][j])))
            count = count+1
    sb = ttk.Scrollbar(page_results_2, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    table.place(relx=0.57, rely=0.1, relwidth=0.4, relheight=0.8)
    sb.place(relx=0.97,rely=0.1,relheight=0.8)
    return