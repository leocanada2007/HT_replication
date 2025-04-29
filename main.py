# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 11:05:36 2025

@author: leoca
"""

# =============================================================================
# 
# 0. Preliminaries
#
# =============================================================================

# Data 

import pandas as pd
import numpy as np

# Plot

import matplotlib.pyplot as plt 

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'

import seaborn as sns

# Chinese Text

from matplotlib import font_manager
fontP = font_manager.FontProperties()
fontP.set_family('SimHei')
fontP.set_size(14)

plt.rcParams['font.sans-serif'] = ['SimHei']


# Project Directories

raw_data_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\data\\raw\\'

derived_data_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\data\\derived\\'

sample_data_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\data\\sample\\'

code_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\HT_Replication\\codes\\'

results_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\HT_Replication\\results\\'

figs_folder = 'C:\\Users\\leoca\\OneDrive\\HT_Replication\\HT_Replication\\figs\\'

import os

os.chdir(code_folder)

import utils

#%%

# =============================================================================
# 
# 1. load data
#
# =============================================================================

PBMRQ = utils.process_raw(raw_data_folder, '申万一级_PBMRQ.xlsx', 'PBMRQ')
PCFncf = utils.process_raw(raw_data_folder, '申万一级_PCFncf.xlsx', 'PCFncf')
PETTM = utils.process_raw(raw_data_folder, '申万一级_PETTM.xlsx', 'PETTM')
PSTTM = utils.process_raw(raw_data_folder, '申万一级_PSTTM.xlsx', 'PSTTM')

df = PBMRQ.merge(PCFncf, on = ['Date', 'Sector'], how = 'inner')
df = df.merge(PETTM, on = ['Date', 'Sector'], how = 'inner')
df = df.merge(PSTTM, on = ['Date', 'Sector'], how = 'inner')

df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

#%%

# =============================================================================
# 
# 2. Descriptive Statistics
#
# =============================================================================

# 图2

utils.group_bar(df, 'Sector', ['PBMRQ', 'PCFncf'], ['PETTM', 'PSTTM'], 'PBMRQ')

# 表格2

t2 = utils.group_rank(df,'Date', 'Sector', 'PCFncf')

# 图3

temp = df[(df['Date'] >= '2007-01-01') & (df['Date'] <= '2015-12-31')]

utils.group_qcut_bar(temp, 'Date', 'PBMRQ', 'PCFncf')

# 表格3 (应当基于个股)

t3 = utils.group_corr_with_one(df, 'Date', ['PCFncf', 'PETTM', 'PSTTM'], 'PBMRQ')    

# 表格4-6

temp = df[(df['Date'] >= '2022-01-01') & (df['Date'] <= '2024-12-31')]

t4, t5, t6 = utils.relative_strenth(temp, 'Date', ['PBMRQ', 'PCFncf', 'PETTM', 'PSTTM'])


