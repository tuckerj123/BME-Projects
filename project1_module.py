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
    
    #divide samples by the labels in event_types
    event_types = np.unique(label_symbols)
    event_samples_N = label_samples[label_symbols == event_types[0]]
    event_samples_V = label_samples[label_symbols == event_types[1]]
    
    #seperate times by the samples
    event_times_N = signal_time[event_samples_N]
    event_times_V = signal_time[event_samples_V]
    
    #seperate voltages by the samples
    event_signals_N = signal_voltage[event_samples_N]
    event_signals_V = signal_voltage[event_samples_V]

    
    print(len(event_samples_N))
    
    
    

    
    
    
    
    
    
    
    
    
    
    