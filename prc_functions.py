#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 11:04:30 2020

Define phase response curve functions
From Courtemanche et al. (1989)

@author: tbury
"""


import numpy as np
import pandas as pd




## Define phase response curves

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
    



def prc_test(phi):
    if phi<0.9:
        return 0.9
    else:
        return phi
    
    
    
    
 



    