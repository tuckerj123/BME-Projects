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
    plt.plot(signal_time, event_signals_N, label="Normal Events", linestyle="", marker="o")
    plt.plot(event_times_V, event_signals_V, label="Arrythmia Events", linestyle="", marker="o")

    #add a legend
    plt.legend(loc=4)
    
def extract_trials(signal_voltage, trial_start_samples, trial_sample_count):
    trials = np.zeros((len(signal_voltage),trial_sample_count))
    
    
    
    print(trials)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    