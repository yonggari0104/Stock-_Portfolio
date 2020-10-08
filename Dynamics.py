#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 19:08:47 2020

@author: kibeomlee
"""
import numpy as np

# Volatility and Correlation Modelling

class Dynamics(object):
    
    
    def rolling_vol(self, return_data, nwin):
        # Calculate moving average volatility 
        return np.sqrt(((return_data- return_data.mean())**2).rolling(window=nwin,axis=0).sum()[nwin:])
       
    def rolling_corr(self, data1, data2):
        