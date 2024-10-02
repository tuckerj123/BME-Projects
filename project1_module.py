#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 11:13:13 2024

@author: tuckerjohnsen
"""
#import libraries
import numpy as np
import matplotlib.pyplot as plt

def load_data_arrays(input_file):
    #load data and show the different variables
    data = np.load(input_file)
    print(data.files)
    
    #declare variables with the same names as the npz file
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
    plt.ylabel(f"Voltage ({units})")
    plt.grid()
    plt.title(title)
    plt.show()
    
def plot_events(label_samples, label_symbols, signal_time, signal_voltage):
    #plot dots for each event in the signal on the same plot done in plot_raw_data()
    plt.figure(1)
    plt.plot(signal_time, signal_voltage, label=f"{label_symbols} Events", linestyle="", marker="o")

    #add a legend
    plt.legend(loc=4) #4 corresponds to correct location
    
def extract_trials(signal_voltage, trial_start_samples, trial_sample_count):
    # initialize array for sampling
    trials = np.zeros((len(trial_start_samples), trial_sample_count))
    
    #replace each row in the array with a trial 
    for trial_index in range(len(trial_start_samples)):
        #calculate the start and final indices
        trial_start = trial_start_samples[trial_index]
        trial_end = trial_start_samples[trial_index]+trial_sample_count

    #if start index is negative, then signal is not complete and should be replaced with nan values
        if trial_start <0:
            samples = np.full(trial_sample_count,np.nan)
            trials[trial_index, :] = samples
        
    #if end index is outside length of file, then signal is not complete and should be replaced with nan values
        elif trial_end > len(signal_voltage):  
            samples = np.full(trial_sample_count,np.nan)
            trials[trial_index, :] = samples
        
        #if the start and end indices are within the range, just replace the array with the signals for the trial
        else:
            trials[trial_index,:] = signal_voltage[trial_start:trial_end]
    
    return trials
    
def plot_mean_and_std_trials(signal_voltage, label_samples, label_symbols, trial_duration_seconds, fs, units, title):
    # Create figure
    plt.figure(2, clear = True)
    plt.grid()
    
    #find what different event types are
    symbols = np.unique(label_symbols)
    
    # determine number of samples in each trial
    dt = 1/fs #how much time passes between each index
    time_before_label = trial_duration_seconds /2 # centers trial at time = 0s
    samples_to_start = int(time_before_label / dt) #turn time into number of indices before the label
    number_of_samples = fs*trial_duration_seconds #determine how many samples in each trial
    
    #create time array for all times at the indices
    trial_time = np.arange(-time_before_label, -time_before_label + trial_duration_seconds, dt)
    
    # Create new array to store mean trial signals
    mean_trial_signal = np.zeros((len(symbols), number_of_samples))
    
    # Find event type trial means and standard deviation arrays
    for event_type_index in range(len(symbols)):
        # FInd the signals of all the trials of the specific event type
        event_samples = label_samples[label_symbols == symbols[event_type_index]]
        sample_start = event_samples - samples_to_start 
        trials = extract_trials(signal_voltage, sample_start, number_of_samples)
    
        # Data Analysis
        trial_mean = np.nanmean(trials, axis = 0)
        trial_std = np.nanstd(trials, axis = 0)
        
        # Store Data for returning
        mean_trial_signal[event_type_index] = trial_mean
        
        # Find error below and above mean
        error_below_mean = trial_mean - trial_std
        error_above_mean = trial_mean + trial_std
    
        # Plot mean with error bars
        plt.plot(trial_time, trial_mean, label = f"{symbols[event_type_index]} trial mean", linewidth = 2)
        plt.fill_between(trial_time, error_below_mean, error_above_mean, alpha = 0.3, label = f"{symbols[event_type_index]} trial mean +/- stddev")
        
        # Annotate
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (v)")
        
    plt.legend()
    
    return symbols, trial_time, mean_trial_signal

def save_means(symbols, trial_time, mean_trial_signal, out_filename = 'ecg_means.npz'):
    np.savez(out_filename, symbols, trial_time, mean_trial_signal)
    return
    
    
    
    
    