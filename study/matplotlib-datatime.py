# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 13:22:05 2020

@author: crtjur
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

np.random.seed(1)

N = 100
y = np.random.rand(N)

start = dt.datetime.now()
duration = 10
delta = dt.timedelta(days=1)
print(delta.total_seconds())

end = start + dt.timedelta(days=100)
days = mdates.drange(start, end, delta)
print(days)

print("type(start): ")
print(type(start))
print("type(end): ")
print(type(end))
print("type(delta): ")
print(type(delta))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.plot(days,y)
plt.gcf().autofmt_xdate()
plt.show()