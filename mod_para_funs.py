#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:26:28 2020


Functions to
    - Simulate modulated parasytole according to Courtemanche et al. (1989)
    - Compute the NIB (number of intervening sinus beats)
    - Compute the intervals between each type of beat
    
@author: tbury
"""


import numpy as np
import pandas as pd

# Import phase response curve functions
from prc_functions import prc_a, prc_b, prc_c, prc_d, prc_e, prc_pure

dic_prc = {'a':prc_a,'b':prc_b,'c':prc_c,'d':prc_d,
           'e':prc_e,'pure':prc_pure}



def run_mod_para(ts=1, te=1.8, theta=0.2, tmax=1000, tburn=100, prc_tag='pure'):
    '''
    Function to simulate modulated parasystole.
    Notation of beat types
    s: expressed sinus beat
    e: expressed ectopic beat
    xs: concealed sinus beat
    xe: concealed ectopic beat
    
    Input:
        ts: period of sinus rhythm
        te: period of ectopic rhythm
        theta: refractory period of the heart
        tmax: time to run simulation up to
        tburn: length of burn in period that is discarded (to remove transients)
        prc: phase response curve from {'pure','a','b','c','d','e'} - see Courtemanche for functions
    Output:
        df_beats: pandas dataframe of beats at each time
    '''
    
    
    # List of beats (tuple (time,beat_type))
    list_beats = []
    
    # Assign PRC curve
    prc = dic_prc[prc_tag]
    
    # Set base modulated time to be equal to te
    te_mod = te
    
    # Simulate beats
    # Assume an expressed sinus beat at t=0
    # and an ectopic beat at t= theta+(ts-theta)/2 (ensures it is expressed)
    
    t_sinus = 0
    list_beats.append((t_sinus,'s'))
    t_ectopic = theta + (ts-theta)/2
    list_beats.append((t_ectopic,'e'))
    
    # Iterate system until sinus time t_sinus<tmax+tburn
    while t_sinus < tmax+tburn:
        

        # Obtain time of subsequent sinus beat
        t_sinus_next = t_sinus + ts
        # Obtain projected time of subsequent ectopic beat (using PRC if last beat was expressed sinus)
        if list_beats[-1][1] != 's':
            t_ectopic_next = t_ectopic + te
        else:
            # Compute phase of sinus beat in current ectopic cycle
            phi = (t_sinus - t_ectopic)/te
            # Compute modulated ectopic period
            te_mod = prc(phi)*te_mod
            t_ectopic_next = t_ectopic + te_mod
        
            
        # If the next beat is a sinus beat
        if t_sinus_next < t_ectopic_next:
            # The sinus beat is concealed if preceded directly by expressed ectopic beat
            if list_beats[-1][1] == 'e':
                beat_type = 'xs'
            # Otherwise the beat takes place
            else: beat_type = 's'
            # Update t_sinus
            t_sinus = t_sinus_next
            # Append beat list
            list_beats.append((t_sinus,beat_type))
            
            
        # If the next beat is an ectopic beat
        else:
            # The ectopic beat is concealed if occurs during refractory period of previous sinus beat
            if (list_beats[-1][1] == 's') & (t_ectopic_next < list_beats[-1][0]+theta):
                beat_type = 'xe'
            # Otherwise beat takes place
            else: beat_type = 'e'
            # Update t_ectopic
            t_ectopic = t_ectopic_next
            # Reset te_mod
            te_mod = te
            # Append beat list
            list_beats.append((t_ectopic,beat_type))
            
    # Put into a dataframe
    dict_beats = {'Time': [tup[0] for tup in list_beats],
                  'Type': [tup[1] for tup in list_beats]}
    df_beats_temp = pd.DataFrame(dict_beats)
    
    # Remove burn-in period and reset start time to zero
    df_beats=df_beats_temp[df_beats_temp['Time']>=tburn].copy()
    df_beats['Time'] = df_beats['Time']-tburn
    df_beats.reset_index(drop=True)
    
    # Return data frame of beats
    return df_beats





def compute_nib(df_beats):
    '''
    Function to compute the NIB from df_beats
    NIB refers to the number of expressed sinus beats between two expressed ectopic
    beats, i.e. the number of 's' between two 'e's
    
    Input:
        df_beats: dataframe for beat type at each time
    Output:
        df_nib: dataframe for NIB
    '''

        
    list_type = df_beats['Type'].values
    list_nib = []
    i = 0
    count = 0
    while i < len(list_type):
        if list_type[i]=='e':
            i+=1
            # Count the number of 's' occurences until next 'e'
            while (list_type[i]!='e')&(i<len(list_type)-1):
                if list_type[i]=='s':
                    count+=1
                    i+=1
                else:
                    i+=1
            list_nib.append(count)
            count = 0
        else:
            i+=1
    
    # If list_nib is empty (no ectopic beats)
    if len(list_nib)==0:
        list_nib = ['silence']
    # Remove last element of list_nib if is less than the max nib as not relevant
    elif list_nib[-1]<max(list_nib):
        list_nib = list_nib[:-1]
        
    # Collect and count occurences
    series_nib = pd.Series(list_nib, name='NIB')
    nib_counts = series_nib.value_counts(normalize=True)
    df_nib = pd.DataFrame({'NIB':nib_counts.index, 'Probability':nib_counts.values})
    
    # Sort df_nib so NIB is in ascendinig order
    df_nib.sort_values('NIB', ascending=True, inplace=True)
    
    return df_nib




def compute_rr(df_beats):
    '''
    Function to compute the interval lengths between expressed beats
    Input:
        df_beats: dataframe for beat type at each time
    Output:
        df_rr: dataframe containing interval lengths and types
    '''

    # Select only expressed beats
    df_beats_express = df_beats[df_beats['Type'].isin(['s','e'])]
    
    list_rr_times = []
    list_rr_types = []
    list_rr_lengths = []
        
        
    # Loop through intervals
    for i in range(len(df_beats_express)-1):
        
        df_temp = df_beats_express.iloc[i:i+2]
    
        # Compute RR interval type
        beats = df_temp['Type'].values
        rr_type = beats[0]+beats[1] # combining strings
        # Append to list
        list_rr_types.append(rr_type)
        
        # Compute RR interval length (in seconds)
        rr_length = df_temp['Time'].iloc[1]-df_temp['Time'].iloc[0]
        # Append to list
        list_rr_lengths.append(rr_length)
        
        # Set the time value of the interval to be that of the second beat
        rr_time = df_temp['Time'].iloc[1]
        # Append to list
        list_rr_times.append(rr_time)
            
            
    # Construct a dataframe containing rr info 
    dic_rr_info = {'Time (s)':list_rr_times, 
                   'RR interval (s)':list_rr_lengths,
                   'Type': list_rr_types}
    df_rr = pd.DataFrame(dic_rr_info)
    
    return df_rr






