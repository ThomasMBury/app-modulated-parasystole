#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 16:55:07 2020

Testing functions

@author: tbury
"""




import numpy as np
import pandas as pd

import sys
sys.path.insert(1, '../')


# Import functions

import mod_para_funs as mp
import construct_figures as cf




# Generate beats and compute stats
tmax = 1000
tburn = 100
ts = 1
te = 2.3
theta = 0.4
prc_tag = 'b'
tmax_plot = 200

df_beats = mp.run_mod_para(ts=ts, te=te, theta=theta, prc_tag=prc_tag,
               tmax=tmax, tburn=tburn)
df_nib = mp.compute_nib(df_beats)
df_rr = mp.compute_rr(df_beats)



# Construct VN vs VV graph

# Collect cases where NIB = 1, i.e. sequence VNV from df_rr
list_dic_nib1 = []
for i in range(len(df_rr)):
    df_temp = df_rr.iloc[i:i+2]
    # If this sequence has the form VNV
    if all(df_temp['Type'].values==['es','se']):
        # Compute and store VS and VV interval
        dic_temp = {'Time (s)': [df_temp.iloc[0]['Time (s)']],
                    'VS (s)': [df_temp.iloc[0]['RR interval (s)']],
                    'VV (s)': [df_temp['RR interval (s)'].sum()]}
        df_store = pd.DataFrame(dic_temp)
        list_dic_nib1.append(df_store)

df_intervals_nib1 = pd.concat(list_dic_nib1, ignore_index=True)

# Scatter plot
df_intervals_nib1.plot(kind='scatter', x='VS (s)', y='VV (s)')



## Run gridplot function
#fig = cf.mp_grid_plot(df_beats, df_rr, df_nib, tmax_plot)
## Export to html as test
#fig.write_html('test.html')










