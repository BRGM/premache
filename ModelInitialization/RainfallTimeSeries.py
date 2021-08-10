import pandas as pd
import numpy as np
import datetime
import time

def RainfallDepth_ToDaily(RainfallData,Format):
    '''
    Convert rainfall time series to daily time series
    '''

    file = RainfallData
    Rainfall_TimeSeries = pd.read_excel(file)
    tab = Rainfall_TimeSeries.values
    
    for i in range(tab.shape[0]):
        tab[i,0] = tab[i,0].date().strftime(Format)
        if tab[i,1]<0:
            tab[i,1] = 0
    
    tab_new=[]
    cumul = (tab[0,1])
    col=[]
    
    for i in range(tab.shape[0]-1):
        if tab[i+1,0] == tab[i,0] : 
            cumul += (tab[i+1,1])
        if not tab[i+1,0] == tab[i,0] : 
            tab_new.append([cumul])
            col.append(str(tab[i,0]))
            cumul= (tab[i+1,1])
    
    tab_new = np.transpose(tab_new).round(decimals=1)
    df = pd.DataFrame(tab_new,index=['Rainfall depth (mm)'],columns = col)
    
    return df