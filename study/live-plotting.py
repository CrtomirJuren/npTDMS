import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import random
from itertools import count

plt.style.use("fivethirtyeight")

x_vals=[]
y_vals=[]

#plt.plot(x_vals,y_vals)

index = count()

class RingBuffer(object):
    def __init__(self, size, padding=None):
        self.size = size
        self.padding = size if padding is None else padding
        self.buffer = np.zeros(self.size+self.padding)
        self.counter = 0

    def append(self, data):
        """this is an O(n) operation"""
        data = data[-self.padding:]
        n = len(data)
        if self.remaining < n: self.compact()
        self.buffer[self.counter+self.size:][:n] = data
        self.counter += n

    @property
    def remaining(self):
        return self.padding-self.counter
    @property
    def view(self):
        """this is always an O(1) operation"""
        return self.buffer[self.counter:][:self.size]
    def compact(self):
        """
        note: only when this function is called, is an O(size) performance hit incurred,
        and this cost is amortized over the whole padding space
        """
        print('compacting')
        self.buffer[:self.size] = self.view
        self.counter = 0

rb = RingBuffer(10)


def init():  # only required for blitting to give a clean slate.

    plt.set_ydata([np.nan] * 2)
    #return line,

def animate(i):

    x_vals.append(next(index))
    x_vals.append(random.randint(0,5))

    plt.cla()
    plt.plot(x_vals,y_vals)

ani = animation.FuncAnimation(plt.gcf(), animate, init_func=init, interval=1) #blit=True

plt.xlabel("time[s]")
plt.ylabel("Amplitude")

plt.legend(loc="upper left")
plt.tight_layout()

plt.show()
