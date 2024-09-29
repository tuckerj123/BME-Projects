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

p1m.plot_events(event_times_N, event_types[0], event_times_N, ecg_voltage_N)
p1m.plot_events(event_times_V, event_types[1], event_times_V, ecg_voltage_V)


#find the x limits of 2 Normal heartbeats and 1 arrythmia with panning on the figure
x_minimum = 2406.5
x_maximum = 2409.5
plt.xlim(x_minimum, x_maximum)

#%%Extract Trials 
event_time_length = 1 # each event signal is 1 second long

# Determine how many samples until the start of each sample
dt = 1/fs
time_before_label = 0.5
samples_to_start = int(time_before_label / dt)
number_of_samples = fs*event_time_length 

#create an array of all the start times of each signals
sample_N_start = event_samples_N - samples_to_start
sample_V_start = event_samples_V - samples_to_start

# extract all the arrays into a 2d array
trials_N_events = p1m.extract_trials(ecg_voltage, sample_N_start, number_of_samples)
trials_V_events = p1m.extract_trials(ecg_voltage, sample_V_start, number_of_samples)

#check if the shape matches expectations
if trials_N_events.shape == (len(sample_N_start), number_of_samples):
    print("The size is expected")
if trials_V_events.shape == (len(sample_V_start), number_of_samples):
    print("The size is expected")

#change time array so t=0 is at the time of the label
trial_to_plot = 0
trial_time_array = np.arange(time_before_label, time_before_label + event_time_length, dt)

#create plot of one trial per event type
plt.figure(2, clear=True)
plt.plot(trial_time_array, trials_N_events[trial_to_plot], label="Normal Heartbeat")
plt.plot(trial_time_array, trials_V_events[trial_to_plot], label="Arrythmia")

#annotate
plt.legend(loc=1)
plt.title(f"Normal Heartbeat {trial_to_plot +1} compared to Arrythmia {trial_to_plot +1}")
plt.xlabel('Time (s)')
plt.ylabel("Voltage (V)")
plt.grid()



