# -*- coding: utf-8 -*-
"""
Created on Tuesday May 3 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

# imports of packages 
import numpy as np 
import scipy.stats as stats


# Function to calculate parameters after memory correction (slope, p-value, avg, std dev)

def calculate_parameters_standards(final_value_file_df,protocol_type,starting_index_std,std_nbr,inj_per_std,removed_inj_per_std,iso_type_list):
    """
    Calculate standards parameters. Slope is the slope of each standrard 
    after Memory correction to see if there is a trend in the memory corrected data.
    P-value indicates if the trend is meaningfull (usually p-value must be below 5% 
                                                   or 0.05 for the slope to be meaningfull).

    Parameters
    ----------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    protocol_type : int
        Which method of correction is used 
    starting_index_std : int
        Index corresponding to removed injection for standard 
    std_nbr : int 
        Number of standards 
    inj_per_std : int
        Injections per standard
    removed_inj_per_std : int
        Removed injection per standard
    iso_type_list : list
        List of isotopes 

    Returns
    -------
    slopes_MC_list : list
        Slope of each standard formatted for the table_results_p1 needs
    p_values_MC_list : list
        p-value of each standard formatted for the table_results_p1 needs
    avg_std_list : list
        Mean of the raw data of each standard formatted for the table_results_p1 needs
    std_dev_std_list : list
        Standard deviation of the raw data of each standard formatted for the table_results_p1 needs
    std_col1_list : list
        Names to include in the first column of the Memory correction results in table _results_p1
    """
    
    slopes_MC_list=[]
    p_values_MC_list=[]
    avg_std_list=[]
    std_dev_std_list=[]
    std_col1_list=[]
    if protocol_type==0 or protocol_type==1:
        slopes_MC_list=[]
        p_values_MC_list=[]
    for i in range(1,std_nbr):
        std_col1_list.append("STD "+str(i+1))
        avg_std_list.append("")
        std_dev_std_list.append("")
        if protocol_type==0 or protocol_type==1:
            slopes_MC_list.append("")
            p_values_MC_list.append("")
        for iso_type in iso_type_list:
            avg_temp=np.mean(final_value_file_df["raw_value_"+iso_type].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std])
            avg_temp=round(avg_temp,3)
            std_dev_temp=np.std(final_value_file_df["raw_value_"+iso_type].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std])
            std_dev_temp=round(std_dev_temp,2)
            if iso_type=="d18O":
                std_col1_list.append("\u03B4\u00B9\u2078O")
            elif iso_type=="dD":
                std_col1_list.append("\u03B4D")
            elif iso_type=="d17O":
                std_col1_list.append("\u03B4\u00B9\u2077O")
            avg_std_list.append(avg_temp)
            std_dev_std_list.append(std_dev_temp)
            if protocol_type==0 or protocol_type==1:
                slope_temp,intercept,dum1,p_value_temp,dum2=stats.linregress(final_value_file_df["Inj Nr"].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std].to_numpy(),final_value_file_df["MC_corr"+iso_type].iloc[i*inj_per_std+starting_index_std:i*inj_per_std+inj_per_std].to_numpy())
                slope_temp=round(slope_temp,4)
                p_value_temp=round(p_value_temp,4)
                slopes_MC_list.append(slope_temp)
                p_values_MC_list.append(p_value_temp)
    if protocol_type==0 or protocol_type==1:
        return slopes_MC_list,p_values_MC_list,avg_std_list,std_dev_std_list,std_col1_list
    if protocol_type==2 or protocol_type==3:
        return avg_std_list,std_dev_std_list,std_col1_list

# Function to calculate standards residuals not used in calibration 

def calculate_residuals_standards(final_value_file_df, var_6_dict,std_values,inj_per_std,starting_index_std,protocol_type):
    """
    Calculate residuals on standards not used for calibration.
    Residuals std contains the mean measured values of theses standards.

    Parameters
    ----------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    var_6_dict : dictionary
        Dictionary storing the values of the CheckButtons on the standards' table
    std_values : numpy.array
        Stores the given ("true") values of the standards 
    inj_per_std : int
        Injections per standard
    starting_index_std : int
        Where to start the count (to eliminate the first standard used as a ricing one)
    protocol_type : int
        Which method of correction is used 
   

    Returns
    -------
    residuals_std : list
        Mean values of standards not used for calibration
    std_uncheck : list
        list of index of standards not used for calibration 

    """
    std_uncheck=[]
    for i,j in enumerate(var_6_dict):
        if var_6_dict[j].get()==0:
            std_uncheck.append(i+1)
    avg_std_18_list=[]
    avg_std_D_list=[]
    avg_std_17_list=[]
    for i in range(0,len(std_uncheck)):
        avg_std_18_temp=np.mean(final_value_file_df["final_value_d18O"].iloc[std_uncheck[i]*inj_per_std+starting_index_std:std_uncheck[i]*inj_per_std+inj_per_std])
        avg_std_18_temp=np.round(avg_std_18_temp,4)
        avg_std_18_list.append(avg_std_18_temp)
        avg_std_D_temp=np.mean(final_value_file_df["final_value_dD"].iloc[std_uncheck[i]*inj_per_std+starting_index_std:std_uncheck[i]*inj_per_std+inj_per_std])
        avg_std_D_temp=np.round(avg_std_D_temp,4)
        avg_std_D_list.append(avg_std_D_temp)
        if protocol_type==1:
            avg_std_17_temp=np.mean(final_value_file_df["final_value_d17O"].iloc[std_uncheck[i]*inj_per_std+starting_index_std:std_uncheck[i]*inj_per_std+inj_per_std])
            avg_std_17_temp=np.round(avg_std_17_temp,4)
            avg_std_17_list.append(avg_std_17_temp)
    residuals_std=[]
    residuals_std.append(avg_std_18_list)
    residuals_std.append(avg_std_D_list)
    if protocol_type==1:
        residuals_std.append(avg_std_17_list)
    return residuals_std,std_uncheck
    
# Function to calculate the avg and std dev of sample and residuals on known sample 

def calculate_spl_parameters(final_value_file_df,protocol_type,starting_index_spl,spl_nbr,inj_per_spl,len_std_injections,port_known_sample=None,idx_known_sample=None):
    """
    Calculate samples parameters (mean and standard deviation). This includes
    the samples and the spy samples (standards treated as samples)

    Parameters
    ----------
    final_value_file_df : pandas.DataFrame
        DataFrame with all correction
    protocol_type : int
        Which method of correction is used 
    starting_index_spl : int
        Index corresponding to removed injection for samples
    spl_nbr : int
        Samples number
    inj_per_spl : int 
        Injections per sample 
    len_std_injections : int 
        Total number of injections of standards
    port_known_sample : list, optional
        List of port for the spy samples. The default is None.
    idx_known_sample : list, optional
        Index of all injections for spy samples. The default is None.

    Returns
    -------
    spl_results : list
        Mean and standard deviation for all samples 
    known_sample_results : list 
        Mean and standard deviation for all spy samples  

    """
    avg_spl_18_list=[]
    std_dev_18_spl_list=[]
    avg_spl_D_list=[]
    std_dev_D_spl_list=[]
    avg_spl_17_list=[]
    std_dev_17_spl_list=[]
    avg_spl_d_excess_list=[]
    std_dev_d_excess_list=[]
    spl_name_list=[]
    avg_known_spl_18_list=[]
    std_dev_known_spl_18_list=[]
    avg_known_spl_D_list=[]
    std_dev_known_spl_D_list=[]
    avg_known_spl_17_list=[]
    std_dev_known_spl_17_list=[] 
    if idx_known_sample!=None:
        for i in range(0,spl_nbr):
            if any(len_std_injections+i*inj_per_spl+starting_index_spl==idx_known_spl for idx_known_spl in idx_known_sample):
                avg_k_spl_18_temp=np.mean(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_k_spl_18_temp=round(avg_k_spl_18_temp,4)
                avg_known_spl_18_list.append(avg_k_spl_18_temp)
                avg_k_spl_D_temp=np.mean(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_k_spl_D_temp=round(avg_k_spl_D_temp,4)
                avg_known_spl_D_list.append(avg_k_spl_D_temp)
                std_dev_18_temp=np.std(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_18_temp=round(std_dev_18_temp,4)
                std_dev_known_spl_18_list.append(std_dev_18_temp)
                std_dev_D_temp=np.std(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_D_temp=round(std_dev_D_temp,4)
                std_dev_known_spl_D_list.append(std_dev_D_temp)
                if protocol_type==1 or protocol_type==3:
                    avg_k_spl_17_temp=np.mean(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                    avg_k_spl_17_temp=round(avg_k_spl_17_temp,4)
                    avg_known_spl_17_list.append(avg_k_spl_17_temp)
                    std_dev_k_spl_17_temp=np.std(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                    std_dev_k_spl_17_temp=round(std_dev_k_spl_17_temp,4)
                    std_dev_known_spl_17_list.append(std_dev_k_spl_17_temp)         
            else: 
                avg_18_temp=np.mean(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_18_temp=round(avg_18_temp,4)
                avg_spl_18_list.append(avg_18_temp)
                avg_D_temp=np.mean(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_D_temp=round(avg_D_temp,4)
                avg_spl_D_list.append(avg_D_temp)
                avg_excess_temp=np.mean(final_value_file_df["final_value_d-excess"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_excess_temp=round(avg_excess_temp,4)
                avg_spl_d_excess_list.append(avg_excess_temp)
                if protocol_type==1 or protocol_type==3:
                    avg_17_temp=np.mean(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                    avg_17_temp=round(avg_17_temp,4)
                    avg_spl_17_list.append(avg_17_temp)
                    std_dev_17_temp=np.std(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                    std_dev_17_temp=round(std_dev_17_temp,4)
                    std_dev_17_spl_list.append(std_dev_17_temp)        
                std_dev_18_temp=np.std(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_18_temp=round(std_dev_18_temp,4)
                std_dev_18_spl_list.append(std_dev_18_temp)
                std_dev_D_temp=np.std(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_D_temp=round(std_dev_D_temp,4)
                std_dev_D_spl_list.append(std_dev_D_temp)
                std_dev_excess_temp=np.std(final_value_file_df["final_value_d-excess"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_excess_temp=round(std_dev_excess_temp,4)
                std_dev_d_excess_list.append(std_dev_excess_temp)
                spl_name_temp=final_value_file_df["Identifier 1"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl]
                spl_name_list.append(spl_name_temp)
        known_sample_results=[]
        known_sample_results.append(port_known_sample)
        known_sample_results.append(avg_known_spl_18_list)
        known_sample_results.append(std_dev_known_spl_18_list)
        known_sample_results.append(avg_known_spl_D_list)
        known_sample_results.append(std_dev_known_spl_D_list)
        spl_results=[]
        spl_results.append(spl_name_list)
        spl_results.append(avg_spl_18_list)
        spl_results.append(std_dev_18_spl_list)
        spl_results.append(avg_spl_D_list)
        spl_results.append(std_dev_D_spl_list) 
        if protocol_type==1 or protocol_type==3:
            known_sample_results.append(avg_known_spl_17_list)
            known_sample_results.append(std_dev_known_spl_17_list)
            spl_results.append(avg_spl_17_list)
            spl_results.append(std_dev_17_spl_list)
        spl_results.append(avg_spl_d_excess_list)
        spl_results.append(std_dev_d_excess_list)
    if idx_known_sample==None:
        for i in range(0,spl_nbr):
            avg_18_temp=np.mean(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            avg_18_temp=round(avg_18_temp,4)
            avg_spl_18_list.append(avg_18_temp)
            avg_D_temp=np.mean(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            avg_D_temp=round(avg_D_temp,4)
            avg_spl_D_list.append(avg_D_temp)
            avg_excess_temp=np.mean(final_value_file_df["final_value_d-excess"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            avg_excess_temp=round(avg_excess_temp,4)
            avg_spl_d_excess_list.append(avg_excess_temp)
            if protocol_type==1 or protocol_type==3:
                avg_17_temp=np.mean(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                avg_17_temp=round(avg_17_temp,4)
                avg_spl_17_list.append(avg_17_temp)
                std_dev_17_temp=np.std(final_value_file_df["final_value_d17O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
                std_dev_17_temp=round(std_dev_17_temp,4)
                std_dev_17_spl_list.append(std_dev_17_temp)        
            std_dev_18_temp=np.std(final_value_file_df["final_value_d18O"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            std_dev_18_temp=round(std_dev_18_temp,4)
            std_dev_18_spl_list.append(std_dev_18_temp)
            std_dev_D_temp=np.std(final_value_file_df["final_value_dD"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            std_dev_D_temp=round(std_dev_D_temp,4)
            std_dev_D_spl_list.append(std_dev_D_temp)
            std_dev_excess_temp=np.std(final_value_file_df["final_value_d-excess"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl:len_std_injections+i*inj_per_spl+inj_per_spl])
            std_dev_excess_temp=round(std_dev_excess_temp,4)
            std_dev_d_excess_list.append(std_dev_excess_temp)
            spl_name_temp=final_value_file_df["Identifier 1"].iloc[len_std_injections+i*inj_per_spl+starting_index_spl]
            spl_name_list.append(spl_name_temp)
            spl_results=[]
            spl_results.append(spl_name_list)
            spl_results.append(avg_spl_18_list)
            spl_results.append(std_dev_18_spl_list)
            spl_results.append(avg_spl_D_list)
            spl_results.append(std_dev_D_spl_list)
            known_sample_results=[]
            if protocol_type==1 or protocol_type==3:
                spl_results.append(avg_spl_17_list)
                spl_results.append(std_dev_17_spl_list)
            spl_results.append(avg_spl_d_excess_list)
            spl_results.append(std_dev_d_excess_list)
    return spl_results,known_sample_results
 