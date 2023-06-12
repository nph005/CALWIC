# -*- coding: utf-8 -*-
"""
Created on Friday July 22 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""
import numpy as np
import scipy.stats as stats
import pandas as pd 

# Function that create the true vector and the measured for normalisation (Van Geldern method)
 
def create_normalisation_vector(iso_type,std_idx_norm,std_values,inj_per_std,result_file_df,removed_inj_per_std,k):
    """
    Generate two vectors one containing the measured standards values,
    the other one contains the true values of the standards.

    Parameters
    ----------
    iso_type : str
        Type of isotope (d18O, dD, d17O) 
    std_idx_norm : list
        list of index of standards used for calibration
    std_values : numpy.array
        Stores the given ("true") values of the standards 
    inj_per_std : int
        Injections per standard
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    removed_inj_per_std : int
        Removed injection per standard
    k : int
        index loop (dummy variable)

    Returns
    -------
    true_vector : np.array()
        Array with "given" values of standards
    measured_vector : np.array()
        Array with measured values of standards

    """
    true_vector=np.array([std_values[std_idx_norm[0],k]]*(inj_per_std-removed_inj_per_std))
    measured_vector=np.array([result_file_df["MC_corr"+iso_type].iloc[std_idx_norm[0]*inj_per_std+removed_inj_per_std:std_idx_norm[0]*inj_per_std+inj_per_std]])
    for i in range(1,len(std_idx_norm)):
        true_vector_temp=np.array([std_values[std_idx_norm[i],k]]*(inj_per_std-removed_inj_per_std))
        true_vector=np.concatenate((true_vector,true_vector_temp))
        measured_vector_temp=np.array([result_file_df["MC_corr"+iso_type].iloc[std_idx_norm[i]*inj_per_std+removed_inj_per_std:std_idx_norm[i]*inj_per_std+inj_per_std]])
        measured_vector=np.append(measured_vector,measured_vector_temp)
    return true_vector, measured_vector

# Function that create the true vector and the measured for normalisation (Groning method)

def create_normalisation_vector_groning(iso_type,std_idx_norm,std_values,inj_per_std,result_file_df,removed_inj_per_std,k):  
    measured_vector=np.array([])
    true_vector=np.array([])
    for i in std_idx_norm:
        name_idf1_std=result_file_df["Identifier 1"].iloc[i*inj_per_std]
        for j in range(0,len(result_file_df)):
            if name_idf1_std==result_file_df["Identifier 1"].iloc[j]:
                measured_vector=np.append(measured_vector,result_file_df["MC_corr"+iso_type].iloc[j])
                true_vector=np.append(true_vector,std_values[i,k])
    return true_vector, measured_vector

# Function that calculate parameters of normalisation curve

def normalisation_curve_calc(iso_type,true_vector,measured_vector):
    """
    Calculate slope and intercept of the calibration curve

    Parameters
    ----------
    iso_type :str
        Type of isotope (d18O, dD, d17O) 
    true_vector : np.array()
        Array with "given" values of standards
    measured_vector : np.array()
        Array with measured values of standards

    Returns
    -------
    slope : float
        Slope of the calibration curve 
    intercept : float 
        Intercept of the calibration curve

    """
    normalisation_curve=stats.linregress(measured_vector, true_vector)
    slope=normalisation_curve[0]
    intercept=normalisation_curve[1]
    slope=round(slope,3)
    intercept=round(intercept,3)
    return slope,intercept

# Function that calculate the final values (after memory correction and normalisation)

def final_value_calculation(corrected_file_df,iso_type,slope,intercept):
    """
    Calibrate all the data file

    Parameters
    ----------
    corrected_file_df : pandas.DataFrame
        DataFrame with memory corrected columns
    iso_type :str
        Type of isotope (d18O, dD, d17O)
    slope : float
        Slope of the calibration curve 
    intercept : float 
        Intercept of the calibration curve

    Returns
    -------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction

    """
    final_value_file_df=corrected_file_df
    final_value_file_df["final_value_"+iso_type]=corrected_file_df["MC_corr"+iso_type]*slope+intercept
    for i in range(0,len(final_value_file_df)):
        if final_value_file_df["MC_corr"+iso_type].iloc[i]==final_value_file_df["raw_value_"+iso_type].iloc[i]:
            final_value_file_df["final_value_"+iso_type].iloc[i]=final_value_file_df["raw_value_"+iso_type].iloc[i]
    return final_value_file_df   

# Function to calculate the deuterieum excess on the calibrated values 

def d_excess_calc(final_value_file_df):
    final_value_file_df["final_value_d-excess"]=final_value_file_df["final_value_dD"]-8*final_value_file_df["final_value_d18O"]
    return final_value_file_df

# Function to calculate the 17O excess on the calibrated values 

def O17_excess_calc(final_value_file_df):
    final_value_file_df["final_value_17O_excess"]=np.log(final_value_file_df["final_value_d17O"]/1000+1)-0.528*np.log(final_value_file_df["final_value_d18O"]/1000+1)
    return final_value_file_df

# Function to raise a flag if humidity is too low or too high 

def flags(final_value_file_df,iso_type_list,inj_per_std,std_nbr):
    """
    Add a column with a flag on humidity if it's too low or too high 
    and an another one to see if the values have been corrected. 

    Parameters
    ----------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction

    Returns
    -------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction

    """
    final_value_file_df["Hum Flag"]=""
    final_value_file_df["Hum Flag"]=0
    for i in range(0,len(final_value_file_df)):
        if final_value_file_df["H2O_Mean"].iloc[i]>23000 or final_value_file_df["H2O_Mean"].iloc[i]<17000:
            final_value_file_df["Hum Flag"].iloc[i]=1
    final_value_file_df["Correction Flag"]=1
    for iso_type in iso_type_list:
        for i in range(0,len(final_value_file_df)):
            if pd.isna(final_value_file_df["final_value_"+iso_type].iloc[i])==True:
                final_value_file_df["Correction Flag"].iloc[i]=0 
        final_value_file_df["Correction Flag"].iloc[0:inj_per_std]=0
        for i in range(std_nbr*inj_per_std,len(final_value_file_df)):
            if final_value_file_df["MC_corr"+iso_type].iloc[i]==final_value_file_df["raw_value_"+iso_type].iloc[i]:
                final_value_file_df["Correction Flag"].iloc[i]=2
    return final_value_file_df

# Function to save calibration curve parameters 

def calibration_curve_values(slope,intercept,calibration_param_list):
    """
    Save the calibration parameters into one list

    Parameters
    ----------
    slope : float
        Slope of the calibration curve 
    intercept : float 
        Intercept of the calibration curve
    calibration_param_list : list
        Calibration curve parameters

    Returns
    -------
    calibration_param_list : list
        Calibration curve parameters

    """
    calibration_param_list[0].append(slope)
    calibration_param_list[1].append(intercept)
    return calibration_param_list

# Function to save the calibration vectors (for plotting)

def calibration_vectors_values(measured_vector, true_vector, calibration_vectors):
    """
    Save the calibration vectors inot one list 

    Parameters
    ----------
    measured_vector : np.array()
        Array with measured values of standards
    true_vector : np.array()
        Array with "given" values of standards
    calibration_vectors : list
        Calibration values list

    Returns
    -------
    calibration_vectors : list
        Calibration values list

    """
    calibration_vectors[0].append(measured_vector)
    calibration_vectors[1].append(true_vector)
    return calibration_vectors

# Function to wrap all the calibration 

def wrapper_calibration(corrected_file_df,iso_type_list,std_idx_norm,std_values,inj_per_std,result_file_df,removed_inj_per_std,std_nbr,protocol_type):
    """
    Wrapper for the calibration

    Parameters
    ----------
    corrected_file_df : pandas.DataFrame
        DataFrame with memory corrected columns
    iso_type_list : list
        List of isotopes 
    std_idx_norm : list
        list of index of standards used for calibration
    std_values : numpy.array
        Stores the given ("true") values of the standards 
    inj_per_std : int
        Injections per standard
    result_file_df : pandas.DataFrame
        DataFrame from the input file
    removed_inj_per_std : int
        Removed injection per standard    
     
    Returns
    -------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    calibration_param_list : list
        Calibration curve parameters
    calibration_vectors : list
        Calibration values list

    """
    calibration_param_list=[[],[]]
    calibration_vectors=[[],[]]
    for k,iso_type in enumerate(iso_type_list):
        true_vector=[]
        measured_vector=[]
        if protocol_type==0 or protocol_type==1:
            true_vector,measured_vector=create_normalisation_vector(iso_type, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std, k)
        if protocol_type==2 or protocol_type==3:
            true_vector,measured_vector=create_normalisation_vector_groning(iso_type, std_idx_norm, std_values, inj_per_std, result_file_df, removed_inj_per_std, k)
        slope,intercept=normalisation_curve_calc(iso_type, true_vector, measured_vector)
        final_value_file_df=final_value_calculation(corrected_file_df, iso_type, slope, intercept)
        calibration_param_list=calibration_curve_values(slope, intercept, calibration_param_list)
        calibration_vectors=calibration_vectors_values(measured_vector, true_vector, calibration_vectors)
    final_value_file_df=d_excess_calc(final_value_file_df)
    if "d17O" in iso_type_list:
        final_value_file_df=O17_excess_calc(final_value_file_df)
    final_value_file_df=flags(final_value_file_df,iso_type_list,inj_per_std,std_nbr)
    return final_value_file_df,calibration_param_list,calibration_vectors