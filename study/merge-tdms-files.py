# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:09:49 2020

@author: crtjur
"""
import os
# imports
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

import time
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as md

from pathlib import Path # for filename withput extension

##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------
#DEBUG = True
DEBUG = False

# data directory
DATA_DIR = r"C:\Users\crtjur\Desktop\ford-otosan"
#DATA_DIR = os.path.join(NOTEBOOK_DIR, "data")

## configurations
#FILEPATH = "DAQ-sim.tdms"
##FILENAME = "test_4_DUT_18"
##FILEPATH = FILENAME + ".tdms"
#
##FILEPATH = r"C:\Users\crtjur\Desktop\2020_11_26_10_55_ PSG-Immersion-postaja-4.tdms"
#
## read in memory whole tdms file
#tdms_file = TdmsFile.read(FILEPATH)
#
##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------
## read data from tdms and put it in dataframe
#metadata = TdmsFile.read_metadata(FILEPATH)
#print(metadata.properties)
#
#
## read properties - all groups, all channels
#group_list = []
#channel_list = []
#
#for group in tdms_file.groups():
#    group_name = group.name
#    group_list.append(group.name)
#    #print(group_name)
#    for channel in group.channels():
#        channel_list.append(channel.name)
#        channel_name = channel.name
#        #print(channel_name)
#        # Access dictionary of properties:
#        properties = channel.properties
#        # Access numpy array of data for channel:
#        data = channel[:]
#        # Access a subset of data
#        data_subset = channel[0:5]
#        #print(data_subset)
#
#print(group_list)
#print(channel_list)
#
##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------
#group_name = group_list[0]
#
## read data and construct pandas dataframe
## df = tdms_file["group-name-string"].as_dataframe()
#df = tdms_file[group_name].as_dataframe()
#
#print(df.head())
#print(df.tail())
#print(df.keys())
#print(df.shape)
#
#number_samples = df.shape[0]
#number_columns = df.shape[1]
#print(number_samples)
#print(number_columns)
#
##get df header = channel names
#column_names = df.columns.tolist()
#print(column_names)
#
## get more properties from selected channel
#channel_name = channel_list[0]
#channel = tdms_file[group_name][channel_name]
#
#wf_start_time_dt64 = channel.properties['wf_start_time']
#print(wf_start_time_dt64)
#
#dt = channel.properties['wf_increment']
#print(dt)
## now we can calculate total test time in seconds
#duration_sec = number_samples * dt
#print(duration_sec)
#
## ENABLE THIS PART FOR EXCEL CONVERSION
## SAVE TO DATEAFRAME TO EXCEL
##df.to_excel("converted-tdms.xlsx")
#
##---------------------------------------------------
##---------------------------------------------------
##---------------------------------------------------
#x_axis_seconds = np.linspace(1, duration_sec, number_samples)  # this will always work in pandas
#
#plot_variant_2()
##--------------------------FUNCTIONS------------------------------
#def plot_variant_1():
#
#    # graph with samples
#    # create a list of X indexes
#
#    for name in channel_list:
#        plt.plot(x_axis_seconds, df[name], label=name)
#        print(df[name].head())
#
#    # set title
#    plt.title(FILENAME)
#
#    # set axis labels
#    plt.xlabel("time[s]")
#    plt.ylabel("Amplitude")
#
#    # Place a legend to the right of this smaller subplot.
#    plt.legend(bbox_to_anchor=(1.01, 0.8), loc=0, borderaxespad=0.)
#
#    # save current plot to file
#    plt.savefig(FILENAME + '-output.png', dpi=300, bbox_inches='tight')
#
#    plt.show()
#
#def plot_variant_2():
#    # set title
#    #plt.title(FILENAME)
#
#    fig = plt.figure()
#    ax = plt.subplot(111)
#
#
#    for name in channel_list:
#        ax.plot(x_axis_seconds, df[name], label=name)
#        #print(df[name].head())
#
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

        for channel in group.channels():
                channel_list.append(channel.name)
                #channel_name = channel.name
                # Access dictionary of properties:
                #properties = channel.properties
                # Access numpy array of data for channel:
                #data = channel[:]


        #Access a subset of data
        #data_subset = channel[0:5]
        #print(data_subset)

        time = channel.time_track()
        # convert tim = numpy array to pandas df
        time_df = pd.DataFrame(time, columns = ['Time'])
        print(time_df[:10])

        data_df = f["analog"].as_dataframe()
        #print(data_df[:10])

        # merge two pandas df
        #merged_df = pd.merge(left= time_df, right=data_df)
        merged_df = pd.concat([time_df, data_df], axis=1).reindex(time_df.index)
        #print(merged_df[:10])
        #print(df.tail())
        #print(df.shape)

        #merged_df = pd.DataFrame([1,2,3], columns = ['Time'])

        xlsx_filename = Path(file).stem + ".xlsx"
        xlsx_filepath = os.path.join(DATA_DIR, xlsx_filename)
        print(xlsx_filepath)
        merged_df.to_excel(xlsx_filepath, index = False)

    #print(channel_list)



    time = channel.time_track()
    #print(time)

        #print(f.groups())
        #print(f.channels())
        #channel = tdms_file[group_name][channel_name]
        #channel_data = channel[:]

#    tdms_file = TdmsFile.read(file)
#
#    group_list = []
#    channel_list = []
#
#    for group in tdms_file.groups():
#        group_name = group.name
#        group_list.append(group.name)
#
#        for channel in group.channels():
#            channel_list.append(channel.name)
#            channel_name = channel.name
#            # Access dictionary of properties:
#            properties = channel.properties
#            # Access numpy array of data for channel:
#            #data = channel[:]
#            #Access a subset of data
#            data_subset = channel[0:5]
#            print(data_subset)
#
#    print(group_list)
#    print(channel_list)
#
#    #---------------------------------------------------
#    #---------------------------------------------------
#    #---------------------------------------------------
#    group_name = group_list[0]
#
#    # read data and construct pandas dataframe
#    # df = tdms_file["group-name-string"].as_dataframe()
#    df = tdms_file[group_name].as_dataframe()
#
#    print(df.head())
#    print(df.tail())
#    print(df.keys())
#    print(df.shape)

    return df

# Get list of files in folder
def list_files(folder):
    file_list = []

    for file in os.listdir(folder):
        # only use .txt files
        if file.endswith(".tdms"):
            file_list.append(os.path.join(folder,file))

            #with open(files[-1], 'r') as f:
            #    content = f.read()

            #rewrite comma with dot
            #with open(files[-1], 'w') as f:
            #   f.write(content.replace(',','.'))
            #print(os.path.join(file))

    if(DEBUG):
        print(file_list)

    return file_list

def main():
    """main function"""
    # get path of all .txt files in DATA_DIR
    file_list = list_files(DATA_DIR)

    for file in file_list:
        print(file)
        df = import_data(file)
        #print(gp_dataframe.head())
        #result_list = analyse_data(gp_dataframe)
        #print(result_list)

#        #dut_name_list.append(os.path.splitext(file)[0])
#        #print(os.path.splitext(file)[0])
#
#        result_list.insert(0,file_list[j])
#        i = 0
#        for result in result_list:
#                cell = ipysheet.cell(row = j, column=i, value = result)
#                i = i + 1
#        j = j + 1
#
#    #print(myList)
#    #print(dut_name_list)
#    #graph_data()
#    #result_df = pd.DataFrame({ file : [1,2,3],'b': [4,5,6],'c': [7,8,9]})
#    #export_data_to_xlsx(result_df)
#    df_to_excel = ipysheet.to_dataframe(sheet)
#    df_to_excel.to_excel('test.xlsx')

if __name__ == "__main__":
    main()