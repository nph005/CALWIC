# -*- coding: utf-8 -*-
"""
Created on Friday August 26 2022

@author: @author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""

import loading_files as lf 
import pandas as pd
import numpy as np 

def get_identifiers(option_protocol1, entry_1_1):
    """
    Load the file (download or copy-paste), then import it 
    and get some usefull columns for the prefill. 

    Parameters
    ----------
    option_protocol1 : tkinter.stringVar()
        Stores the value of where to look for the file 
    entry_1_1 : tkinter.Entry()
        Contains the filename (without extension)

    Returns
    -------
    result_file_df : pandas.DataFrame()
        DataFrame from the input file 
    inj_nbr_df : pandas.Series()
        column "Inj Nr" extracted from result_file_df
    id1_df : pandas.Series()
        column "Identifier 1" extracted from result_file_df
    id2_df : pandas.Series()
        column "Identifier 2" extracted from result_file_df
    port_df : pandas.Series()
        column "Port" extracted from result_file_df

    """
    filename=lf.downloading_file(option_protocol1, entry_1_1)
    result_file_df=pd.read_csv("./files/raw_files_temp/"+filename+".csv",sep=None,skipinitialspace=True,engine="python")
    inj_nbr_df=result_file_df["Inj Nr"]
    id2_df=result_file_df["Identifier 2"]
    id1_df=result_file_df["Identifier 1"]
    port_df=result_file_df["Port"]
    return result_file_df,inj_nbr_df,id1_df,id2_df,port_df

def counter(id1_df,id2_df,inj_nbr_df,port_df):
    """
    Calculate all the parameters which needs to be prefilled

    Parameters
    ----------
    id1_df : pandas.Series()
        column "Identifier 1" extracted from result_file_df
    id2_df : pandas.Series()
        column "Identifier 2" extracted from result_file_df
    inj_nbr_df : pandas.Series()
        column "Inj Nr" extracted from result_file_df
    port_df : pandas.Series()
        column "Port" extracted from result_file_df

    Returns
    -------
    inj_per_std : int
        Injections per standard
    std_nbr : int 
        Number of standards 
    inj_per_spl : int 
        Injections per sample 
    spl_nbr : int
        Samples number
    is_spy : bool
        Indicates if there are spy samples
    spy_nbr : int
        number of spy samples detected
    spy_port : list
        Port of the spy samples
    spy_name_found : list
        Name of the spy samples (if it matches with a name from the std_values.csv)
    std_name_found : list
        Name of the standards (if it matches with a name from the std_values.csv)

    """
    std_values_file,std_short_names_list=lf.load_standard_csv_file()
    std_where=np.where(id2_df.str.contains("STD"))
    inj_std_part=inj_nbr_df.iloc[std_where]
    std_name_part=id1_df.iloc[std_where]
    try :
        inj_per_std=inj_std_part.iloc[-1]
        std_nbr=0
        std_name_found=[]
        for i in range(len(inj_std_part),0,-1):
            h=0
            if inj_std_part.iloc[-1]==inj_std_part.iloc[i-1]:
                std_nbr=std_nbr+1
                for j in range(0,len(std_short_names_list)):
                    if std_name_part.iloc[i-1]==std_short_names_list[j]:
                        std_name_found.insert(0,std_short_names_list[j])
                        h=1
                if h==0:
                    std_name_found.insert(0,"not found")
        error=0
        try:
            spl_where=np.where(id2_df.str.contains("SAMPLE"))
            inj_spl_part=inj_nbr_df.iloc[spl_where]
            inj_per_spl=inj_spl_part.iloc[-1]
            spl_nbr=0
            for i in range(len(inj_spl_part),0,-1):
                if inj_spl_part.iloc[-1]==inj_spl_part.iloc[i-1]:
                    spl_nbr=spl_nbr+1
                    

                    
            error=0
            try:
                is_spy=True
                spy_where=np.where(id2_df.str.contains("SPY"))
                if len(spy_where)==0:
                    is_spy=False
                spy_nbr=0
                if is_spy==True:
                    inj_spy_part=inj_nbr_df.iloc[spy_where]
                    spy_name_part=id1_df.iloc[spy_where]
                    port_spy_part=port_df.iloc[spy_where]
                    spy_nbr=0
                    spy_name_found=[]
                    spy_port=[]
                    for i in range(len(inj_spy_part),0,-1):
                        h=0
                        if inj_spy_part.iloc[-1]==inj_spy_part.iloc[i-1]:
                            spy_port.insert(0,port_spy_part.iloc[i-1])
                            spy_nbr=spy_nbr+1
                            for j in range(0,len(std_short_names_list)):
                                if spy_name_part.iloc[i-1]==std_short_names_list[j]:
                                    spy_name_found.insert(0,std_short_names_list[j])
                                    h=1
                            if h==0:
                                spy_name_found.insert(0,"not found")
                spl_nbr=spl_nbr+spy_nbr
                error=0
            except IndexError:
                error=3
                inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found="","","","","","","","",""
                return error,inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found
        except IndexError:
            error=2
            inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found="","","","","","","","",""
            return error,inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found
    except IndexError:
        error=1
        inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found="","","","","","","","",""
        return error,inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found
    return error,inj_per_std,std_nbr,inj_per_spl,spl_nbr,is_spy,spy_nbr,spy_port,spy_name_found,std_name_found


