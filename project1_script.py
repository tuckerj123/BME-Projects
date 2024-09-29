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

#%%Plot event markers on the existing ECG
#divide samples by the labels in event_types
event_types = np.unique(label_symbols)
event_samples_N = label_samples[label_symbols == event_types[0]]
event_samples_V = label_samples[label_symbols == event_types[1]]

#seperate times by the samples
event_times_N = t[event_samples_N]
event_times_V = t[event_samples_V]

#seperate voltages by the samples
ecg_voltage_N = ecg_voltage[event_samples_N]
ecg_voltage_V = ecg_voltage[event_samples_V]

p1m.plot_events(event_times_N, event_types, event_times_N, ecg_voltage_N)

#find the x limits of 2 Normal heartbeats and 1 arrythmia with panning on the figure
x_minimum = 2406.5
x_maximum = 2409.5
plt.xlim(x_minimum, x_maximum)

#%%Extract Trials 
e
vent_time_length = 1 # each event signal is 1 second long

p1m.extract_trials(ecg_voltage, , fs*event_time_length)