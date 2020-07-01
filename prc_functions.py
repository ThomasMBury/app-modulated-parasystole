#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 11:04:30 2020

Define phase response curve functions.

From Courtemanche et al. (1989)
    - prc_a
    - prc_b
    - prc_c
    - prc_d
    - prc_e
are taken from Figure 2.

From Schulte et al. (2002)
    - prc_schulte_a
    - prc_schulte_b
    - prc_schulte_c
are taken from Figure 10.

@author: tbury
"""


import numpy as np
import pandas as pd


def prc_sawtooth(phi, 
                 phi_c=0.82432, 
                 dPRC=0.9,
                 noise=0):
    '''
    Sawtooth PRC for the ectopic focus.
    Note that dPRC=1 corresponds to immediate activation
    of the focus for phi>phi_c


    Parameters
    ----------
    phi : float
        phase of the activation within the ectopic cycle.
        equal to x(mod te)/te, where x is the time at which
        the ectopic focus is reached with a signal (from ventricles)
        
    phi_c : float in [0,1]
        phase at which the sawtooth begins (sinus beat affects T)
        
    dPRC : float in [0,1]
        derivative of the PRC function from start of sawtooth to phi=1

    noise : standard deviation of noise applied to phi_c.
        Set noise=0 for no noise.
        
    
    Returns
    -------
    T/te : ratio of modulated time to te

    '''

    # If noise included, perturb phi_c
    if noise:
        phi_c = phi_c+np.random.normal(loc=0,scale=noise)
        phi_c = min(phi_c,1)
        phi_c = max(phi_c,0)
    
    # Find y_c, the y value for when phi = phi_c
    y_c = 1 - (1-phi_c)*dPRC  
    
    # If the phase of the activation is less than the critical phase
    # then there is no modulation (simplification)
    if phi < phi_c:
        y = 1
    else:
        y = y_c + dPRC*(phi-phi_c)
    
    return y





def prc_sawtooth_double(phi, 
                 phi_c=0.5, 
                 dPRC_post=1,
                 dPRC_pre=0.5,
                 noise=0):
    '''
    Double sawtooth PRC for the ectopic focus.
    Note that dPRC=1 corresponds to immediate activation
    of the focus for phi>phi_c


    Parameters
    ----------
    phi : float
        phase of the activation within the ectopic cycle.
        equal to x(mod te)/te, where x is the time at which
        the ectopic focus is reached with a signal (from ventricles)
        
    phi_c : float in [0,1]
        phase at which the sawtooth begins (sinus beat affects T)
        
    dPRC_post : float in [0,1]
        derivative of the PRC function for phi>phi_c
        
    dPRC_pre : float in [0,1]
        derivative of the PRC function for phi<phi_c
        
    noise : standard deviation of noise applied to phi_c.
        Set noise=0 for no noise.
        
    
    Returns
    -------
    T/te : ratio of modulated time to te

    '''

    # If noise included, perturb phi_c
    if noise:
        phi_c = phi_c+np.random.normal(loc=0,scale=noise)
        phi_c = min(phi_c,1)
        phi_c = max(phi_c,0)
    
    # For phi less than phi_c, there is elongation of ectopic period
    if phi < phi_c:
        y = 1 + dPRC_pre*phi
    # For phi greater than phi_c, there is shortening of ectopic period
    else:
        y = 1 - (1-phi)*dPRC_post
    
    return y



#--------------
# Approximate PRC functions used in Moe et al. (1973)
#–--------------

def prc_moe_1(phi):
    return prc_sawtooth_double(phi,
                               phi_c=0.6,
                               dPRC_post = 0.2/0.4,
                               dPRC_pre = 0.2/0.6)

def prc_moe_2(phi):
    return prc_sawtooth_double(phi,
                               phi_c=0.55,
                               dPRC_post = 0.2/0.45,
                               dPRC_pre = 0.2/0.55)


def prc_moe_3(phi):
    return prc_sawtooth_double(phi,
                               phi_c=0.5,
                               dPRC_post = 0.25/0.5,
                               dPRC_pre = 0.25/0.5)







def prc_a(phi):
     '''
     Phase response curve A given in Courtemanche 1989
         Input: phase of sinus beat in ectopic cycle
         Output: T/t_E normalised perturbed cycle length
     '''
     # Parameters
     C = 0.04
     phi_max = 0.25
     sigma = 0.12
     S = 0.1
     theta = 0.4
     N=10
     
     out = 1 + C*np.exp(-(phi-phi_max)**2/(sigma**2)) + \
                 S*(phi-1)*(phi**N)/(phi**N+theta**N)
     return out
 

def prc_b(phi):
     '''
     Phase response curve B given in Courtemanche 1989
         Input: phase of sinus beat in ectopic cycle
         Output: T/t_E normalised perturbed cycle length
     '''
     # Parameters
     C = 0.05
     phi_max = 0.4
     sigma = 0.12
     S = 0.5
     theta = 0.6
     N=10
     
     out = 1 + C*np.exp(-(phi-phi_max)**2/(sigma**2)) + \
                 S*(phi-1)*(phi**N)/(phi**N+theta**N)
     return out


def prc_c(phi):
     '''
     Phase response curve C given in Courtemanche 1989
         Input: phase of sinus beat in ectopic cycle
         Output: T/t_E normalised perturbed cycle length
     '''
     # Parameters
     C = 0.1
     phi_max = 0.3
     sigma = 0.08
     S = 0.85
     theta = 0.4
     N=40
     
     out = 1 + C*np.exp(-(phi-phi_max)**2/(sigma**2)) + \
                 S*(phi-1)*(phi**N)/(phi**N+theta**N)
     return out


def prc_d(phi):
     '''
     Phase response curve D given in Courtemanche 1989
         Input: phase of sinus beat in ectopic cycle
         Output: T/t_E normalised perturbed cycle length
     '''
     # Parameters
     C = 0.215
     phi_max = 0.35
     sigma = 0.057
     S = 0.92
     theta = 0.38
     N=22.74
     
     out = 1 + C*np.exp(-(phi-phi_max)**2/(sigma**2)) + \
                 S*(phi-1)*(phi**N)/(phi**N+theta**N)
     return out


def prc_e(phi):
     '''
     Phase response curve E (discontinuous) given in Courtemanche 1989
         Input: phase of sinus beat in ectopic cycle
         Output: T/t_E normalised perturbed cycle length
     '''
     # Parameters
     A = 0.35
     S = 1
     N_1 = 10
     theta_1 = 0.36
     N_2 = 40
     theta_2 = 0.6
     
     if phi < 0.6:
         out = 1 + A*phi**N_1/(phi**N_1+theta_1**N_1)
     else:
         out = 1 + S*(phi-1)* phi**N_2/(phi**N_2 + theta_2**N_2)
     return out
 
    
    
# Pure parasystole (sinus beat has no influence on ectopic period)
def prc_pure(phi):
    out = 1
    return out
    


# Note that the PRCs defined in Schulte consider DeltaT/te
# To get T/te, we need just add 1 to the output.
    
def prc_schulte_a(phi):
    if phi<0.5:
        out = 0
        
    elif 0.5<=phi<=0.75:
        x1 = 0.5
        x2 = 0.75
        y1 = 0
        y2 = -0.076
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
        
    else:
        x1 = 0.75
        x2 = 1
        y1 = -0.076
        y2 = 0
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1 
             
    return out + 1
    

    


def prc_schulte_b(phi):
    if phi<0.1:
        x1 = 0
        x2 = 0.1
        y1 = 0
        y2 = -0.6
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
        
    else:
        x1 = 0.1
        x2 = 1
        y1 = -0.6
        y2 = 0
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
        
             
    return out + 1
    
    



def prc_schulte_c(phi):
    if phi<0.3:
        x1 = 0
        x2 = 0.3
        y1 = 0
        y2 = 0.3
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
        
    elif 0.3<=phi<=0.4:
        x1 = 0.3
        x2 = 0.4
        y1 = 0.3
        y2 = -0.1
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
    
    else:
        x1 = 0.4
        x2 = 1
        y1 = -0.1
        y2 = 0
        m = (y2-y1)/(x2-x1)
        out = m*(phi-x1)+y1
        
        
    return out + 1   
    

    
    
    
   
 



    