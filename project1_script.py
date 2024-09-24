#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:38:29 2024

@author: tuckerjohnsen
"""

# Import Data
# Import Packages
import numpy as np
from matplotlib import pyplot as py
from project1_module import load_data_arrays as lda

# Loading data into arrays
input_file = 'ecg_e0103_half1.npz'
    
ecg_voltage, fs, label_samples, label_symbols, subject_id, electrode, units = lda(input_file)

# convert sample array to time

samples = np.arange(len(ecg_voltage))
t = 1/fs * samples

#%% New Module 
