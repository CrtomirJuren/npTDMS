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
import math # for rounding up/down ceil/floor function

import time
from time import sleep
import datetime as dt

# tqdm progress bar
from tqdm import tqdm
from tqdm import trange
from colorama import Fore

import matplotlib.pyplot as plt
import matplotlib.dates as md
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

class TdmsFileReader:
    def __init__(self, file_path, *args, **kwargs):
        
        self.file_path = file_path
        self.file_name = Path(self.file_path).stem #get filename withput extension
        self.file_dir = os.path.dirname(self.file_path) ## directory of file
        
        self.channel_names = []
        self.group_names = []
        self.selected_group = None
        self.selected_channel = None
        
        self.chunks_number = None
        
        # main tdms dataframe with all the data
        self.dataframe = None
        
        # figure reference for saving plot
        self.figure = None

        
    def read_tdms_to_df(self):

        with TdmsFile.open(self.file_path) as tdms_file:
            
            # get groups
            for group in tdms_file.groups():
                self.group_names.append(group.name)
            
            # set current group
            self.selected_group = self.group_names[0]
            
            # get channels
            for channel in group.channels():
                self.channel_names.append(channel.name)

            # calculate number of chunks in file
            pbar_length = 0
            for idx, chunk in enumerate(tdms_file.data_chunks()):
                    chunks_number = idx
            
            # create progress bar
            pbar = tqdm(total = chunks_number, leave=True, desc=self.file_name)
            
            
            # start loading chunks of signal data to numpy buffer
            is_fc_chunk = True
            for chunk in tdms_file.data_chunks():
                
                pbar.update()
                
                v_stacked_buffer = []
                is_fc_channel = True
                for channel in group.channels():
                       
                    channel_name = channel.name
                    signal_chunk = chunk[self.selected_group][channel_name]
                    
                    if is_fc_channel:
                        is_fc_channel = False
                        v_stacked_buffer = signal_chunk[:]
                    else:
                        v_stacked_buffer = np.vstack((v_stacked_buffer, signal_chunk))
                    
                if is_fc_chunk:
                    is_fc_chunk = False
                    h_stacked_buffer = v_stacked_buffer[:]
                else:
                    h_stacked_buffer = np.hstack((h_stacked_buffer, v_stacked_buffer[:]))
               
            # close progress bar
            pbar.close() 
            
            # signal by rows to signal by columns
            signal_data = np.transpose(h_stacked_buffer)
            
            # numpy array to dataframe
            signal_data_df = pd.DataFrame(signal_data, columns = self.channel_names)
            
            # get time arrays
            date_time_dt64 = channel.time_track(absolute_time = True)#, accuracy='ns'
            test_time_dt64 = channel.time_track(absolute_time = False)
            
            # convert time = numpy array to pandas df
            date_time_df = pd.DataFrame(date_time_dt64, columns = ['date_time'])
            test_time_df = pd.DataFrame(test_time_dt64, columns = ['test_time'])
            
            # merge date_time, test_time and data
            self.dataframe = pd.concat([date_time_df, test_time_df, signal_data_df], axis=1).reindex(date_time_df.index)
    
    
    def get_df(self):
        return self.dataframe


    def df_export_to_excel(self):
        xlsx_filepath = os.path.join(self.file_dir, self.file_name + ".xlsx")
        self.dataframe.to_excel(xlsx_filepath, index = False)


    def plot_export_to_png(self):
        #-----------SAVE-------------------
        plot_filepath = os.path.join(self.file_dir, self.file_name + ".png")
        # save plot to file
        self.figure.savefig(plot_filepath, bbox_inches='tight', dpi=500)
    
    
    def plot_automatic(self):
        self.figure = plt.figure()
        ax = plt.subplot(111)
        
        # populate y axis data
        for channel in self.channel_names:
            self.dataframe.plot(kind='line', x="test_time", y = channel, ax=ax)
 
        # automatic grid
        ax.grid(True, alpha=0.7)
        
        plt.show()
    
    
    def plot_manual(self):

        # create plot    
        self.figure = plt.figure(figsize=(19.20,10.80))
        ax = plt.subplot(111)
        ax1 = self.figure.add_subplot(111)
        ax2 = ax1.twiny()
        
        # create plot name
        plt.title(self.file_name)
            
        # populate y axis data
        for channel in self.channel_names:
            self.dataframe.plot(kind='line', x="test_time", y=channel, ax=ax1)
        
        #---------------GET MAX, MIN Y AXIS AMPLITUDES----------------------------
        amp_max = []
        amp_min= []

        for channel in self.channel_names:
            amp_max.append(self.dataframe[channel].max())  
            amp_min.append(self.dataframe[channel].min())  
       
        #round to nearest integer
        amp_max = math.ceil(max(amp_max))
        amp_min = math.floor(min(amp_min))

        #---------------GET MAX, MIN Y AXIS AMPLITUDES----------------------------
        # Assuming df has a unique index, this gives the row with the maximum value:
        
        # SET PLOT LIMITS
        #Get maximum = last value of absolute test time
        date_time_max = self.dataframe["date_time"].tail(1)
        test_time_max = self.dataframe["test_time"].tail(1)

        test_time_max = math.ceil(test_time_max)
        
        # # set plot axis limits
        ax.set_xlim([0,test_time_max])
        ax.set_ylim([amp_min,amp_max])
        
        #ax2.set_xlim(ax1.get_xlim())
        #ax2.set_xticks(new_tick_locations)
        #ax2.set_xticklabels(tick_function(new_tick_locations))
        ax1.set_xlabel(r"test_time")
        ax2.set_xlabel(r"date_time")
                
        #---------------------------GRID----------------------
        # Major ticks every 20, minor ticks every 5
        major_ticks_x = np.arange(0, test_time_max, test_time_max/10)
        minor_ticks_x = np.arange(0, test_time_max, test_time_max/20)
        
        ax.set_xticks(major_ticks_x)
        ax.set_xticks(minor_ticks_x, minor=True)
        
        major_ticks_y = np.arange(amp_min, amp_max, amp_max/10)
        minor_ticks_y = np.arange(amp_min, amp_max, amp_max/20)
        
        ax.set_yticks(major_ticks_y)
        ax.set_yticks(minor_ticks_y, minor=True)
        
        #And a corresponding grid
        ax.grid(which='both')
        
        # Or if you want different settings for the grids:
        ax.grid(which='minor', alpha=0.4)
        ax.grid(which='major', alpha=0.7)

        #-----------LEGEND-------------------
        #Place a legend to the right of this smaller subplot.
        plt.legend(bbox_to_anchor=(1.01, 0.8), loc=0, borderaxespad=0.)
        # Shrink current axis by 20%
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
        # Put a legend to the right of the current axis
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.6))
        
        #--------------SHOW--------------
        plt.show()

# Get list of files in folder
def list_files(folder):
    file_list = []
    for file in os.listdir(folder):
        # only use .txt files
        if file.endswith(".tdms"):
            file_list.append(os.path.join(folder,file))
    return file_list
    
def main():

    file_path = r"C:\Users\crtom\Documents\npTDMS.git\data\DAQ-sim.tdms"
    
    # create object
    my_tdms_obj = TdmsFileReader(file_path)
    
    # load data to dataframe
    my_tdms_obj.read_tdms_to_df()
    
    # get dataframe
    df = my_tdms_obj.get_df()
    print(df.head(1))
    
    my_tdms_obj.plot_manual() #my_tdms_obj.plot_automatic()
    my_tdms_obj.plot_export_to_png()
    my_tdms_obj.df_export_to_excel()
    
if __name__ == "__main__":
    main()


