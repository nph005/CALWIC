# -*- coding: utf-8 -*-
"""
Created on Friday July 15 2022

@author: Baptiste Bordet : https://orcid.org/0000-0002-9994-7813

This file is part of ALWIC-tool.

ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with ALWIC-tool. If not, see http://www.gnu.org/licenses
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


# Function to plot raw standards values (to check if there is a standard to remove)

def memory_correction_parameters_plot(protocol_type,iso_type_list,std_nbr,inj_per_std,result_file_df,processing_check_page,option_name_6_dict):
    rows=std_nbr-1
    columns=len(iso_type_list)
    fig,ax=plt.subplots(nrows=rows,ncols=columns)
    fig.subplots_adjust(left=0.1,
                    bottom=0.075, 
                    right=0.95, 
                    top=0.95, 
                    wspace=0.4, 
                    hspace=0.7)
    for j in range(1,ax.shape[0]+1):
        for i,iso_type in enumerate(iso_type_list):
            ax[j-1][i].set_title(option_name_6_dict[list(option_name_6_dict.keys())[j]].get()+" (STD " +str(j+1)+ ")",loc="right")
            ax[j-1][i].plot(result_file_df["Inj Nr"].iloc[inj_per_std*(j):inj_per_std+inj_per_std*(j)],result_file_df["raw_value_"+iso_type].iloc[inj_per_std*(j):inj_per_std+inj_per_std*(j)],linewidth=0,marker="o",label="Raws Data")
            ax[j-1][i].set_xlabel("Injection number")
            ax[j-1][i].legend()
            if iso_type=="d18O":
                ax[j-1][i].set_ylabel("$\delta ^{18}O $"+" "+"$(\u2030)$")
            elif iso_type=="dD":
                ax[j-1][i].set_ylabel("$\delta D $"+" "+"$(\u2030)$")
            elif iso_type=="d17O":
                ax[j-1][i].set_ylabel("$\delta ^{17}O $"+" "+"$(\u2030)$")
    canvas_intermediate=FigureCanvasTkAgg(fig,master=processing_check_page)
    canvas_intermediate.draw()
    canvas_intermediate.get_tk_widget().place(relx=0.03,rely=0.15,relheight=0.75,relwidth=0.5)

            

# Function to create memory correction plot

def memory_correction_plot(isotope_type,which_std,corrected_file_df,std_nbr,inj_per_std,option_name_6_dict,axes):
    axes.set_title(option_name_6_dict[list(option_name_6_dict.keys())[which_std]].get()+" (STD " +str(which_std+1)+ ")",loc="right")
    axes.plot(corrected_file_df["Inj Nr"].iloc[inj_per_std*which_std:inj_per_std+inj_per_std*which_std],corrected_file_df["MC_corr"+isotope_type].iloc[inj_per_std*which_std:inj_per_std+inj_per_std*which_std],c="r",linewidth=0,marker="+",markersize=10,label="Corrected values")
    axes.plot(corrected_file_df["Inj Nr"].iloc[inj_per_std*which_std:inj_per_std+inj_per_std*which_std],corrected_file_df["raw_value_"+isotope_type].iloc[inj_per_std*which_std:inj_per_std+inj_per_std*which_std],linewidth=0,marker="o",label="Raws Data")
    axes.set_xlabel("Injection number")
    axes.legend()
    if isotope_type=="d18O":
        axes.set_ylabel("$\delta ^{18}O $"+" "+"$(\u2030)$")
    elif isotope_type=="dD":
        axes.set_ylabel("$\delta D $"+" "+"$(\u2030)$")
    elif isotope_type=="d17O":
        axes.set_ylabel("$\delta ^{17}O $"+" "+"$(\u2030)$")
    return axes

# Function to create calibration curve plot

def calibration_curve_plot(isotope_type,measured_vector,true_vector,slope,intercept,axes):
    min_x=np.min(measured_vector)
    max_x=np.max(measured_vector)
    min_y=np.min(true_vector)
    max_y=np.max(true_vector)
    lim_min=np.min((min_x,min_y))-.15*np.abs(np.min((min_x,min_y)))
    lim_max=np.max((max_x,max_y))+.15*np.abs(np.max((max_x,max_y)))
    X_fit=np.arange(min_x,max_x+.5)
    Y_fit=X_fit*slope+intercept
    isotope_name=""
    if isotope_type=="d18O":
        isotope_name="$\delta ^{18}O$"
    if isotope_type=="dD":
        isotope_name="$\delta D$"
    if isotope_type=="d17O":
       isotope_name="$\delta ^{17}O$"
    axes.set_title("Calibration Curve "+isotope_name,loc="right")
    axes.plot(X_fit,Y_fit,c="b")
    axes.plot(measured_vector,true_vector,linewidth=0,marker="o",markersize=6,c="b")
    axes.set_xlim(lim_min,lim_max)
    axes.set_ylim(lim_min,lim_max)
    if isotope_type=="d18O":
        axes.set_xlabel("$\delta ^{18}O$ measured "+"$(\u2030)$")
        axes.set_ylabel("$\delta ^{18}O$ defined "+"$(\u2030)$")
    if isotope_type=="dD":
        axes.set_xlabel("$\delta D$ measured "+"$(\u2030)$")
        axes.set_ylabel("$\delta D$ defined "+"$(\u2030)$")
    if isotope_type=="d17O":
        axes.set_xlabel("$\delta ^{17}O$ measured "+"$(\u2030)$")
        axes.set_ylabel("$\delta ^{17}O$ defined "+"$(\u2030)$")
    return axes



# Function to create all plots 

def creation_all_plots(list_plots,corrected_file_df,iso_type_list,std_nbr,inj_per_std,option_name_6_dict,calibration_vectors,calibration_param_list,filename,eval_groning):
    rows=std_nbr
    columns=len(iso_type_list)
    fig,ax=plt.subplots(nrows=rows,ncols=columns)
    fig.subplots_adjust(left=0.1,
                    bottom=0.075, 
                    right=0.95, 
                    top=0.95, 
                    wspace=0.4, 
                    hspace=0.7)
    for j in range(0,ax.shape[0]-1):
        for i,iso_type in enumerate(iso_type_list):
            ax[j][i]=memory_correction_plot(iso_type, j+1, corrected_file_df, std_nbr, inj_per_std, option_name_6_dict,ax[j][i])
    for i,iso_type in enumerate(iso_type_list):
         ax[-1][i]=calibration_curve_plot(iso_type,calibration_vectors[0][i],calibration_vectors[1][i],calibration_param_list[0][i],calibration_param_list[1][i],ax[-1][i])
    
    return fig,ax

# Function that defines the possible plots to make (page1) 

def create_list_plots(std_nbr,protocol_type,iso_type_list):
    list_plots=["All plots"]
    for i in range(1,std_nbr):
        for iso_type in iso_type_list:
            list_plots.append("Memory Correction "+iso_type+" std "+str(i+1))
    for iso_type in iso_type_list:
        list_plots.append("Calibration Curve "+iso_type)
    return list_plots

 # Function that create canvas when all plots is activated (page 1)

def all_plots_canvas_creator(figure,page_results_1):
    canvas=FigureCanvasTkAgg(figure,master=page_results_1)
    canvas.draw()
    canvas.get_tk_widget().place(relx=0.03,rely=0.15,relheight=0.75,relwidth=0.5)
    return canvas

# Function that create canvas when one other plot is activated (page1)

def other_plots_canvas_creator(figure1,figure2,page_results_1):
    canvas1=FigureCanvasTkAgg(figure1,master=page_results_1)
    canvas1.draw()
    canvas1.get_tk_widget().place(relx=0.03,rely=0.15,relheight=0.75,relwidth=0.5)
    canvas2=FigureCanvasTkAgg(figure2,master=page_results_1)
    canvas2.draw()
    canvas2.get_tk_widget().place(relx=0.57,rely=0.15,relheight=0.75,relwidth=0.41)
    return canvas1, canvas2

# Function to make raws plots (page results 2)

def make_raws_plots(protocol_type,final_value_file_df):
    if protocol_type==0 or protocol_type==2:
        fig,ax=plt.subplots(nrows=6,ncols=1)
        for axs in ax:
            axs.grid(axis="x",which="major",color="k")
            axs.set_xticks(np.arange(0,max(final_value_file_df.index+1),25))
            axs.set_xlim(left=0,right=max(final_value_file_df.index+3))
        fig.subplots_adjust(left=0.1,
                        bottom=0.075, 
                        right=0.95, 
                        top=0.95, 
                        wspace=0.4, 
                        hspace=0.7)
        ax[0].scatter(final_value_file_df.index+1,final_value_file_df["H2O_Mean"])
        ax[1].scatter(final_value_file_df.index+1,final_value_file_df["raw_value_d18O"])
        ax[2].scatter(final_value_file_df.index+1,final_value_file_df["MC_corrd18O"],c="orange")
        ax[3].scatter(final_value_file_df.index+1,final_value_file_df["raw_value_dD"])
        ax[4].scatter(final_value_file_df.index+1,final_value_file_df["MC_corrdD"],c="orange")
        ax[5].scatter(final_value_file_df.index+1,final_value_file_df["final_value_d-excess"],c="green")
        ax[5].set_xlabel("Injection Number on the run", fontsize=10)
        ax[0].set_title("Humidity", fontsize=15)
        ax[1].set_title("\u03B4\u00B9\u2078O raw", fontsize=15)
        ax[2].set_title("\u03B4\u00B9\u2078O Memory Corrected", fontsize=15)
        ax[3].set_title("\u03B4D  raw", fontsize=15)
        ax[4].set_title("\u03B4D Memory Corrected", fontsize=15)
        ax[5].set_title("d-excess", fontsize=15)
        ax[0].set_ylabel("Humidity level (ppmv)",fontsize=10)
        ax[1].set_ylabel("\u03B4\u00B9\u2078O (\u2030)",fontsize=10)
        ax[2].set_ylabel("\u03B4\u00B9\u2078O (\u2030)",fontsize=10)
        ax[3].set_ylabel("\u03B4D (\u2030)",fontsize=10)
        ax[4].set_ylabel("\u03B4D (\u2030)",fontsize=10)
        ax[5].set_ylabel("d-excess (\u2030)",fontsize=10)
    if protocol_type==1 or protocol_type==3:
        fig,ax=plt.subplots(nrows=9,ncols=1)
        for axs in ax:
            axs.grid(axis="x",which="major",color="k")
            axs.set_xticks(np.arange(0,max(final_value_file_df.index+1),25))
            axs.set_xlim(left=0,right=max(final_value_file_df.index+3))
        fig.subplots_adjust(left=0.1,
                        bottom=0.075, 
                        right=0.95, 
                        top=0.95, 
                        wspace=0.4, 
                        hspace=0.7)
        ax[0].scatter(final_value_file_df.index+1,final_value_file_df["H2O_Mean"])
        ax[1].scatter(final_value_file_df.index+1,final_value_file_df["raw_value_d18O"])
        ax[2].scatter(final_value_file_df.index+1,final_value_file_df["MC_corrd18O"],c="orange")
        ax[3].scatter(final_value_file_df.index+1,final_value_file_df["raw_value_dD"]) 
        ax[4].scatter(final_value_file_df.index+1,final_value_file_df["MC_corrdD"],c="orange")
        ax[5].scatter(final_value_file_df.index+1,final_value_file_df["raw_value_d17O"])
        ax[6].scatter(final_value_file_df.index+1,final_value_file_df["MC_corrd17O"],c="orange")
        ax[7].scatter(final_value_file_df.index+1,final_value_file_df["final_value_d-excess"],c="green")
        ax[8].scatter(final_value_file_df.index+1,final_value_file_df["final_value_17O_excess"],c="green")
        ax[8].set_xlabel("Injection Number on the run", fontsize=10)
        ax[0].set_title("Humidity", fontsize=15)
        ax[1].set_title("\u03B4\u00B9\u2078O raw", fontsize=15)
        ax[2].set_title("\u03B4\u00B9\u2078O Memory corrected", fontsize=15)
        ax[3].set_title("\u03B4D raw", fontsize=15)
        ax[4].set_title("\u03B4D Memory corrected", fontsize=15)
        ax[5].set_title("d17O raw",fontsize=15)
        ax[6].set_title("d17O Memory corrected",fontsize=15)
        ax[7].set_title("d-excess", fontsize=15)
        ax[8].set_title("17O-excess", fontsize=15)
        ax[0].set_ylabel("Humidity level (ppmv)",fontsize=10)
        ax[1].set_ylabel("\u03B4\u00B9\u2078O (\u2030)",fontsize=10)
        ax[2].set_ylabel("\u03B4\u00B9\u2078O (\u2030)",fontsize=10)
        ax[3].set_ylabel("\u03B4D (\u2030)",fontsize=10)
        ax[4].set_ylabel("\u03B4D (\u2030)",fontsize=10)
        ax[5].set_ylabel("d17O (\u2030)", fontsize=10)
        ax[6].set_ylabel("d17O (\u2030)", fontsize=10)
        ax[7].set_ylabel("d-excess (\u2030)",fontsize=10)
        ax[8].set_ylabel("17O-excess (\u2030)",fontsize=10)
    return fig,ax

def create_two_figures(list_plots,option_plots,corrected_file_df, iso_type_list, std_nbr, inj_per_std, option_name_6_dict, calibration_vectors, calibration_param_list):
    figure1,ax1=creation_all_plots(list_plots, corrected_file_df, iso_type_list, std_nbr, inj_per_std, option_name_6_dict, calibration_vectors, calibration_param_list)
    figure2,ax2 = plt.subplots()
    rows=std_nbr
    idx_plots=int(list_plots.index(option_plots.get()))
    row_plot=int(np.ceil(idx_plots/len(iso_type_list)))
    column_plot=int(idx_plots%len(iso_type_list))-1
    row_plot=row_plot-1
    if row_plot==rows-1:
        i=column_plot
        ax2=calibration_curve_plot(iso_type_list[i], calibration_vectors[0][i],calibration_vectors[1][i],calibration_param_list[0][i],calibration_param_list[1][i],ax2)
        ax2.grid(True, which="major")
    else:
        ax2=memory_correction_plot(iso_type_list[column_plot], row_plot+1, corrected_file_df, std_nbr, inj_per_std, option_name_6_dict, ax2)
        ax2.grid(True, which="major")
    return figure1, figure2