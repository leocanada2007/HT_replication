# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 20:21:48 2025

@author: leoca
"""

import pandas as pd

def process_raw(path, data, varname):
    
    df = pd.read_excel(path + data)
    
    df.rename(columns = {'Unnamed: 0' : 'Date'}, inplace= True)
    
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    df = pd.melt(df, id_vars='Date', value_vars=df.columns[1:])
    
    df.columns = ['Date', 'Sector', varname]
    
    
    return df
