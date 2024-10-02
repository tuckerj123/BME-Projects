#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
project1_script.py

Python script to analyze heart activity over a set time from an ECG
Then complete data analysis and visualization of beats of different types
that may be indicative of health effects.

Tucker Johnston & Ryan Siegel

ChatGPT was utilized to explain how to take element-wise means
TAs (Haorui Sun) provided recommendation to skip data from the trials that are incomplete

Created on Tue Sep 24 10:38:29 2024

@author: tuckerjohnsen
"""

# Import necessary data and libraries

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

# Save plot
plt.savefig('raw_data_plot.png')

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

#plot signals of both event types
p1m.plot_events(event_times_N, event_types[0], event_times_N, ecg_voltage_N)
p1m.plot_events(event_times_V, event_types[1], event_times_V, ecg_voltage_V)


#find the x limits of 2 Normal heartbeats and 1 arrythmia with panning on the figure
x_minimum = 2406.5
x_maximum = 2409.5
plt.xlim(x_minimum, x_maximum)

# Save plot
plt.savefig('labeled_raw_data_plot.png')

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
trial_to_plot = 1
trial_time_array = np.arange(-time_before_label, -time_before_label + event_time_length, dt)

#create plot of one trial per event type
plt.figure(2, clear=True)
plt.plot(trial_time_array, trials_N_events[trial_to_plot], label="Normal Heartbeat")
plt.plot(trial_time_array, trials_V_events[trial_to_plot], label="Arrythmia")

#annotate
plt.legend(loc=1)
plt.title(f"Normal Heartbeat {trial_to_plot +1} compared to Arrythmia {trial_to_plot +1}")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.grid()

# Save plot
plt.savefig('extracted_trial_plot.png')

#%% Plot Trial Means
trial_duration_seconds = 1 #how many seconds in each trial

#plot wrapper function of mean and std
symbols, trial_time, mean_trial_signal = p1m.plot_mean_and_std_trials(ecg_voltage, label_samples, label_symbols, trial_duration_seconds, fs, units, title=f"Mean ECG for Subject {subject_id}")

# Save plot
plt.savefig('event_mean_with_std_plot.png')

#%% Saving Array and Plots
p1m.save_means(symbols, trial_time, mean_trial_signal, out_filename = f"ecg_means_{subject_id}.npz")

# Test Saved Data
infile = "ecg_means_e0103.npz"
loaded_data = np.load(infile)
loaded_symbols = loaded_data['arr_0']
loaded_times = loaded_data['arr_1']
loaded_means = loaded_data['arr_2']
if np.array_equal(loaded_symbols, symbols):
    print("Loaded Matches Saved")
else:
    print("No Match")
if np.array_equal(loaded_times, trial_time):
    print("Loaded Matches Saved")
else:
    print("No Match")
if np.array_equal(loaded_means, mean_trial_signal):
    print("Loaded Matches Saved")
else:
    print("No Match")









