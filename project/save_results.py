# -*- coding: utf-8 -*-
"""
Created on Tuesday July 19 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from scipy import signal 
import os
import google_api
import PIL

save_extension=".txt"

# Function to save standard's parameters in a csv

def save_std_parameters_file(calibration_param_list,inj_per_std,std_uncheck,final_value_file_df,operator_id,processor_id,std_nbr,starting_index_std,residuals_std,std_values,protocol_type,filename,directory_path,option_protocol,MCs=None,single_factor_mean=None,exp_params=None):
    """
    Format the standards parameters and then save it in a file 

    Parameters
    ----------
    calibration_param_list : list
        Calibration curve parameters
    inj_per_std : int
        Injections per standard
    std_uncheck : list
        List of index of standards not used for calibration 
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    operator_id : str
        Name of the person who performed the measurements 
    processor_id : str
        Name of the person who processed the file 
    std_nbr : int
        Number of standards
    starting_index_std : int
        Index corresponding to removed injection for standard 
    residuals_std : list
        Mean values of standards not used for calibration
    std_values : numpy.array
        Stores the given ("true") values of the standards 
    protocol_type : int
        Which method of correction is used 
    filename : str
        Name of the input file. (without extension)
    directory_path : str
        Folder where the results files will be saved
    option_protocol : tk.StingVar()
        Contains the name of the correction method used
    MCs : dict, optional
        Contains the Memory coefficients after optimization
    single_factor_mean : list, optional
        Contains the single factor values for each isotope
    exp_params : list, optional
        Contains the alpha, beta and balance values used in the Gröning correction

    Returns
    -------
    None. Only save the standard results file

    """
    detrended = signal.detrend(final_value_file_df["H2O_Mean"].interpolate())
    std_dev_humidity=np.std(detrended)
    column1=["start time : ", "end time : ","operator id : ", "processor id :","correction method","std dev of humidity (detrended)"]
    if protocol_type==0 or protocol_type==1:
        column1.append("MC d18O")
        for i in range(len(MCs["d18O"])-1):
            column1.append("")
    if protocol_type==2 or protocol_type==3:
        column1.append("single_factor d18O")
        column1.append("alpha d18O")
        column1.append("beta d18O")
        column1.append("balance d18O")
    column1.append("slope d18O")
    column1.append("intercept d18O")
    for i in range(1,std_nbr):
        column1.append("STD "+str(i+1)+" avg d18O")
        column1.append("STD "+str(i+1)+" std dev d18O")
    for i in range(0,len(std_uncheck)):
        column1.append("STD "+str(std_uncheck[i]+1)+" measured d18O")
        column1.append("STD "+str(std_uncheck[i]+1)+" true d18O")
        column1.append("STD "+str(std_uncheck[i]+1)+" residuals d18O")
    column2=[final_value_file_df["Time Code"].iloc[0],final_value_file_df["Time Code"].iloc[-1],operator_id,processor_id,option_protocol.get(),std_dev_humidity]   
    if protocol_type==0 or protocol_type==1:
        for i in range(len(MCs["d18O"])):
            column2.append(MCs["d18O"][i])
    if protocol_type==2 or protocol_type==3:
        column2.append(single_factor_mean[0])
        for i in range(0,3):
            column2.append(exp_params[i,0])
    column2.append(calibration_param_list[0][0])
    column2.append(calibration_param_list[1][0])
    for i in range(1,std_nbr):
        column2.append(np.mean(final_value_file_df["raw_value_d18O"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
        column2.append(np.std(final_value_file_df["raw_value_d18O"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
    for i in range(0,len(std_uncheck)):
        column2.append(residuals_std[0][i])
        column2.append(std_values[i][0])
        column2.append(round(residuals_std[0][i]-std_values[i,0],4))
    column3=["","","","","","ppmv"]
    if protocol_type==0 or protocol_type==1:
        column3.append("MC dD")
        for i in range(len(MCs["dD"])-1):
            column3.append("")
    if protocol_type==2 or protocol_type==3:
        column3.append("single_factor dD")
        column3.append("alpha dD")
        column3.append("beta dD")
        column3.append("balance dD")
    column3.append("slope dD")
    column3.append("intercept dD")
    for i in range(1,std_nbr):
        column3.append("STD "+str(i+1)+" avg dD")
        column3.append("STD "+str(i+1)+" std dev dD")
    for i in range(0,len(std_uncheck)):
        column3.append("STD "+str(std_uncheck[i]+1)+" measured dD")
        column3.append("STD "+str(std_uncheck[i]+1)+" true dD")
        column3.append("STD "+str(std_uncheck[i]+1)+" residuals dD")
    column4=["","","","","",""]
    if protocol_type==0 or protocol_type==1:
        for i in range(len(MCs["dD"])):
            column4.append(MCs["dD"][i])
    if protocol_type==2 or protocol_type==3:
        column4.append(single_factor_mean[1])
        for i in range(0,3):
            column4.append(exp_params[i,1])
    column4.append(calibration_param_list[0][1])
    column4.append(calibration_param_list[1][1])
    for i in range(1,std_nbr):
        column4.append(np.mean(final_value_file_df["raw_value_dD"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
        column4.append(np.std(final_value_file_df["raw_value_dD"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
    for i in range(0,len(std_uncheck)):
        column4.append(residuals_std[1][i])
        column4.append(std_values[i][1])
        column4.append(round(residuals_std[1][i]-std_values[i,1],4))
    if protocol_type==1 or protocol_type==3:
        column5=["","","","","",""]
        if protocol_type==1:
            column5.append("MC d17O")
            for i in range(len(MCs["d17O"])-1):
                column5.append("")
        if protocol_type==3:
            column5.append("single_factor d17O")
            column5.append("alpha d17O")
            column5.append("beta d17O")
            column5.append("balance d17O")    
        column5.append("slope d17O")
        column5.append("intercept d17O")
        for i in range(1,std_nbr):
            column5.append("STD "+str(i+1)+" avg d17O")
            column5.append("STD "+str(i+1)+" std dev d17O")
        for i in range(0,len(std_uncheck)):
            column5.append("STD "+str(std_uncheck[i]+1)+" measured d17O")
            column5.append("STD "+str(std_uncheck[i]+1)+" true d17O")
            column5.append("STD "+str(std_uncheck[i]+1)+" residuals d17O")    
        column6=["","","","","",""]
        if  protocol_type==1:
            for i in range(len(MCs["d17O"])):
                column6.append(MCs["d17O"][i])
        if protocol_type==3:
            column6.append(single_factor_mean[2])
            for i in range(0,3):
                column6.append(exp_params[i,2])
        column6.append(calibration_param_list[0][2])
        column6.append(calibration_param_list[1][2])
        for i in range(1,std_nbr):
            column6.append(np.mean(final_value_file_df["raw_value_d17O"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
            column6.append(np.std(final_value_file_df["raw_value_d17O"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std]))
        for i in range(0,len(std_uncheck)):
            column6.append(residuals_std[2][i])
            column6.append(std_values[i][2])
            column6.append(round(residuals_std[2][i]-std_values[i,20],4))
    column1=np.reshape(column1,(len(column1),1))
    column2=np.reshape(column2,(len(column2),1))
    column3=np.reshape(column3,(len(column3),1))
    column4=np.reshape(column4,(len(column4),1))
    concat=np.concatenate((column1,column2,column3,column4),axis=1)
    df_tosave=pd.DataFrame(data=concat,columns=["col1","col2","col3","col4"])
    if protocol_type==1 or protocol_type==3:
        column5=np.reshape(column5,(len(column5),1))
        column6=np.reshape(column6,(len(column6),1))
        concat=np.concatenate((column1,column2,column3,column4,column5,column6),axis=1)
        df_tosave=pd.DataFrame(data=concat,columns=["col1","col2","col3","col4","col5","col6"])   
    df_tosave.to_csv(directory_path+filename+"_std_parameters"+save_extension,index=False,sep=",")
    return
# Function to save samples results in a csv file 

def save_sample_results_file(spl_results,filename,protocol_type,directory_path):
    """
    Format the samples results and then save it in a file

    Parameters
    ----------
    spl_results : list
        Mean and standard deviation for all samples 
    filename : str
        Name of the input file. (without extension)
    protocol_type : int
        Which method of correction is used 
    directory_path : str
        Folder where the results files will be saved 

    Returns
    -------
    None. Only save the sample results file

    """
    data_understood_pd=[]
    if protocol_type==0 or protocol_type==2:
        for i in range(0,len(spl_results[0])):
            data_understood_pd.append([spl_results[0][i],spl_results[1][i],spl_results[2][i],spl_results[3][i],spl_results[4][i]]) 
        df_tosave=pd.DataFrame(data=data_understood_pd,columns=["Sample_name","avg_d18O","std_dev_d18O","avg_dD","std_dev_dD"])
    if protocol_type==1 or protocol_type==3:
        for i in range(0,len(spl_results[0])):
            data_understood_pd.append([spl_results[0][i],spl_results[1][i],spl_results[2][i],spl_results[3][i],spl_results[4][i],spl_results[5][i],spl_results[6][i]])
        df_tosave=pd.DataFrame(data=data_understood_pd,columns=["Sample_name","avg_d18O","std_dev_d18O","avg_dD","std_dev_dD","avg_d17O","std_dev_d17O"])
    df_tosave["Flag"]=0
    for i in range(0,len(df_tosave)):
        if df_tosave["std_dev_d18O"].iloc[i]>0.06 or df_tosave["std_dev_dD"].iloc[i]>0.21 : # Change here the thresholds for flags of std dev on samples
            df_tosave["Flag"].iloc[i]=1  
        if protocol_type==1 or protocol_type==3:
            if df_tosave["std_dev_d17O"].iloc[i]>0.1:
                df_tosave["Flag"].iloc[i]=1 
    df_tosave.to_csv(directory_path+filename+"_spl_results"+save_extension,index=False,sep=",")
    return 

# Function to save control samples in a csv file 

def save_control_spl_file(known_sample_results,known_values,filename,protocol_type,directory_path):
    """
    Format the control samples results and then save it in a file  

    Parameters
    ----------
    known_sample_results : list 
        Mean and standard deviation for all spy samples
    known_values : numpy.array
        Stores the given ("true") values of the known samples
    filename : str
        Name of the input file. (without extension)
    protocol_type : int
        Which method of correction is used 
    directory_path : str
        Folder where the results files will be saved 

    Returns
    -------
    None. Only save the control sample results file

    """
    data_understood_pd=[]
    if protocol_type==0 or protocol_type==2:
        for i in range(0,len(known_sample_results[0])):
            residuals=known_sample_results[1][i]-known_values[i,0]
            residuals=round(residuals,2)
            residuals2=known_sample_results[3][i]-known_values[i,1]
            residuals2=round(residuals2,2)
            data_understood_pd.append([known_sample_results[0][i],known_sample_results[1][i],known_values[i,0],residuals,known_sample_results[0][i],known_sample_results[3][i],known_values[i,1],residuals2])
        df_tosave=pd.DataFrame(data=data_understood_pd,columns=["vials d18O","measured d18O","True d18O","residuals d18O","vials dD","measured dD","True dD","residuals dD"])
    if protocol_type==1 or protocol_type==3:
        for i in range(0,len(known_sample_results[0])):
            residuals=known_sample_results[1][i]-known_values[i,0]
            residuals=round(residuals,2)
            residuals2=known_sample_results[3][i]-known_values[i,1]
            residuals2=round(residuals2,2)
            residuals3=known_sample_results[5][i]-known_values[i,2]
            residuals3=round(residuals3,2)
            data_understood_pd.append([known_sample_results[0][i],known_sample_results[1][i],known_values[i,0],residuals,known_sample_results[0][i],known_sample_results[3][i],known_values[i,1],residuals2,known_sample_results[0][i],known_sample_results[5][i],known_values[i,2],residuals3])
        df_tosave=pd.DataFrame(data=data_understood_pd,columns=["vials d18O","measured d18O","True d18O","residuals d18O","vials dD","measured dD","True dD","residuals dD","vials d17O","measured d17O","True d17O","residuals d17O"])    
    df_tosave.to_csv(directory_path+filename+"_control_samples_results"+save_extension,index=False,sep=",")
    return

def save_result_file(final_value_file_df,filename,directory_path):
    """
    Save the result file 

    Parameters
    ----------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    filename : str
        Name of the input file. (without extension)
    directory_path : str
        Folder where the results files will be saved 

    Returns
    -------
    None. Only save the result file 

    """
    final_value_file_df.to_csv(directory_path+filename+"_final_file"+save_extension,index=False,sep=",")
    return 

def set_local():
    global saving_place
    saving_place="local"
    where_to_save.destroy()
    

def set_drive():
    global saving_place
    saving_place="drive"
    where_to_save.destroy()
    
def save_all_files(filename,spl_results,final_value_file_df,protocol_type,calibration_param_list,inj_per_std,page_results_2,MCs,single_factor_mean,exp_params,std_uncheck,operator_id,processor_id,option_protocol,std_nbr,starting_index_std,residuals_std,std_values,known_sample_results=None,known_values=None):
    """
    Wrapper to save all the files 

    Parameters
    ----------
    filename : str
        Name of the input file. (without extension)
    spl_results : list
        Mean and standard deviation for all samples 
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    protocol_type : int
        Which method of correction is used 
    calibration_param_list : list
        Calibration curve parameters
    inj_per_std : int
        Injections per standard
    page_results_2 :  tkinter.Toplevel()
        Second result page
    MCs : dict
        Contains the Memory coefficients after optimization
    single_factor_mean : list, optional
        Contains the single factor values for each isotope
    exp_params : list, optional
        Contains the alpha, beta and balance values used in the Gröning correction
    std_uncheck : list
        List of index of standards not used for calibration
    operator_id : str
        Name of the person who performed the measurements 
    processor_id : str
        Name of the person who processed the file 
    option_protocol : tk.StingVar()
        Contains the name of the correction method used
    std_nbr : int
        Number of standards
    starting_index_std : int
        Index corresponding to removed injection for standard 
    residuals_std : list
        Mean values of standards not used for calibration
    std_values : numpy.array
        Stores the given ("true") values of the standards 
    known_sample_results : list, optional 
        Mean and standard deviation for all spy samples
    known_values : numpy.array, optional 
        Stores the given ("true") values of the known samples

    Returns
    -------
    None.  

    """
    global where_to_save, saving_place
    saving_place=""
    directory_path=""
    saved=0
    where_to_save=tk.Toplevel(page_results_2)
    where_to_save_width = 330
    where_to_save_height = 110
    x = int(int(where_to_save.winfo_screenwidth()/2) - int(where_to_save_width/2))
    y = int(int(where_to_save.winfo_screenheight()/2) - int(where_to_save_height/2))
    where_to_save.geometry(f"{where_to_save_width}x{where_to_save_height}+{x}+{y}")
    where_to_save.title("location of save")
    frame_1=tk.Frame(where_to_save,bg="white",height=70,width=330)
    frame_1.place(relx=0,rely=0)
    img=PIL.Image.open("GUI_images/question_mark.png")
    img1=img.resize((40, 40))
    image_1=PIL.ImageTk.PhotoImage(img1)
    label_1=tk.Label(where_to_save, image = image_1,height=50,width=50,bg="white")
    label_1.image=image_1 # to keep a reference see https://web.archive.org/web/20201111190625/http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    label_1.place(relx=0.05,rely=0.1)
    label_2=tk.Label(where_to_save, text="Where do you want to save your results ?",font=("Calibri", 10),bg="white")
    label_2.place(relx=0.25, rely=0.25)
    local_saving=tk.Button(where_to_save,text="Local folder",bg="white",font=("Calibri", 9),command=set_local)
    local_saving.place(relx=0.3,rely=0.7)
    drive_saving=tk.Button(where_to_save,text="Google Drive folder",bg="white",font=("Calibri", 9),command=set_drive)
    drive_saving.place(relx=0.6,rely=0.7)
    where_to_save.transient(page_results_2)
    where_to_save.grab_set()
    page_results_2.wait_window(where_to_save)
    if saving_place=="local":
        directory_path=filedialog.askdirectory(parent=page_results_2)
        directory_path=directory_path+"/"
        saved=1
    if saving_place=="drive":
        directory_path="./files/saving_temp/"
        saved=1
    if saved==1:
        if type(known_sample_results)==list:
            save_control_spl_file(known_sample_results, known_values, filename,protocol_type,directory_path)
        save_result_file(final_value_file_df, filename,directory_path)
        save_sample_results_file(spl_results, filename,protocol_type,directory_path)
        if protocol_type==0 or protocol_type==1:
            save_std_parameters_file(calibration_param_list,inj_per_std,std_uncheck,final_value_file_df,operator_id,processor_id,std_nbr,starting_index_std,residuals_std,std_values,protocol_type,filename,directory_path,option_protocol,MCs=MCs)
        if protocol_type==2 or protocol_type==3:
            save_std_parameters_file(calibration_param_list, inj_per_std, std_uncheck, final_value_file_df, operator_id, processor_id, std_nbr, starting_index_std, residuals_std, std_values, protocol_type, filename, directory_path, option_protocol,single_factor_mean=single_factor_mean,exp_params=exp_params)
        if saving_place=="drive":
            files_to_upload=os.listdir("./files/saving_temp/")
            for file in files_to_upload:
                google_api.upload_files("./files/saving_temp", file)
        tk.messagebox.showinfo("Information","Data Saved",parent=page_results_2)
    return