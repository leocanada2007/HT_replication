# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 11:49:54 2025

@author: leoca

"""
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt 

import seaborn as sns



def group_bar(df, group_var, val_var_left, val_var_right, rank_var):
    
    # 图2
    
    val_var = val_var_left + val_var_right
    
    df_group = df.groupby(group_var)[val_var].mean().reset_index()
    
    df_group = df_group.sort_values(rank_var, ascending=False)
    

    fig, ax = plt.subplots(figsize=(15, 10))
    
    df_group.plot.bar(x=group_var, y=val_var_left, rot=0, ax=ax)
    
    plt.xticks(rotation=90)
    
    df_group.plot.line(x=group_var, y=val_var_right, ax=ax, secondary_y=True)
    
    ax.tick_params(labelrotation=90)
    
    plt.show()


def group_rank(df, group_var_x, group_var_y, val_var):
    
    # 表格2
    
    df_group = df.groupby([pd.to_datetime(df[group_var_x]).dt.year, group_var_y])[val_var].mean().reset_index()
    
    df_group['rank'] = df_group.groupby(pd.to_datetime(df_group[group_var_x]))[val_var].rank('dense', ascending = False).astype(int)
    
    df_group.drop(columns = val_var, inplace = True)
    
    df_group = df_group.pivot(index=group_var_y, columns=group_var_x, values='rank')
    
    return df_group
    

def group_qcut_bar(df, group_var_x, quct, val_var):
    
    # 图3
    
    # Group 1: least volumne
    
    df_copy = df.copy()
    
    df_copy['Quintile'] = df_copy.groupby(pd.to_datetime(df_copy[group_var_x]).dt.year)[quct].transform(lambda x: pd.qcut(x, 5, labels=range(1,6)))
    
    df_group = df_copy.groupby([pd.to_datetime(df_copy[group_var_x]).dt.year, 'Quintile'])[val_var].mean().reset_index()
    
    sns.catplot(
    x=group_var_x,       # x variable name
    y=val_var,       # y variable name
    hue="Quintile",  # group variable name
    data=df_group,     # dataframe to plot
    kind="bar")
    
    plt.show()


def group_corr_with_one(df, group_var_x, var_list, var):
    
    # 表格3
    
    full_list = var_list + [var]
    
    df_copy = df.copy()[[group_var_x] + full_list]
    
    df_group = df_copy.groupby(pd.to_datetime(df[group_var_x]).dt.year)[full_list].corr().reset_index().drop(columns = var_list)
    
    df_group = df_group[df_group[var] != 1]
    
    df_group = df_group.pivot(index='level_1', columns=group_var_x, values=var)
    
    df_group['mean'] = df_group.mean(axis=1)
    
    return df_group
    
    
def relative_strenth(df, group_var_x, var_list):
    
    # 表格4-6
    
    df_copy = df.copy()

    df_copy[group_var_x] = pd.to_datetime(df_copy[group_var_x])
    df_copy['month_year'] = df_copy[group_var_x].dt.to_period('M')
    
    monthly_correlations = df_copy.groupby('month_year')[var_list].corr()
    mean_correlations = monthly_correlations.groupby(level=[1]).mean().sort_index(axis=1)
    std_correlations = monthly_correlations.groupby(level=[1]).std().sort_index(axis=1)
    relative_strenth = mean_correlations/std_correlations
    relative_strenth.replace([np.inf, -np.inf], np.nan, inplace=True)
    
    print(relative_strenth)
    
    
    return relative_strenth, mean_correlations, std_correlations



    
    
    