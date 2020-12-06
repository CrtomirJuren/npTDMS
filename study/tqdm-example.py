# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 11:45:00 2020

@author: crtom

If your filename is tqdm.py then you needed to rename it to another name. hope it will work.

"""


from tqdm import tqdm
from tqdm import trange
from time import sleep
from colorama import Fore

import pandas as pd
import numpy as np

def variant1():
    for i in tqdm(range(100), desc="loading a", unit ="iterations"):
        sleep(0.01)

def variant2():
    pbar = tqdm(total = 100)
    for i in range(10):
        sleep(0.1)
        pbar.update(10)
    pbar.close()

def variant3():
    pbar_length = 1000
    pbar = tqdm(total = pbar_length)
    
    iterations = 1000
    for i in range(iterations):
        sleep(0.01)
        pbar.update(pbar_length/iterations)
    pbar.close()
    
# nested progress bar

def variant4():
    # total number of files iteration = 10 files
    for i in trange(4, desc="1st loop"):
        for j in trange(5, desc="2nd loop"):
            for k in trange(50, desc="3rd loop", leave = False):
                sleep(0.01)
                
def variant5():
    # total number of files iteration = 10 files
    for i in trange(10, desc="Total Files Progress"):
        for j in tqdm(range(100), desc="Current File"):
            #for k in trange(50, desc="3rd loop", leave = False):
            sleep(0.01)

# colored progress bars
def variant6():
    # Cross-platform colored terminal text.
    color_bars = [Fore.BLACK,
        Fore.RED,
        Fore.GREEN,
        Fore.YELLOW,
        Fore.BLUE,
        Fore.MAGENTA,
        Fore.CYAN,
        Fore.WHITE]
    
    for color in color_bars:
        for i in trange(int(100),bar_format="{l_bar}%s{bar}%s{r_bar}" % (color, Fore.RESET)):
            sleep(0.01)
            
# pandas integration
def variant7():
    # create dataframe
    df = pd.DataFrame(np.random.rand(5,10))
    
    #register pandas progress with tqdm
    tqdm.pandas(desc="pandas progress")

    df.progress_apply(lambda x:x**2)


#--------------------------    
variant7()
