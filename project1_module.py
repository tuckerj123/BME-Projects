#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:13:13 2024

@author: tuckerjohnsen
"""
import numpy as np
import matplotlib.pyplot as plt



def load_data_arrays(input_file):

    data = np.load(input_file)
    print(data.files)
    
    ecg_voltage = data['ecg_voltage']
    fs = data['fs']
    label_samples = data['label_samples']
    label_symbols = data['label_symbols']
    subject_id = data['subject_id']
    electrode = data['electrode']
    units = data['units']
    return ecg_voltage, fs, label_samples, label_symbols, subject_id, electrode, units

def plot_raw_data(signal_voltage, signal_time, units="V", title=""):
    # Plot data
    plt.figure(1, clear=True)
    plt.plot(signal_time, signal_voltage)

    #annotate
    plt.xlabel('Time (s)')
    plt.ylabel(f"Voltage ({units})") # arbitrary units
    plt.grid()
    plt.title(title)
    
def plot_events(label_samples, label_symbols, signal_time, signal_voltage):
    
    #plot dots for each event in the signal
    plt.figure(1)
    plt.plot(signal_time, signal_voltage, label=f"{label_symbols} Events", linestyle="", marker="o")

    #add a legend
    plt.legend(loc=4)
    
def extract_trials(signal_voltage, trial_start_samples, trial_sample_count):
    # initialize array for sampling
    trials = np.zeros((len(trial_start_samples), trial_sample_count))
    
    #replace each row in the array with a trial 
    for trial_index in range(len(trial_start_samples)):
        #calculate the start and final indices
        trial_start = trial_start_samples[trial_index]
        trial_end = trial_start_samples[trial_index]+trial_sample_count

    #Remove any trials that are not complete
        # first few samples have negative indices, this makes any negative indices = 0
        if trial_start <0:
            samples = np.full(trial_sample_count,np.nan)
            trials[trial_index, :] = samples
        
        #last few trials have end indices that are too big, this sets those indices = -1 
        elif trial_end > len(signal_voltage):  
            samples = np.full(trial_sample_count,np.nan)
            trials[trial_index, :] = samples
        
        #if the start and end indices are within the range, just replace the array
        else:
            trials[trial_index,:] = signal_voltage[trial_start:trial_end]
    
    return trials
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    