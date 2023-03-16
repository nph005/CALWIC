# -*- coding: utf-8 -*-
"""
Created on Thu Dec 1  2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

import numpy as np 
from scipy.optimize import minimize,Bounds
import pandas as pd 

# Function to calulate the fist injection of each standard/sample 

def create_first_injections_values(result_file_df,iso_type_list):
    first_injections=[[],[],[]]
    for i,iso_type in enumerate(iso_type_list):
        for j in range(0,len(result_file_df)-1):
            if result_file_df["Inj Nr"].iloc[j]==1:
                first_injections[i].append(result_file_df["raw_value_"+iso_type].iloc[j])
    return first_injections

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
            if result_file_df["Inj Nr"].iloc[j]>result_file_df["Inj Nr"].iloc[j+1]:
                last_injections[i].append(result_file_df["raw_value_"+iso_type].iloc[j])
        last_injections[i].append(result_file_df["raw_value_"+iso_type].iloc[-1])
    return last_injections

# Function to calculate f on a list shape

def calculate_single_factor(first_injections,last_injections,iso_length):
    f_list=[[],[],[]]
    single_factor_mean=[]
    limits=[0.4,4,0.4]
    for j in range(iso_length):
        for i in range(1,len(first_injections[0])):
            a1=last_injections[j][i] - last_injections[j][i-1]
            a2=last_injections[j][i] - first_injections[j][i]
            f_temp=a2/a1
            f=f_temp*(1-f_temp-f_temp*f_temp)
            if f>0 and np.abs(a1)>2*limits[j]:
                f_list[j].append(f)
    for i in range(iso_length):
        single_factor_mean.append(np.nanmean(f_list[i]))
    return single_factor_mean

# Function to perfom first memory correction 

def single_factor_memory_correction(single_factor_mean,iso_type, result_file_df,iso_number):
    result_file_df["MC_corr"+iso_type]=result_file_df["raw_value_"+iso_type]
    for i in range(3,len(result_file_df)):
        result_file_df["MC_corr"+iso_type].iloc[i]=result_file_df["raw_value_"+iso_type].iloc[i]+single_factor_mean[iso_number]*(result_file_df["raw_value_"+iso_type].iloc[i]-result_file_df["raw_value_"+iso_type].iloc[i-1])+single_factor_mean[iso_number]**2*(result_file_df["raw_value_"+iso_type].iloc[i]-result_file_df["raw_value_"+iso_type].iloc[i-2])+single_factor_mean[iso_number]**3*(result_file_df["raw_value_"+iso_type].iloc[i]-result_file_df["raw_value_"+iso_type].iloc[i-3])
    return result_file_df
    
# Function to perform exponential memory correction 

def exp_memory_correction(groning_params,last_injections,result_file_df,iso_type,inj_per_std,iso_number):
    k=iso_number
    alpha=groning_params[k][0]
    beta=groning_params[k][1]
    balance=groning_params[k][2]
    j=0
    for i in range(inj_per_std,len(result_file_df)):
        inj_nbr=result_file_df["Inj Nr"].iloc[i]
        if result_file_df["Inj Nr"].iloc[i]<result_file_df["Inj Nr"].iloc[i-1]:
            j=j+1      
        corr1=((result_file_df["MC_corr"+iso_type].iloc[i]-last_injections[k][j])/(last_injections[k][j-1]-last_injections[k][j]))*100
        corr=corr1*(balance*np.exp(-alpha*(inj_nbr-1)) + (1-balance)*(np.exp(-beta*(inj_nbr-1))))
        result_file_df["MC_corr"+iso_type].iloc[i]=result_file_df["MC_corr"+iso_type].iloc[i]-corr*((last_injections[k][j-1]-last_injections[k][j])/100)
    return result_file_df

# Function to perform exponential memory correction when adjusting parameters

def exp_memory_correction_minimize(groning_params,last_injections,result_file_df,iso_type,inj_per_std,iso_number):
    k=iso_number
    alpha=groning_params[0]
    beta=groning_params[1]
    balance=groning_params[2]
    j=0
    for i in range(inj_per_std,len(result_file_df)):
        inj_nbr=result_file_df["Inj Nr"].iloc[i]
        if result_file_df["Inj Nr"].iloc[i]<result_file_df["Inj Nr"].iloc[i-1]:
            j=j+1      
        corr1=((result_file_df["MC_corr"+iso_type].iloc[i]-last_injections[k][j])/(last_injections[k][j-1]-last_injections[k][j]))*100
        corr=corr1*(balance*np.exp(-alpha*(inj_nbr-1)) + (1-balance)*(np.exp(-beta*(inj_nbr-1))))
        result_file_df["MC_corr"+iso_type].iloc[i]=result_file_df["MC_corr"+iso_type].iloc[i]-corr*((last_injections[k][j-1]-last_injections[k][j])/100)
    return result_file_df



# Function to minimize, b is balance term a and c are terms in each exponetial term
 
def function_to_minimize_exp(parameters,result_file_df,first_injections,last_injections,iso_type,inj_per_std,iso_length,iso_number):
    X=result_file_df
    single_factor_mean=calculate_single_factor(first_injections, last_injections, iso_length)
    X=single_factor_memory_correction(single_factor_mean,iso_type, result_file_df,iso_number)
    X=exp_memory_correction_minimize(parameters,last_injections,result_file_df,iso_type,inj_per_std,iso_number)
    cost_function=0
    j=0
    k=iso_number
    for i in range(inj_per_std,len(result_file_df)):
        if result_file_df["Inj Nr"].iloc[i]<result_file_df["Inj Nr"].iloc[i-1]:
            j=j+1
        cost_function=cost_function+np.abs(X["MC_corr"+iso_type].iloc[i]-last_injections[k][j])
    return cost_function

def exponential_optimisation(result_file_df,first_injections,last_injections,iso_type,inj_per_std,iso_length,iso_number):
    initial_guess=np.array([1.1,0.2,0.76])
    bounds=Bounds([-np.inf,-np.inf,0],[np.inf,np.inf,1])
    arguments=(result_file_df,first_injections,last_injections,iso_type,inj_per_std,iso_length,iso_number)
    res=minimize(fun=function_to_minimize_exp,x0=initial_guess,method="nelder-mead",args=arguments,bounds=bounds,options={"disp":True,"maxiter":100})
    return res.x 

# Function to wrap Gröning method 

def wrapper_memory_correction_groning_method(iso_type_list,result_file_df,len_std_injections,groning_params, inj_per_std):
    first_injections=create_first_injections_values(result_file_df, iso_type_list)
    last_injections=create_last_injections(result_file_df, iso_type_list)
    iso_length=len(iso_type_list)
    single_factor_mean=calculate_single_factor(first_injections, last_injections, iso_length)
    #groning_params=[[],[],[]]
    #TODO make this function work 
    #for i,iso_type in enumerate(iso_type_list):
    #   result=exponential_optimisation( result_file_df,first_injections,last_injections,iso_type,inj_per_std,iso_length,i)  
    #   groning_params[i].append(result)
    for i,iso_type in enumerate(iso_type_list):
        first_corrected_file_df=single_factor_memory_correction(single_factor_mean, iso_type, result_file_df, i)
        corrected_file_df=exp_memory_correction(groning_params, last_injections, first_corrected_file_df, iso_type, inj_per_std,i)
    exp_params=groning_params
    return corrected_file_df, single_factor_mean, exp_params


def wrapper_memory_correction_groning_method_d17O(iso_type_list,result_file_df,len_std_injections,groning_params, inj_per_std):
    first_injections=create_first_injections_values(result_file_df, iso_type_list)
    last_injections=create_last_injections(result_file_df, iso_type_list)
    iso_length=len(iso_type_list)
    single_factor_mean=calculate_single_factor(first_injections, last_injections, iso_length)
    for i,iso_type in enumerate(iso_type_list):
        first_corrected_file_df=single_factor_memory_correction(single_factor_mean, iso_type, result_file_df, i)
        corrected_file_df=exp_memory_correction(groning_params,last_injections, first_corrected_file_df, iso_type, inj_per_std,i)
    exp_params=groning_params
    return corrected_file_df, single_factor_mean, exp_params
