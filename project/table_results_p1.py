# -*- coding: utf-8 -*-
"""
Created on Monday July 18 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

from tkinter import ttk 

def is_spy_and_is_residuals(var_6_dict,var_5_1):
    """
    Determines if there are residuals to calculate
    and/or spy samples in the run. The returned values are only 
    used for the results table.

    Parameters
    ----------
    var_6_dict : dictionary
        Dictionary storing the values of the CheckButtons on the standards' table
    var_5_1 : tkinter.IntVar()
        Variable connected to button_5_1 (See main.py)
        

    Returns
    -------
    is_residuals_results_table : Boolean
        0 if there is no residuals, 1 if there is 
    is_spy_results_table : Boolean
        0 if there is no spy sample, 1 if there is

    """
    is_residuals_results_table=0
    is_spy_results_table=0
    for i,j in enumerate(var_6_dict):
        if var_6_dict[j].get()==0:
            is_residuals_results_table=1
            break
    if var_5_1.get()==1:
        is_spy_results_table=1
    return is_residuals_results_table, is_spy_results_table

# Function to create table of MC results (results page 1)

def create_MC_results_table(std_col1_list,protocol_type,page_results_1,is_residuals_results_table, is_spy_results_table,slopes_MC_list,p_values_MC_list,iso_type_list,single_factor_list,exp_params): 
    """
    Print the result table about memory correction 
    on page result 1.

    Parameters
    ----------

    std_col1_list : list
        Names to include in the first column of the Memory correction results in table _results_p1
    protocol_type : int
        Which method of correction is used 
    page_results_1 : tkinter.Toplevel()
        First result page
    is_residuals_results_table : Boolean
        0 if there is no residuals, 1 if there is
    is_spy_results_table : Boolean
        0 if there is no spy sample, 1 if there is
    slopes_MC_list : list
        Slope of each standard
    p_values_MC_list : list
        p-value of each standard

    Returns
    -------
    None. Only prints the table

    """
    style=ttk.Style()
    style.theme_use("alt")
    table=ttk.Treeview(page_results_1)
    if protocol_type==0 or protocol_type==1:
        table['columns'] = ("title", 'slope MC correction', 'p-value')
    if protocol_type==2 or protocol_type==3:
        table['columns'] = ("title", "single factor", "alpha", "beta", "balance")
    table.heading("#0",text="",anchor="center")
    table.heading("title",text="𝗠𝗲𝗺𝗼𝗿𝘆 𝗖𝗼𝗿𝗿𝗲𝗰𝘁𝗶𝗼𝗻",anchor="center")
    if protocol_type==0 or protocol_type==1:
        table.heading("slope MC correction",text="slope MC correction",anchor="center")
        table.heading("p-value",text="p-value",anchor="center")
        table.column("slope MC correction",anchor="center",width=80)
        table.column("p-value",anchor="center",width=80)
    if protocol_type==2 or protocol_type==3:
        table.heading("single factor",text="single factor",anchor="center")
        table.heading("alpha",text="alpha",anchor="center")
        table.heading("beta",text="beta",anchor="center")
        table.heading("balance",text="balance",anchor="center")
        table.column("single factor",anchor="center",width=80)
        table.column("alpha",anchor="center",width=80)
        table.column("beta",anchor="center",width=80)
        table.column("beta",anchor="center",width=80)
        table.column("balance",anchor="center",width=80)
    table.column("#0", width=0,  stretch="NO")
    table.column("title",anchor="center", width=80)
    if protocol_type==0 or protocol_type==1:
        count=0
        for j in range(0,len(std_col1_list)):
            table.insert(parent='',index='end',iid=count,text='',
                     values=(str(std_col1_list[j]),str(slopes_MC_list[j]),str(p_values_MC_list[j])))
            count=count+1
    if protocol_type==2 or protocol_type==3:
        iso_type_str_list=["\u03B4\u00B9\u2078O","\u03B4D","\u03B4\u00B9\u2077O"]
        count=0
        for j in range(len(iso_type_list)):
            table.insert(parent='',index='end',iid=count,text='',
                     values=(iso_type_str_list[j],str(round(single_factor_list[j],3)),str(exp_params[0,j]),str(exp_params[1,j]),str(exp_params[2,j])))
            count=count+1
    sb = ttk.Scrollbar(page_results_1, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    if is_residuals_results_table==1 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.33,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.33,relheight=0.11)
    if is_residuals_results_table==1 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.48,relwidth=0.4,relheight=0.14)
        sb.place(relx=0.97,rely=0.48,relheight=0.14)
    if is_residuals_results_table==0 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.51,relwidth=0.4,relheight=0.2)
        sb.place(relx=0.97,rely=0.51,relheight=0.2)
    if is_residuals_results_table==0 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.33,relwidth=0.4,relheight=0.15)
        sb.place(relx=0.97,rely=0.33,relheight=0.15)
    return

# Function to print results of standards (raww mean and raw standard deviation)

#TODO add docstring 
def create_standards_results(avg_std_list,std_dev_std_list,std_col1_list,protocol_type,page_results_1,is_residuals_results_table, is_spy_results_table):
    """
    

    Parameters
    ----------
    avg_std_list : list
        Mean of the raw data of each standard
    std_dev_std_list : list
        Standard deviation of the raw data of each standard formatted for the table_results_p1 needs
    std_col1_list : TYPE
        DESCRIPTION.
    protocol_type : TYPE
        DESCRIPTION.
    page_results_1 : TYPE
        DESCRIPTION.
    is_residuals_results_table : TYPE
        DESCRIPTION.
    is_spy_results_table : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    style=ttk.Style()
    style.theme_use("alt")
    table=ttk.Treeview(page_results_1) 
    table['columns'] = ('title', 'mean', 'std dev')
    table.heading("#0",text="",anchor="center")
    table.heading("title",text="𝗦𝘁𝗮𝗻𝗱𝗮𝗿𝗱𝘀 𝗣𝗮𝗿𝗮𝗺𝗲𝘁𝗲𝗿𝘀",anchor="center")
    table.heading("mean",text="raw mean",anchor="center")
    table.heading("std dev",text="raw std dev",anchor="center")
    table.column("#0", width=0,  stretch="NO")
    table.column("title",anchor="center", width=80)
    table.column("mean",anchor="center",width=80)
    table.column("std dev",anchor="center",width=80)
    count=0
    for j in range(0,len(std_col1_list)):
        table.insert(parent='',index='end',iid=count,text='',
                 values=(str(std_col1_list[j]),str(avg_std_list[j]),str(std_dev_std_list[j])))
        count=count+1
    sb = ttk.Scrollbar(page_results_1, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    if is_residuals_results_table==1 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.15,relwidth=0.4,relheight=0.15)
        sb.place(relx=0.97,rely=0.15,relheight=0.15)
    if is_residuals_results_table==1 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.15,relwidth=0.4,relheight=0.3)
        sb.place(relx=0.97,rely=0.15,relheight=0.3)
    if is_residuals_results_table==0 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.15,relwidth=0.4,relheight=0.3)
        sb.place(relx=0.97,rely=0.15,relheight=0.3)
    if is_residuals_results_table==0 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.15,relwidth=0.4,relheight=0.15)
        sb.place(relx=0.97,rely=0.15,relheight=0.15)
    return 
# Function to print results of calibration 

def create_calibration_results_table(calibration_param_list,page_results_1,protocol_type,is_residuals_results_table, is_spy_results_table): 
    """
    Print the result table about calibration curve
    on page result 1. 

    Parameters
    ----------
    calibration_param_list : list of list 
        Contains the slopes and intercept of the different isotopes 
    page_results_1 : tkinter.Toplevel()
        First result page
    protocol_type : int
        Which method of correction is used 
    is_residuals_results_table : Boolean
        0 if there is no residuals, 1 if there is
    is_spy_results_table : Boolean
        0 if there is no spy sample, 1 if there is

    Returns
    -------
    None. Only prints the table

    """
    style=ttk.Style()
    style.theme_use("alt")
    table=ttk.Treeview(page_results_1) 
    table['columns'] = ('std', 'slope', 'intercept')
    table.heading("#0",text="",anchor="center")
    table.heading("std",text="𝗖𝗮𝗹𝗶𝗯𝗿𝗮𝘁𝗶𝗼𝗻 𝗖𝘂𝗿𝘃𝗲",anchor="center")
    table.heading("slope",text="slope",anchor="center")
    table.heading("intercept",text="Intercept",anchor="center")
    table.column("#0", width=0,  stretch="NO")
    table.column("std",anchor="center", width=80)
    table.column("slope",anchor="center",width=80)
    table.column("intercept",anchor="center",width=80)
    table.insert(parent='',index='end',iid=0,text='',
                     values=("\u03B4\u00B9\u2078O",str(calibration_param_list[0][0]),str(calibration_param_list[1][0])))
    table.insert(parent='',index='end',iid=1,text='',
                     values=("\u03B4D",str(calibration_param_list[0][1]),str(calibration_param_list[1][1])))
    if protocol_type==1:
        table.insert(parent='',index='end',iid=2,text='',
                         values=("\u03B4\u00B9\u2077O",str(calibration_param_list[0][2]),str(calibration_param_list[1][2])))
    sb = ttk.Scrollbar(page_results_1, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    if is_residuals_results_table==1 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.47,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.47,relheight=0.11)
    if is_residuals_results_table==1 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.65,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.65,relheight=0.11)
    if is_residuals_results_table==0 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.77,relwidth=0.4,relheight=0.13)
        sb.place(relx=0.97,rely=0.77,relheight=0.13)
    if is_residuals_results_table==0 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.51,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.51,relheight=0.11)
    return


# Function to create residuals of standards not used in calibration 

def create_residuals_standard_results_table(residuals_std,std_values,std_uncheck,page_results_1,protocol_type,is_residuals_results_table, is_spy_results_table):
    """
    Print the result table about residuals
    on page result 1.

    Parameters
    ----------
    residuals_std : list
        Mean values of standards not used for calibration
    std_values : numpy.array
        Stores the given ("true") values of the standards
    std_uncheck : list
        list of index of standards not used for calibration 
    page_results_1 : tkinter.Toplevel()
        First result page
    protocol_type : int
        Which method of correction is used 
    is_residuals_results_table : Boolean
        0 if there is no residuals, 1 if there is
    is_spy_results_table : Boolean
        0 if there is no spy sample, 1 if there is

    Returns
    -------
    None. Only prints the table

    """ 
    style=ttk.Style()
    style.theme_use("alt")
    table=ttk.Treeview(page_results_1)
    table["columns"]=("title", "measured", "true", "residuals")
    table.heading("#0",text="",anchor="center")
    table.heading("title",text="𝗦𝘁𝗮𝗻𝗱𝗮𝗿𝗱𝘀 𝗥𝗲𝘀𝗶𝗱𝘂𝗮𝗹𝘀",anchor="center")
    table.heading("measured",text="measured",anchor="center")
    table.heading("true",text="true",anchor="center")
    table.heading("residuals",text="residuals",anchor="center")
    table.column("#0", width=0,  stretch="NO")
    table.column("title",anchor="center", width=80)
    table.column("measured",anchor="center",width=80)
    table.column("true",anchor="center",width=80)
    table.column("residuals",anchor="center",width=80)
    j=0
    for i in range(0,len(std_uncheck)):
        residuals=residuals_std[0][i]-std_values[i,0]
        residuals=round(residuals,4)
        table.insert(parent='',index='end',iid=j,text='',
                     values=("STD "+str(std_uncheck[i]+1)+" \u03B4\u00B9\u2078O", residuals_std[0][i], std_values[i,0],residuals))
        j=j+1
        residuals=residuals_std[1][i]-std_values[i,1]
        residuals=round(residuals,4)
        table.insert(parent='',index='end',iid=j,text='',
                     values=("STD "+str(std_uncheck[i]+1)+" \u03B4D", residuals_std[1][i], std_values[i,1],residuals))
        j=j+1
        if protocol_type==1:
            residuals=residuals_std[2][i]-std_values[i,2]
            residuals=round(residuals,4)
            table.insert(parent='',index='end',iid=j,text='',
                     values=("STD "+str(std_uncheck[i]+1)+" \u03B4\u00B9\u2077O", residuals_std[2][i], std_values[i,2],residuals))
    sb = ttk.Scrollbar(page_results_1, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    if is_residuals_results_table==1 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.61,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.61,relheight=0.11)
    if is_residuals_results_table==1 and is_spy_results_table==0:
        table.place(relx=0.57,rely=0.79,relwidth=0.4,relheight=0.11)
        sb.place(relx=0.97,rely=0.79,relheight=0.11)
    if is_residuals_results_table==0 and is_spy_results_table==0:
        return
    if is_residuals_results_table==0 and is_spy_results_table==1:
        return
# Function to create known sample results  

def create_known_sample_results_table(known_sample_results,page_results_1,known_values,protocol_type,is_residuals_results_table, is_spy_results_table):
    """
    Print the result table about control samples
    on page result 1.

    Parameters
    ----------
    known_sample_results : list 
        Mean and standard deviation for all spy samples  
    page_results_1 : tkinter.Toplevel()
        First result page
    known_values : numpy.array
        Stores the given ("true") values of the known samples
    protocol_type : int
        Which method of correction is used 
    is_residuals_results_table : Boolean
        0 if there is no residuals, 1 if there is
    is_spy_results_table : Boolean
        0 if there is no spy sample, 1 if there is

    Returns
    -------
    None. Only prints the table

    """
    style=ttk.Style()
    style.theme_use("alt")
    table=ttk.Treeview(page_results_1)
    table['columns'] = ('title', 'measured', 'true', 'residuals')
    table.heading("#0",text="",anchor="center")
    table.heading("title",text="𝗞𝗻𝗼𝘄𝗻 𝗦𝗮𝗺𝗽𝗹𝗲𝘀",anchor="center")
    table.heading("measured",text="measured",anchor="center")
    table.heading("true",text="true",anchor="center")
    table.heading("residuals",text="residuals",anchor="center")
    table.column("#0", width=0,  stretch="NO")
    table.column("title",anchor="center", width=80)
    table.column("measured",anchor="center",width=80)
    table.column("true",anchor="center",width=80)
    table.column("residuals",anchor="center",width=80)
    i=0
    for j in range(0,len(known_sample_results[0])):
        residuals=known_sample_results[1][j]-known_values[j,0]
        residuals=round(residuals,2)
        table.insert(parent='',index='end',iid=i,text='',
                     values=(str(known_sample_results[0][j])+" \u03B4\u00B9\u2078O",str(known_sample_results[1][j]),str(known_values[j,0]),str(residuals)))
        i=i+1
        residuals=known_sample_results[3][j]-known_values[j,1]
        residuals=round(residuals,2)
        table.insert(parent='',index='end',iid=i,text='',
                     values=(str(known_sample_results[0][j])+" \u03B4D",str(known_sample_results[3][j]),str(known_values[j,1]),str(residuals)))
        i=i+1
        if protocol_type==1:
            residuals=known_sample_results[5][j]-known_values[j,2]
            residuals=round(residuals,2)
            table.insert(parent='',index='end',iid=i,text='',
                         values=(str(known_sample_results[0][j])+" \u03B4\u00B9\u2077O",str(known_sample_results[5][j]),str(known_values[j,2]),str(residuals)))
            i=i+1
    sb = ttk.Scrollbar(page_results_1, orient="vertical")
    table.config(yscrollcommand=sb.set)
    sb.config(command=table.yview)
    if is_residuals_results_table==1 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.75,relwidth=0.4,relheight=0.15)
        sb.place(relx=0.97,rely=0.75,relheight=0.15)
    if is_residuals_results_table==0 and is_spy_results_table==1:
        table.place(relx=0.57,rely=0.66,relwidth=0.4,relheight=0.24)
        sb.place(relx=0.97,rely=0.66,relheight=0.24)
    if is_residuals_results_table==0 and is_spy_results_table==0:
        return
    if is_residuals_results_table==1 and is_spy_results_table==0:
        return
    return
