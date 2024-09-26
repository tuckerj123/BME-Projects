#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 10:38:29 2024

@author: tuckerjohnsen
"""
# Import Data

# Import Packages
import numpy as np
from matplotlib import pyplot as plt
import project1_module as p1m

# Loading data into arrays
input_file = 'ecg_e0103_half1.npz'
    
ecg_voltage, fs, label_samples, label_symbols, subject_id, electrode, units = p1m.load_data_arrays(input_file)

# convert sample array to time

samples = np.arange(len(ecg_voltage))
t = 1/fs * samples

#%% Plot Raw signal

p1m.plot_raw_data(ecg_voltage, t, title=f"ECG Raw Data for Subject {subject_id}")

#%%
import numpy as np
from matplotlib import pyplot as plt
import project1_module as p1m

p1m.plot_events(label_samples, label_symbols, t, ecg_voltage)




