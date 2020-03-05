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
te = 2.2
theta = 0.14
prc_tag = 'pure'
tmax_plot = 200

df_beats = mp.run_mod_para(ts=ts, te=te, theta=theta, prc_tag=prc_tag,
               tmax=tmax, tburn=tburn)
df_nib = mp.compute_nib(df_beats)
df_rr = mp.compute_rr(df_beats)


# Run gridplot function
fig = cf.mp_grid_plot(df_beats, df_rr, df_nib, tmax_plot)
# Export to html as test
fig.write_html('test.html')










