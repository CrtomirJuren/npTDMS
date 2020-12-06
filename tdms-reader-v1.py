# -*- coding: utf-8 -*-
"""
Script to Convert .tdms to .xlsx

Created on Wed Nov 25 16:09:49 2020
@author: crtjur
"""
#---------------------------------------------------
#----------------------imports----------------------
#---------------------------------------------------
import os
from pathlib import Path # for filename withput extension

import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

import time
from time import sleep
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as md

# tqdm progress bar
from tqdm import tqdm
from tqdm import trange
from colorama import Fore

import math # for rounding up/down ceil/floor function

# CONTROLS FOR PLOT DISPLAY
# select plot inline or in seperate window
#%matplotlib inline # plot in spyder
#%matplotlib qt # plot in separate window
from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt')

#---------------------------------------------------
#-------------------configurations------------------
#---------------------------------------------------
#DEBUG = True
DEBUG = False

# data directory
#r"test_4_DUT_18"
#r"DAQ-sim"
DATA_DIR = r"C:\Users\crtom\Documents\npTDMS.git\data"
FILENAME = r"DAQ-sim"
FILEPATH = os.path.join(DATA_DIR, FILENAME + ".tdms")

channel_list = []
group_list = []
    
def import_data(file_path):
    """Read tdms file"""
    global channel_list
    global group_list
    
  
    print("opening", file_path)
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    
    with TdmsFile.open(file_path) as tdms_file:
        
         # Iterate over all items in the file properties and print them
        for name, value in tdms_file.properties.items():
            print("{0}: {1}".format(name, value))
        
        # DAQ data has only one group
        for group in tdms_file.groups():
            group_name = group.name
            group_list.append(group_name)
        
        print(tdms_file.groups())

        for channel in group.channels():
            channel_name = channel.name
            channel_list.append(channel_name)
            #channel_name = channel.name
            #Access dictionary of properties:
            # PROPERTIES IS A DICTIONARY
            properties = channel.properties
            #print(properties)
            #Access numpy array of data for channel:
            #data = channel[:]
        
        for x,y in properties.items():
            print(x," = ",y)

        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
            
        # calculate number of chunks in file
        # get number of all data chunk -> used for tqdm progress           
        pbar_length = 0
        for chunk in tdms_file.data_chunks():
                pbar_length += 1
        
        # read data by chunks
        pbar = tqdm(total = pbar_length, leave=True, desc='Loading')
        
        print(FILENAME, "started loading")
        
        is_fc_chunk = True
        for chunk in tdms_file.data_chunks():
            
            pbar.update()
            #print("new chunk")
            
            v_stacked_buffer = []
            is_fc_channel = True
            for channel in group.channels():
                   
                channel_name = channel.name
                signal_chunk = chunk[group_name][channel_name]
                
                if is_fc_channel:
                    is_fc_channel = False
                    v_stacked_buffer = signal_chunk[:]
                else:
                    v_stacked_buffer = np.vstack((v_stacked_buffer, signal_chunk))
                
            if is_fc_chunk:
                #first call 
                is_fc_chunk = False
                #i += 1
                h_stacked_buffer = v_stacked_buffer[:]
            else:
                h_stacked_buffer = np.hstack((h_stacked_buffer, v_stacked_buffer[:]))
        
        pbar.close() 

        print(FILENAME, "finished loading")         
           
        signal_data = np.transpose(h_stacked_buffer)
        
        # convert your array into a dataframe
        signal_data_df = pd.DataFrame(signal_data,columns=channel_list)
        
        # get time data
        date_time_dt64 = channel.time_track(absolute_time = True)#, accuracy='ns'
        test_time_dt64 = channel.time_track(absolute_time = False)
        
        # convert tim = numpy array to pandas df
        date_time_df = pd.DataFrame(date_time_dt64, columns = ['date_time'])
        test_time_df = pd.DataFrame(test_time_dt64, columns = ['test_time'])
        
        # merge date_time, test_time and data
        tdms_df = pd.concat([date_time_df, test_time_df, signal_data_df], axis=1).reindex(date_time_df.index)
        
    return tdms_df
        
# Get list of files in folder
def list_files(folder):
    file_list = []
    for file in os.listdir(folder):
        # only use .txt files
        if file.endswith(".tdms"):
            file_list.append(os.path.join(folder,file))
    return file_list

def export_df_to_excel(file, dataframe):
    xlsx_filename = Path(file).stem + ".xlsx"
    xlsx_filepath = os.path.join(DATA_DIR, xlsx_filename)
    print(xlsx_filepath)
    merged_df.to_excel(xlsx_filepath, index = False)

##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------

def plot_dataframe_auto(df):
    global channel_list
    
    fig = plt.figure()
    ax = plt.subplot(111)
    ax1 = fig.add_subplot(111)
    
    # populate y axis data
    for channel in channel_list:
        #print(channel.name)
        df.plot(kind='line', x="test_time", y=channel, ax=ax1)
        print(channel)

    plt.show()
    
def plot_dataframe_manual(df, file_path):
    global channel_list
    
    # create file, path variables
    plot_name = Path(file_path).stem
    plot_filepath = os.path.join(DATA_DIR, plot_name+".png")
    
    # create plot    
    fig = plt.figure(figsize=(19.20,10.80))
    ax = plt.subplot(111)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()
    
    # create plot name
    plt.title(plot_name)
        
    # populate y axis data
    for channel in channel_list:
        #print(channel.name)
        df.plot(kind='line', x="test_time", y=channel, ax=ax1)
        print(channel)
    
    #---------------GET MAX, MIN Y AXIS AMPLITUDES----------------------------
    amp_max = []
    amp_min= []
    for channel in channel_list:
        amp_max.append(df[channel].max())  
        amp_min.append(df[channel].min())  
    #print(amp_max)        
    #print(amp_min)        
    amp_max = max(amp_max)
    amp_min = min(amp_min)
    #round to nearest integer
    amp_max = math.ceil(amp_max)
    amp_min = math.floor(amp_min)

   
    #---------------GET MAX, MIN Y AXIS AMPLITUDES----------------------------
    # Assuming df has a unique index, this gives the row with the maximum value:
    
    # SET PLOT LIMITS
    #Get maximum = last value of absolute test time
    date_time_max = df["date_time"].tail(1)
    print("test_date_time_max: ",date_time_max)
    
    #Get maximum = last value of absolute test time
    test_time_max = df["test_time"].tail(1)
    test_time_max = math.ceil(test_time_max)
    print(test_time_max)
    
    # # set plot axis limits
    ax.set_xlim([0,test_time_max])
    ax.set_ylim([amp_min,amp_max])
    
    #ax2.set_xlim(ax1.get_xlim())
    #ax2.set_xticks(new_tick_locations)
    #ax2.set_xticklabels(tick_function(new_tick_locations))
    ax2.set_xlabel(r"date_time")
    #ax2.set_xlabel(r"Modified x-axis: $1/(1+X)$")
    
    #---------------------------GRID----------------------
    # AUTOMATIC
    ax.grid(True)
    #CUSTOM
    # Major ticks every 20, minor ticks every 5
    major_ticks_x = np.arange(0, test_time_max, test_time_max/10)
    minor_ticks_x = np.arange(0, test_time_max, test_time_max/20)
    
    # #
    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)
    # #
    major_ticks_y = np.arange(amp_min, amp_max, amp_max/10)
    minor_ticks_y = np.arange(amp_min, amp_max, amp_max/20)
    # #
    ax.set_yticks(major_ticks_y)
    ax.set_yticks(minor_ticks_y, minor=True)
    # #
    # # And a corresponding grid
    ax.grid(which='both')
    # #
    # # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.4)
    ax.grid(which='major', alpha=0.7)
    # # Turn grid on for both major and minor ticks and style minor slightly
    # # differently.
    #ax.grid(which='major', color='#CCCCCC', linestyle='--')
    #ax.grid(which='minor', color='#CCCCCC', linestyle=':')
    
    #-----------LEGEND-------------------
    #Place a legend to the right of this smaller subplot.
    plt.legend(bbox_to_anchor=(1.01, 0.8), loc=0, borderaxespad=0.)
    # Shrink current axis by 20%
    box = ax.get_position()
    
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.6))
    #-----------SAVE-------------------
    # save plot to file
    plt.savefig(plot_filepath, bbox_inches='tight', dpi=500)
    
    #--------------SHOW--------------
    plt.show()
    
def main():

    #file_path = r"D:\npTDMS\data\DAQ-sim.tdms"
    #file_path = r"D:\npTDMS\data\test_4_DUT_18.tdms"
    dataframe = import_data(FILEPATH)
    
    plot_dataframe_manual(dataframe, FILEPATH)
    
if __name__ == "__main__":
    main()

