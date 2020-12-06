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

import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

import time
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as md

# plot inline
#%matplotlib inline
# plot in separate window
#%matplotlib qt
# for script and plotting
# CONTROLS FOR PLOT DISPLAY
from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('matplotlib', 'qt')

from pathlib import Path # for filename withput extension

#---------------------------------------------------
#-------------------configurations------------------
#---------------------------------------------------
#DEBUG = True
DEBUG = False

# data directory
# r"C:\Users\crtjur\Desktop\jupyter-notebooks.git\npTDMS"
# r"C:\Users\crtjur\Desktop\ford-otosan"
DATA_DIR = r"C:\Users\crtjur\Desktop\ford-otosan\GH-HIDRIA"#r"C:\Users\crtjur\Desktop\ford-otosan" # r"C:\Users\crtjur\Desktop\ford-otosan"
#C:\Users\crtjur\Desktop\ford-otosan\GH-HIDRIA
FILENAME = "test_4_DUT_18"
FILEPATH = os.path.join(DATA_DIR, FILENAME + ".tdms")

def import_data(file):
    """Read tdms file"""
    df = None

    channel_list = []
    group_list = []

    with TdmsFile.open(file) as f:

        print("opening", file)

        for group in f.groups():
            group_name = group.name
            group_list.append(group_name)

            for channel in group.channels():
                channel_name = channel.name
                channel_list.append(channel_name)
                #channel_name = channel.name
                #Access dictionary of properties:
                #properties = channel.properties
                #Access numpy array of data for channel:
                #data = channel[:]

        # select group
        selected_group = group_list[0]

        time = channel.time_track()
        # convert tim = numpy array to pandas df
        time_df = pd.DataFrame(time, columns = ['Time'])
        print(time_df[:10])

        #data_df = f["analog"].as_dataframe()
        data_df = f[selected_group].as_dataframe()
        print(data_df[:10])

        # merge two pandas df
        merged_df = pd.concat([time_df, data_df], axis=1).reindex(time_df.index)
        print(merged_df.head())
        print(merged_df.tail())
        print(merged_df.shape)

    #time = channel.time_track()
    #print(time)

    #print(f.groups())
    #print(f.channels())
    #channel = tdms_file[group_name][channel_name]
    #channel_data = channel[:]

#    tdms_file = TdmsFile.read(file)
#
#    group_list = []
#    channel_list = []

    return merged_df

# Get list of files in folder
def list_files(folder):
    file_list = []

    for file in os.listdir(folder):
        # only use .txt files
        if file.endswith(".tdms"):
            file_list.append(os.path.join(folder,file))

    if(DEBUG):
        print(file_list)

    return file_list

def export_df_to_excel(file, dataframe):
    xlsx_filename = Path(file).stem + ".xlsx"
    xlsx_filepath = os.path.join(DATA_DIR, xlsx_filename)
    print(xlsx_filepath)
    merged_df.to_excel(xlsx_filepath, index = False)

##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------
def plot_dataframe(dataframe, filepath):
    # create plot name
    plot_filename = Path(filepath).stem + ".png"
    plot_filepath = os.path.join(DATA_DIR, plot_filename)
    #print(plot_filepath)

    # get column names from dataframe
    time_column_name = list(dataframe.columns)[0]
    data_column_names = list(dataframe.columns)[1:]
    #print(time_column_name)
    #print(data_column_names)


    fig = plt.figure()
    plt.title(plot_filename)
    ax = plt.subplot(111)

    # create x axis
    #ax = plt.gca()

    # create secondary axis
    # twin object for two different y-axis on the sample plot
    #ax2=ax.twinx()

    # populate y axis data
    for column in data_column_names:
        #print(channel.name)
        dataframe.plot(kind='line', x=time_column_name, y=column, ax=ax)

    # set plot axis limits
    ax.set_xlim([0,1000])
    ax.set_ylim([0,1100])

    #-----GRID-------------
    # AUTOMATIC
    #ax.grid(True)
    #CUSTOM
    # Major ticks every 20, minor ticks every 5
    major_ticks_x = np.arange(0, 1026, 205)
    minor_ticks_x = np.arange(0, 1026, 20)

    ax.set_xticks(major_ticks_x)
    ax.set_xticks(minor_ticks_x, minor=True)

    major_ticks_y = np.arange(0, 1101, 100)
    minor_ticks_y = np.arange(0, 1101, 20)

    ax.set_yticks(major_ticks_y)
    ax.set_yticks(minor_ticks_y, minor=True)

    # And a corresponding grid
    ax.grid(which='both')

    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    # Turn grid on for both major and minor ticks and style minor slightly
    # differently.
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
    plt.savefig(plot_filepath, bbox_inches='tight')

    #-----------SHOW-------------------
    plt.show()

##--------------------------FUNCTIONS------------------------------

#def plot_variant_2():
#    # set title
#    #plt.title(FILENAME)
#
#    fig = plt.figure()
#    ax = plt.subplot(111)
#
#    for name in channel_list:
#        ax.plot(x_axis_seconds, df[name], label=name)
#        #print(df[name].head())
#
#    # set axis labels
#    #plt.xlabel("time[s]")
#    #plt.ylabel("Amplitude")
#
#    # Place a legend to the right of this smaller subplot.
#    #plt.legend(bbox_to_anchor=(1.01, 0.8), loc=0, borderaxespad=0.)
#
#    # save current plot to file
#    #plt.savefig(FILENAME + '-output.png', dpi=300, bbox_inches='tight')
#
#    # Shrink current axis by 20%
#    box = ax.get_position()
#    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
#
#    # Put a legend to the right of the current axis
#    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#
#    plt.show()

def main():
    """main function"""

    # get path of all .tdms files in DATA_DIR
    file_list = list_files(DATA_DIR)

    for file in file_list: #file_list[0:1]
        print(file)

        df = import_data(file)

        # get only data until
        #export_df_to_excel(file, df)

        # plot dataframe
        plot_dataframe(df, file)

def test():
        file = r"C:\Users\crtjur\Desktop\jupyter-notebooks.git\npTDMS\test_4_DUT_18.tdms"
        print(file)
        df = import_data(file)
        # get only data until
        #export_df_to_excel(file, df)
        # plot dataframe
        plot_dataframe(df, file)

if __name__ == "__main__":
    main()
    #test()