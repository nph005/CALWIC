# -*- coding: utf-8 -*-
"""
Created on Friday July 15 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

import pandas as pd 
from tkinter import filedialog
import tkinter as tk 
import google_api as gapi
import shutil as stl
import os
from pathlib import Path
import Initialisation
from python_calamine.pandas import pandas_monkeypatch; pandas_monkeypatch()

config_dict=Initialisation.read_config_file()

# Function to load standards values 

def load_standard_csv_file():
    """
    load std values from std_values.csv

    Returns
    -------
    std_values_file : pandas.DataFrame
        Values of standards contained in the file 
    std_short_names_list : list
        List of the names of standards 

    """
    std_values_file=pd.read_csv(Path("./files/std_values.csv"),sep=None,engine="python")
    std_short_names_list=std_values_file[std_values_file.columns[1]].tolist()
    return std_values_file,std_short_names_list

# Function to load groning parameters csv file 

def load_groning_params_file():
    """
    load groning parameters values from groning_exp_parameters.csv

    Returns
    -------
    groning_params_file : pandas.DataFrame
        Values of exponential parameters contained in the file 
    instruments_names_list : list
        List of the names of instruments 
    """
    groning_params_file=pd.read_csv(Path("./files/groning_exp_parameters.csv"),sep=None,engine="python")
    instruments_names_list=groning_params_file[groning_params_file.columns[0]].tolist()
    return groning_params_file,instruments_names_list
# Function to load instrument identifier csv file 

def load_instrument_identifier_file():
    """
    load instruments names values from instrument_identifier.csv

    Returns
    -------
    instrument_identifier_list : list
        List of identifiers of instruments
    """
    instrument_identifier_file=pd.read_csv(Path("./files/instrument_identifier.csv"),sep=",",header=None)
    instrument_identifier_list=instrument_identifier_file[instrument_identifier_file.columns[0]].tolist()
    return instrument_identifier_list
# Function to load the results file and open it as a DataFrame

def load_csv_file_into_DF(filename,std_nbr,inj_per_std,spl_nbr,inj_per_spl):
    """
    Load the input file into a DataFrame and calculate some usefull lengths.
    This function is used in the processing function (see last function). 
    Parameters
    ----------
    filename : str
        Name of the input file. (without extension)
    std_nbr : int
        Number of standards
    inj_per_std : int
        Injections per standard
    spl_nbr : int
        Number of samples
    inj_per_spl : int
        Injections per sample

    Returns
    -------
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    len_std_injections : int 
        Total number of injections of standards
    len_spl_injections : int
        Total number of injections of samples

    """

    result_file_df=pd.read_csv(Path(os.path.join("./files/raw_files_temp/",filename+".csv")),sep=None,skipinitialspace=True,engine="python")
    result_file_df=result_file_df.rename(columns={"d(18_16)Mean":"raw_value_d18O","d(D_H)Mean":"raw_value_dD"})
    if "d(17_16)Mean" in result_file_df.columns:
        result_file_df=result_file_df.rename(columns={"d(17_16)Mean":"raw_value_d17O"})   
    len_std_injections=std_nbr*inj_per_std
    len_spl_injections=spl_nbr*inj_per_spl
    return result_file_df,len_std_injections,len_spl_injections
            
# Downloading file into a temporary file

def downloading_file(option_protocol1,entry_1_1): 
    """
    Download the files into a temporary folder if it doesn't exists yet. 
    It can be either downloaded from the google drive or copy paste from the a local folder.  

    Parameters
    ----------
    option_protocol1 : tkinter.stringVar()
        Stores the value of where to look for the file 
    entry_1_1 : tkinter.Entry()
        Contains the filename (without extension)

    Returns
    -------
    filename : str
        Name of the input file. (without extension)

    """
    filename=entry_1_1.get()
    files=os.listdir(Path('./files/raw_files_temp'))
    if filename+".csv" in files:
        return filename
    if option_protocol1.get()=="Local_directory":
        if config_dict["is_batch_processing"]=="True":
            directory_file=config_dict["directory_input_files"]
            filename=entry_1_1.get()
        else:
           default_path=""
           if os.path.isdir(Path(config_dict["directory_input_files"]))==True:
               default_path=Path(config_dict["directory_input_files"])
           filepath = filedialog.askopenfilename(initialdir=default_path)
           if filepath=="":
               return
           filepath_splitted = os.path.split(filepath)
           directory_file = filepath_splitted[0]
           filename_long = filepath_splitted[1].rpartition(".")
           filename = filename_long[0]
        if config_dict["extension_input_files"]==".xls" or config_dict["extension_input_files"]==".xlsx" :
            try:
                excel=pd.read_excel(Path(os.path.join(directory_file,filename+".xls")),index_col=None)
                excel.to_csv(Path(os.path.join(directory_file,filename+".csv")),encoding="utf-8")
            except:
                excel=pd.read_excel(Path(os.path.join(directory_file,filename+".xlsx")),index_col=None, engine="calamine")
                excel.to_csv(Path(os.path.join(directory_file,filename+".csv")),encoding="utf-8")
        dest = Path(os.path.join("./files/raw_files_temp/",filename+".csv"))
        stl.copyfile(Path(os.path.join(directory_file,filename+".csv")), dest)
    if option_protocol1.get()=="Google_drive":
        error=gapi.download(filename)
        if error==1:
            tk.messagebox.showwarning("Warning","File not found in drive !!")
            return
    return filename 

# Function to load file (must be done before processing if spy samples are included )

def loading_file(option_protocol1,entry_1_1):
    """
    Download file and then import it in DataFrame. 
    This function is used for spy samples if there are. 

    Parameters
    ----------
    option_protocol1 : tkinter.stringVar()
        Stores the value of where to look for the file 
    entry_1_1 : tkinter.Entry()
        Contains the filename (without extension)

    Returns
    -------
    port_list : list
        List of column "Port" extracted from result_file_df
    filename : str
        Name of the input file. (without extension)

    """
    filename=downloading_file(option_protocol1,entry_1_1)
    result_file_df=pd.read_csv(Path(os.path.join("./files/raw_files_temp/",filename+".csv")),sep=None,skipinitialspace=True,engine="python")
    port_temp=result_file_df["Port"].tolist()
    port_list=[port_temp[0]]
    for i in range(1,len(port_temp)):
        if port_temp[i]!=port_list[-1]:
            port_list.append(port_temp[i])
    return port_list, filename, result_file_df
