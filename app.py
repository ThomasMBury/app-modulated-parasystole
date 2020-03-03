#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:51:44 2020

Create dash app for modulated parasystole
Run simulation within app so don't have to store large data file

@author: tbury

"""

import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from plotly.subplots import make_subplots
import plotly.graph_objects as go


from construct_figures import mp_grid_plot, prc_plot
import mod_para_funs as mp

import os



#-------------
# Launch the dash app
#---------------
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
print('Launching dash')

server = app.server

#----------------
# Simulate parasystole at default parameter values
#–----------------

# Simulation values
tmax = 1000
tburn = 100

# Default physiological values
ts = 1
te = 2.2
theta = 0.4
prc_tag = 'pure'


# Run simulation
df_beats = mp.run_mod_para(ts=ts, te=te, theta=theta, prc_tag=prc_tag,
               tmax=tmax, tburn=tburn)

# Compute NIB values
df_nib = mp.compute_nib(df_beats)

# Compute intervals data
df_rr = mp.compute_rr(df_beats)


# Dropdown options (choosing PRC function)
prcTags = ['pure','a','b','c','d','e'] # Phase response function (see prc_functions.py)
prc_opts = [{'label':x.upper(), 'value':x} for x in prcTags]




#--------------------
# Create plotly figures
#–--------------------

# Grid plot
tmax_plot = 200 # Max time for time series plot of intervals
fig_grid = mp_grid_plot(df_rr=df_rr, df_beats=df_beats,df_nib=df_nib, tmax_plot=tmax_plot)


# PRC plot
fig_prc = prc_plot(prc=prc_tag)


#--------------------
# App layout
#–-------------------

# Title information
title_text="<b>Modulated parasystole simulation</b><br>"

# Font sizes
size_slider_text = '15px'
size_title = '20px'


# Parameter bounds
theta_min = 0.1
theta_max = 0.6
theta_marks = {x:str(round(x,2)) for x in np.arange(theta_min,theta_max,0.2)}

te_min = 1
te_max = 3
te_marks = {x:str(round(x,2)) for x in np.arange(te_min,te_max,0.2)}


ts_min = 0.4
ts_max = 1.2
ts_marks = {x:str(round(x,2)) for x in np.arange(ts_min,ts_max,0.2)}



app.layout = html.Div([
        
    # Title section of app
    html.H1('Modulated parasystole simulation',
        style={'textAlign':'center',
               'fontSize':size_title,
               'color':'black'}
    ),
    
    # Dropdown menu and sliders
    html.Div(
        [
        # Dropdown for PRC function
        html.Label('Phase response curve',
                   style={'fontSize':size_slider_text}),
         
        dcc.Dropdown(id='prc_drop_down',
                     options=prc_opts,
                     value=prc_tag,
                     optionHeight=20,
                     searchable=False,
                     clearable=False),
                     
        html.Br(),       

        # Slider for ts
        html.Label('ts = {}'.format(ts),
                   id='ts_slider_text',
                   style={'fontSize':size_slider_text}),  
                   
        dcc.Slider(id='ts_slider',
                   min=ts_min, 
                   max=ts_max, 
                   step=0.01, 
                   marks=ts_marks,
                   value=ts
        ),        
      
                   
        # Slider for te
        html.Label('te = {}'.format(te),
                   id='te_slider_text',
                   style={'fontSize':size_slider_text}),  
                   
        dcc.Slider(id='te_slider',
                   min=te_min, 
                   max=te_max, 
                   step=0.01, 
                   marks=te_marks,
                   value=te
        ),
                   
                   
        # Slider for theta 
        html.Label('theta = {}'.format(theta),
                   id='theta_slider_text',
                   style={'fontSize':size_slider_text}),   
                   
        dcc.Slider(id='theta_slider',
                   min=theta_min, 
                   max=theta_max, 
                   step=0.01, 
                   marks=theta_marks,
                   value=theta
        ),        

        ],
        
        style={'width':'35%',
               'height':'300px',
               'fontSize':'10px',
               'padding-left':'5%',
               'padding-right':'0%',
               'padding-bottom':'0px',
               'vertical-align': 'middle',
               'display':'inline-block'},
    ),
        

    # Plot PRC functions
    html.Div(
        [dcc.Graph(id='prc_plot',
                   figure = fig_prc,
                   config={'displayModeBar': False})],
        style={'width':'45%',
               'height':'300px',
               'fontSize':'10px',
               'padding-left':'10%',
               'padding-right':'5%',
               'vertical-align': 'middle',
               'display':'inline-block'},
    ),



            
    # Grid plot     
    html.Div(
        [dcc.Graph(id='grid_plot',figure = fig_grid)]
    )

  
])



#–-------------------
# Callback functions
#–--------------------

  
# Update text for sliders             
@app.callback(
        [Output('ts_slider_text','children'),
         Output('te_slider_text','children'),
         Output('theta_slider_text','children')
         ],
        [Input('prc_drop_down','value'),
         Input('ts_slider','value'),
         Input('te_slider','value'),
         Input('theta_slider','value')
         ]
)

def update_slider_text(prc,ts,te,theta):
    
    # Text for ts slider
    text_ts = 'ts = {}'.format(ts)
    
    # Text for te slider
    text_te = 'te = {}'.format(te)    
    
    # Text for theta slider
    text_theta = 'theta = {}'.format(theta)   

    return text_ts, text_te, text_theta
            
         

# Update PRC plot
@app.callback(Output('prc_plot','figure'),
              [Input('prc_drop_down','value')])

def update_fig_prc(prc):
    fig_prc = prc_plot(prc=prc)
    return fig_prc


   
# Update grid plot            
@app.callback(Output('grid_plot','figure'),
              [Input('prc_drop_down','value'),
               Input('theta_slider','value'),
               Input('te_slider','value')])

def update_grid(prc, theta, te):
    # Run simulation with new parameter values
    df_beats = mp.run_mod_para(ts=ts, te=te, theta=theta, prc_tag=prc,
               tmax=tmax, tburn=tburn)
    # Compute NIB values
    df_nib = mp.compute_nib(df_beats)
    # Compute intervals data
    df_rr = mp.compute_rr(df_beats)

    # Updated figure
    fig = mp_grid_plot(df_rr=df_rr, df_beats=df_beats,df_nib=df_nib, tmax_plot=tmax_plot)
    
    return fig





#-----------------
# Add the server clause
#–-----------------

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
    
