# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:09:49 2020

@author: crtjur
"""

# imports
import numpy as np
import pandas as pd

import nptdms
from nptdms import TdmsFile

import time
import datetime as dt
#from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as md

#---------------------------------------------------
#---------------------------------------------------
#---------------------------------------------------
# configurations
#FILEPATH = "DAQ-sim.tdms"
FILENAME = "test_4_DUT_18"
FILEPATH = FILENAME + ".tdms"


# read in memory whole tdms file
tdms_file = TdmsFile.read(FILEPATH)

#---------------------------------------------------
#---------------------------------------------------
#---------------------------------------------------
# read data from tdms and put it in dataframe
metadata = TdmsFile.read_metadata(FILEPATH)
print(metadata.properties)


# read properties - all groups, all channels
group_list = []
channel_list = []

for group in tdms_file.groups():
    group_name = group.name
    group_list.append(group.name)
    #print(group_name)
    for channel in group.channels():
        channel_list.append(channel.name)
        channel_name = channel.name
        #print(channel_name)
        # Access dictionary of properties:
        properties = channel.properties
        # Access numpy array of data for channel:
        data = channel[:]
        # Access a subset of data
        data_subset = channel[0:5]
        #print(data_subset)

print(group_list)
print(channel_list)

#---------------------------------------------------
#---------------------------------------------------
#---------------------------------------------------
group_name = group_list[0]

# read data and construct pandas dataframe
# df = tdms_file["group-name-string"].as_dataframe()
df = tdms_file[group_name].as_dataframe()

print(df.head())
print(df.tail())
print(df.keys())
print(df.shape)

number_samples = df.shape[0]
number_columns = df.shape[1]
print(number_samples)
print(number_columns)

#get df header = channel names
column_names = df.columns.tolist()
print(column_names)

# get more properties from selected channel
channel_name = channel_list[0]
channel = tdms_file[group_name][channel_name]

wf_start_time_dt64 = channel.properties['wf_start_time']
print(wf_start_time_dt64)

dt = channel.properties['wf_increment']
print(dt)
# print(type(dt)) = float
# now we can calculate total test time in seconds
duration_milisec = 1000*number_samples * dt
print(duration_milisec)

# ENABLE THIS PART FOR EXCEL CONVERSION
# SAVE TO DATEAFRAME TO EXCEL
#df.to_excel("converted-tdms.xlsx")

#---------------------------------------------------
#---------------------------------------------------
#---------------------------------------------------
# HERE TIMESTAMP CONVERSION STARTS.
print("type(dt64): ")
print(type(wf_start_time_dt64))
# transform wf_start_time to float
wf_start_time_float = (wf_start_time_dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
print("type(dt64): ")
print(type(wf_start_time_float))
#print(type(wf_start_time_float)) = numpy.float64

# create list of timestamps
timestamps = np.linspace(start, end, delta)
print("type(start): ")
print(type(start))
print("type(end): ")
print(type(end))
print("type(delta): ")
print(type(delta))

# create dates
dates=[dt.datetime.fromtimestamp(ts) for ts in timestamps]

# graph with samples
# create a list of X indexes

x_axis_seconds = np.linspace(1, duration_sec, number_samples)  # this will always work in pandas



for name in channel_list:
    plt.plot(x_axis_seconds, df[name], label=name)
    print(df[name].head())

# set title, axis legend
#plt.title("DAQ-sim.tdms")FILENAME
#plt.title(FILENAME)
plt.xlabel("time[s]")


# this adds names to label
#y_labels_string = " ".join(channel_list)
#plt.ylabel(y_labels_string)
plt.ylabel("Amplitude")

# plot first axis

#plt.legend(loc="center right")
# Place a legend to the right of this smaller subplot.
# good right outside top position
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.legend(bbox_to_anchor=(1.01, 0.8), loc=0, borderaxespad=0.)

#fig.tight_layout()
#plt.savefig('output.png', dpi=300)
plt.savefig('plot-output.png', dpi=300, bbox_inches='tight')
# save current plot to file
#plt.savefig('DAQ-sim.png')

plt.show()