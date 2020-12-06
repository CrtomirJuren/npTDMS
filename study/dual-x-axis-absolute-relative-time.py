# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:54:56 2020

@author: crtjur
"""

# Based on question:
# https://stackoverflow.com/questions/7761778/matplotlib-adding-second-axes-with-transparent-background
import time
import numpy as np
import matplotlib.pyplot as plt

# Plot Data
rel_time = np.arange(0, 50)  # seconds
abs_time = 0
abs_time = rel_time + time.time()  # epoch time
y = np.array([1.1, 1.2, 1.2, 1.1, 1.2, 1.1, 1.3, 1.3, 1.2, 1.1, 1.4, 1.7,
              2.5, 2.6, 3.5, 4, 4.3, 4.8, 5, 4.9, 5.3, 5.2, 5.5, 5.1,
              5.4, 5.6, 5.1, 6, 6.2, 6.2, 5.5, 6.1, 5.4, 6.3, 6.2, 6.5,
              6.3, 6.1, 6.5, 6.6, 6.1, 6.6, 6.5, 6.4, 6.6, 6.5, 6.2, 6.6,
              6.4, 6.8])  # Arbitrary data

fig = plt.figure()
fig.subplots_adjust(bottom=0.25)  # space on the bottom for second time axis

host = fig.add_subplot(111)  # setup plot

p1 = host.plot(rel_time, y, 'b-')  # plot data vs relative time
host.set_xlabel("Relative Time [sec]")
host.set_ylabel("DATA")

newax = host.twiny()  # create new axis
newax.set_frame_on(True)
newax.patch.set_visible(False)
newax.xaxis.set_ticks_position('bottom')
newax.xaxis.set_label_position('bottom')
newax.spines['bottom'].set_position(('outward', 50))
#newax.plot(abs_time, y, 'k-')  # plot data vs relative time
newax.set_xlabel("Absolute Time [Epoch sec]")

#You need to specify limits for your x-axes.
host.set_xlim(rel_time[0],rel_time[-1])
newax.set_xlim(abs_time[0],abs_time[-1])

plt.show()