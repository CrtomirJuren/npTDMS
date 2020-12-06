# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 20:07:37 2020

@author: crtom
"""
import numpy as np

a = np.array([0,1,2])
b = np.array([10,11,12])
c = np.array([101,102,103])

d = np.array([3,4,5])
e = np.array([13,14,15])
f = np.array([104,105,106])

packet_1 = np.vstack((a,b,c))
print(packet_1)

packet_2= np.vstack((d,e,f))
print(packet_2)

data = np.hstack((packet_1, packet_2))
print(data)
"""
annel = np.hstack((channel, channel))
print(channel)

channel = np.array([1,2,3])
channel = np.vstack((channel, channel))
print(channel)
"""