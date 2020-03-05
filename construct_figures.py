#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 20:20:22 2020

Functions to construct figures in dash app for modulated parasystole


@author: tbury
"""

import numpy as np
import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import prc_functions as pf
dic_prc = {'a':pf.prc_a,'b':pf.prc_b,'c':pf.prc_c,'d':pf.prc_d,
           'e':pf.prc_e,'pure':pf.prc_pure}


def mp_grid_plot(df_beats, df_rr, df_nib, tmax_plot):
    
    # Figure parameters
    ms = 7 # Marker size    

    # Plotting data up to tmax_plot
    df_rr_plot = df_rr[df_rr['Time (s)']<=tmax_plot]
    

    ##-----------Create grid figure------------#
    
    # Geometry of grid
    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{"colspan": 3}, None,None],
               [{}, {}, {}]])
    
            
    ## Add traces
  
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=df_rr_plot[df_rr_plot['Type']=='ss']['Time (s)'],
            y=df_rr_plot[df_rr_plot['Type']=='ss']['RR interval (s)'],
            marker=dict(
                color='Blue',
                size=ms
                ),
            name='NN'
        ),
        row=1, col=1            
                    
    )
            
    # Add trace of NV beats
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=df_rr_plot[df_rr_plot['Type']=='se']['Time (s)'],
            y=df_rr_plot[df_rr_plot['Type']=='se']['RR interval (s)'],
            marker=dict(
                color='Red',
                size=ms
                ),
            name='NV'
        ),
        row=1, col=1            
                    
    )
            
    # Add trace of VN beats
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=df_rr_plot[df_rr_plot['Type']=='es']['Time (s)'],
            y=df_rr_plot[df_rr_plot['Type']=='es']['RR interval (s)'],
            marker=dict(
                color='Green',
                size=ms
                ),
            name='VN'
        ),
        row=1, col=1            
    )
            
    # Add trace of VV beats
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=df_rr_plot[df_rr_plot['Type']=='ee']['Time (s)'],
            y=df_rr_plot[df_rr_plot['Type']=='ee']['RR interval (s)'],
            marker=dict(
                color='Purple',
                size=ms
                ),
            name='VV'
        ),
        row=1, col=1
    )
    
    # Add trace of NIB bar chart
    fig.add_trace(
        go.Bar(
            x=df_nib['NIB'],
            y=df_nib['Probability'],
            width=0.8,
            showlegend=False
        ),
        row=2, col=1
    )
    
    
    
    # Trace for distribution of NV and VN beats
    data_nv = df_rr[df_rr['Type']=='se']['RR interval (s)']
    data_vn = df_rr[df_rr['Type']=='es']['RR interval (s)']
    
    fig.add_trace(go.Histogram(x = data_nv,
                               histnorm='probability',
                               marker_color='Red',
                               showlegend=False), row=2, col=2)
    fig.add_trace(go.Histogram(x = data_vn,
                               histnorm='probability',
                               marker_color='Green',
                               showlegend=False), row=2, col=2)
    
    
    
    
    # Trace for distribution of VV intervals
    # Dataframe of ectopic beats and times
    df_vbeats = df_beats[df_beats['Type']=='e']
    # Compute interval between each V beat (round to 2dp)
    v_intervals = df_vbeats['Time'].diff().dropna().values
    v_intervals_round = [round(v,2) for v in v_intervals]
    
    fig.add_trace(go.Histogram(x = v_intervals_round,
                               histnorm='probability',
                               marker_color='Purple',
                               name='VV',
                               xbins={'start':0,'end':50,'size':0.2},
                               showlegend=False), row=2, col=3)
    
    
    
    ## Set axes properties
    
    # RR Interval axes
    fig.update_xaxes(title="Time (s)", row=1, col=1)
    ymax = np.ceil(max(df_rr['RR interval (s)']))
    fig.update_yaxes(title="Interval (s)",
                     range=[0,ymax],
                     fixedrange=True,
                     row=1,col=1)
    
    # NIB axes
    fig.update_xaxes(title="NIB",
                     type='category',
                     row=2,col=1)
    fig.update_yaxes(title="Probability",
                     range=[-0.05,1.05], row=2,col=1)
    
    # NV and VN distributions
    fig.update_xaxes(title="Interval (s)",
                     range=[0,2.2],
                     row=2,col=2)
    fig.update_yaxes(range=[-0.05,1.05], row=2,col=2)
    
    
    # VV distributions
    fig.update_xaxes(title="VV interval (s)",
                     range=[0,20],
                     row=2,col=3)
    fig.update_yaxes(range=[-0.05,1.05], row=2,col=3)



    # Adjust image padding
    fig.update_layout(margin={'l':0,'r':0,'t':40,'b':0}) 
    
    return fig






def prc_plot(prc):
    '''
    Plots all PRC functions lightly, and boldens prc.
    Input:
        prc: tag for PRC function: {'pure','a','b','c','d','e'}
    Output:
        figure
    '''
    
    # Plot parameters
    phi_min = 0
    phi_max = 1
    
    # X values
    phi_vals = np.arange(phi_min,phi_max,0.01)
    
    # Y values
    prc_pure_vals = [pf.prc_pure(phi) for phi in phi_vals]
    prc_a_vals = [pf.prc_a(phi) for phi in phi_vals]
    prc_b_vals = [pf.prc_b(phi) for phi in phi_vals]
    prc_c_vals = [pf.prc_c(phi) for phi in phi_vals]
    prc_d_vals = [pf.prc_d(phi) for phi in phi_vals]
    prc_e_vals = [pf.prc_e(phi) for phi in phi_vals]    
    
    # Include nan in prc_e_vals to emphasise discontinuity
    pos = np.where(phi_vals >= 0.6)[0][0]
    prc_e_vals[pos] = np.nan
    
    # Opacities
    dic_opacities = {x:(0.5 if x!=prc else 1) for x in dic_prc.keys()}
    dic_thickness = {x:(1 if x!=prc else 4) for x in dic_prc.keys()}
    
    # Set up figure
    fig = go.Figure()
    
    ## Add traces
    
    # prc pure
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_pure_vals,
                    mode='lines',
                    name='Pure',
                    opacity=dic_opacities['pure'],
                    line={'width':dic_thickness['pure']}))
    
    # prc a
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_a_vals,
                    mode='lines',
                    name='A',
                    opacity=dic_opacities['a'],
                    line={'width':dic_thickness['a']}))
    
    # prc b
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_b_vals,
                    mode='lines',
                    name='B',
                    opacity=dic_opacities['b'],
                    line={'width':dic_thickness['b']}))

    # prc c
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_c_vals,
                    mode='lines',
                    name='C',
                    opacity=dic_opacities['c'],
                    line={'width':dic_thickness['c']}))
    
    # prc d
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_d_vals,
                    mode='lines',
                    name='D',
                    opacity=dic_opacities['d'],
                    line={'width':dic_thickness['d']}))

    # prc e
    fig.add_trace(go.Scatter(x=phi_vals, y=prc_e_vals,
                    mode='lines',
                    name='E',
                    opacity=dic_opacities['e'],
                    line={'width':dic_thickness['e']}))

    # Layout of figure
    fig.update_layout(
            title={
                'text':'Phase response curves',
                'font':{'size':15},
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
#            legend_title='<b>PRC functions</b>',
            xaxis_title='Phi',
            yaxis_title='T/te',
            margin={'l':0,'r':0,'t':40,'b':0},
            height=270)
    
    
    return fig


#fig2 = mp_grid_plot(df_beats, df_rr, df_nib, tmax_plot)
#fig2.write_html('test2.html')
