# -*- coding: utf-8 -*-
"""
Created on Friday July 22 2022

@author: @author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses

This is the memory correction following van Geldern method (memory coefficient).
"""

# import of packages 

import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
import pandas as pd 

################################ common part ################################

#Function to create pure values (pure values beeing the last injection of the last sample/standard)

def create_last_injections(result_file_df,iso_type_list):
    """
    Create list of last injections of each standard and sample

    Parameters
    ----------
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    iso_type_list : list
        List of isotopes 

    Returns
    -------
    last_injections : list
        Contains every last injection

    """
    last_injections=[[],[],[]]
    for i,iso_type in enumerate(iso_type_list):
        for j in range(0,len(result_file_df)-1):
            if result_file_df.loc[j,"Inj Nr"]>result_file_df.loc[j+1,"Inj Nr"]:
                last_injections[i].append(result_file_df.loc[j,"raw_value_"+iso_type])
    return last_injections


#F unction that defines the constraints and bounds for non linear optimization 

def define_constraints_and_bounds(MC,inj_per_std):
    """
    Define constraints and bounds for the calculation of memory coefficients. 

    Parameters
    ----------
    MC : numpy.array()
        Memory coefficients
    inj_per_std : int
        Injections per standard

    Returns
    -------
    bounds : scipy.optimize.Bounds
        Upper and lower boundaries for memory coefficients
    cons : list
        Contains all constraints for optimization

    """
    cons=[]
    for i in range(0,inj_per_std):
        ineq1={"type":"ineq","fun":lambda MC,j=i:MC[j]}
        ineq2={"type":"ineq","fun":lambda MC,j=i:1-MC[j]} 
        ineq3={"type":"ineq","fun":lambda MC,j=i:1-MC[j]}
        ineq4={"type":"ineq","fun":lambda MC,j=i,h=i-1:-MC[h]+MC[j]}
        if i==0:
            ineq4={"type":"ineq","fun":lambda MC,j=i:MC[j]}
        if i==inj_per_std:
            ineq3={"type":"ineq","fun":lambda MC,j=i:-1+MC[j]}
        cons.append(ineq1)
        cons.append(ineq2)
        cons.append(ineq3)
        cons.append(ineq4)
    lbound=np.array([0]*inj_per_std)
    ubound=np.array([1]*inj_per_std)
    bounds=Bounds(lbound,ubound)
    return bounds,cons

# Function that must be minimised for non linear optimisation, X is the raws data 

def function_to_minimize(MC,X,last_injections,len_std_injections,inj_per_std,iso_type,iso_number,std_nbr,idx_std_to_use):
    """
    Calculation of combined standard deviation for standards. 

    Parameters
    ----------
    MC : list
        List of memory coefficients
    X : list
        Raw values measured for standards
    last_injections : list
        Contains every last injection
    len_std_injections : int
        Total number of injections for standards
    inj_per_std : int
        Injections per standard
    iso_type : str
        Type of isotope (d18O, dD, d17O) 
    iso_number : int
        Index in the iso_type_list
    std_nbr : int
        Number of standards

    Returns
    -------
    f : float
        Combined standard deviation

    """
    std_dev_list=[]
    count=0
    if len(idx_std_to_use)==len_std_injections:
        count=1
        for i in range(1,std_nbr):
            std_dev_list.append(np.std(X[inj_per_std*i:inj_per_std*i+inj_per_std]+(1-MC)*(X[inj_per_std*i:inj_per_std*i+inj_per_std]-last_injections[iso_number][i-1])))
    if len(idx_std_to_use)%inj_per_std==0 and count==0:
    
        X=X[idx_std_to_use]
        for i in range(1,int(len(idx_std_to_use)/inj_per_std)):
            h=idx_std_to_use[i*inj_per_std:inj_per_std*i+inj_per_std]
            temp=X[h]
            std_dev_list.append(np.std(temp[h]+(1-MC)*(temp[h]-last_injections[iso_number][i-1])))
    if len(idx_std_to_use)==len_std_injections-1:
        h=np.where((np.diff(idx_std_to_use)==2))[0]+1
        temp=X
        temp[h]=np.nan
        for i in range(1,std_nbr):
            std_dev_list.append(np.nanstd(temp[inj_per_std*i:inj_per_std*i+inj_per_std]+(1-MC)*(temp[inj_per_std*i:inj_per_std*i+inj_per_std]-last_injections[iso_number][i-1])))
    f=np.sqrt(np.sum(np.square(std_dev_list)))
    return f

# Function to do the non-linear optimisation 

def non_linear_optimisation(inj_per_std,cons,bounds,last_injections,MC,result_file_df,len_std_injections,iso_type,iso_number,std_nbr,idx_std_to_use):
    """
    Optimize Memory coefficients to minimise the combined standard deviation

    Parameters
    ----------
    inj_per_std : int
        Injections per standard
    cons : list
        Contains all constraints for optimization
    bounds : scipy.optimize.Bounds
        Upper and lower boundaries for memory coefficients
    last_injections : list
        Contains every last injection
    MC : list
        List of memory coefficients
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    len_std_injections : int
        Total number of injections for standards
    iso_type : str
        Type of isotope (d18O, dD, d17O)
    iso_number : int
        Index in the iso_type_list
    std_nbr : int
        Number of standards
    idx_std_to_use : list
        Index of injections to use to calculate Memory coefficients VG
    Returns
    -------
    new_MC : list
        List of memory coefficient after optimization

    """
    initial_guess=np.ones((inj_per_std))
    X=result_file_df[result_file_df.index<=len_std_injections]["raw_value_"+iso_type]
    arguments=(X,last_injections,len_std_injections,inj_per_std,iso_type,iso_number,std_nbr,idx_std_to_use)
    res=minimize(fun=function_to_minimize, x0=initial_guess,method='COBYLA',args=arguments,constraints=cons,options={"disp":False,"maxiter":1000,"rhobeg":0.001}) 
    new_MC=res.x
    return new_MC

#Function that calculate the deltas values after memory correction 

def delta_calc_MC(MC,last_injections,result_file_df,inj_per_std,iso_type,iso_number):
    """
    Calculate the new values after memory correction

    Parameters
    ----------
    MC : list
        List of memory coefficients
    last_injections : list
        Contains every last injection
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    inj_per_std : int
        Injections per standard
    iso_type : str
        Type of isotope (d18O, dD, d17O)
    iso_number : int
        Index in the iso_type_list

    Returns
    -------
    result_file_df :  pandas.DataFrame
        DataFrame from the input file with memory corrected columns

    """
    result_file_df["MC_corr"+iso_type]=result_file_df["raw_value_"+iso_type]
    j=-1
    for i in range(inj_per_std,len(result_file_df)):
        if result_file_df.loc[i,"Inj Nr"]<result_file_df.loc[i-1,"Inj Nr"]:
            j=j+1
        inj_nbr=result_file_df.loc[i,"Inj Nr"]-1
        if pd.isna(last_injections[iso_number][j])!=True:
            result_file_df.loc[i,"MC_corr"+iso_type]=result_file_df.loc[i,"raw_value_"+iso_type]+(1-MC[inj_nbr])*(result_file_df.loc[i,"raw_value_"+iso_type]-last_injections[iso_number][j])           
    return result_file_df

####################### wrapper for Van Geldern method #######################

def wrapper_memory_coefficient_van_geldern(iso_type_list,MC_one,inj_per_std,last_injections,result_file_df,len_std_injections,std_nbr,idx_std_to_use):
    """
    Wrapp all the Van Geldern method (d18O, dD)

    Parameters
    ----------
    iso_type_list : list
        List of all isotopes to correct 
    MC_one : list
        Starting memory coefficients (all set to one)
    inj_per_std : int
        Injections per standard
    last_injections : list
        Contains every last injection
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    len_std_injections : int
        Total number of injections for standards
    std_nbr : int
        Number of standards
    idx_std_to_use : list
        Index of injections to use to calculate Memory coefficients VG
    Returns
    -------
    corrected_file_df : pandas.DataFrame
        DataFrame with memory corrected columns
    MCs : dict
        Contains the Memory coefficients after optimization 

    """
    bounds,cons=define_constraints_and_bounds(MC_one, inj_per_std)
    MCs={"d18O":[],"dD":[]}
    for i,iso_type in enumerate(iso_type_list):
        MCs[iso_type]=non_linear_optimisation(inj_per_std, cons, bounds, last_injections, MC_one, result_file_df, len_std_injections, iso_type, i,std_nbr,idx_std_to_use)
        corrected_file_df=delta_calc_MC(MCs[iso_type],last_injections,result_file_df,inj_per_std,iso_type,i)
    return corrected_file_df,MCs

##################### wrapper for van Geldern d17O method #####################

def wrapper_memory_coefficient_van_geldern_d17O(iso_type_list,MC_one,inj_per_std,last_injections,result_file_df,len_std_injections,std_nbr,idx_std_to_use):
    """
    Wrapp all the Van Geldern method (d18O, dD,d17O)

    Parameters
    ----------
    iso_type_list : list
        List of all isotopes to correct 
    MC_one : list
        Starting memory coefficients (all set to one)
    inj_per_std : int
        Injections per standard
    last_injections : list
        Contains every last injection
    result_file_df : pandas.DataFrame
        DataFrame from the input file 
    len_std_injections : int
        Total number of injections for standards
    std_nbr : int
        Number of standards
    idx_std_to_use : list
        Index of injections to use to calculate Memory coefficients VG
    Returns
    -------
    corrected_file_df : pandas.DataFrame
        DataFrame with memory corrected columns
    MCs : dict
        Contains the Memory coefficients after optimization 

    """
    bounds,cons=define_constraints_and_bounds(MC_one, inj_per_std)
    MCs={"d18O":[],"dD":[],"d17O":[]}
    for i,iso_type in enumerate(iso_type_list):
        MCs[iso_type]=non_linear_optimisation(inj_per_std, cons, bounds, last_injections, MC_one, result_file_df, len_std_injections, iso_type, i,std_nbr,idx_std_to_use)
        corrected_file_df=delta_calc_MC(MCs[iso_type],last_injections,result_file_df,inj_per_std,iso_type,i)
    return corrected_file_df,MCs