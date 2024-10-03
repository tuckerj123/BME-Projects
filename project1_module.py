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
    """
    This function loads the input file, prints the names of the elements, then
    assigns each of the elements of the input file to a corresponding variable.
    These variables are then returned.
    
    Parameters
    ----------
    input_file : .npz
        This file has a similar function to a dictionary.
        It contains pre-recorded ECG data in a list that can be accessed by
        using the name of the variable. Specifically this .npz file
        contains ECG voltages, sampling frequency, the samples, 
        symbols (markers for normal vs. abnormal heart beats), the subject ID,
        electrode data, and the units.
        
    Returns
    -------
    ecg_voltage : Array of floats
        A 1-dimensional array contains all voltages recorded in this sample,
        measured in mV.
    fs : Array of one integer
        This array contains the sampling frequency (Hz) used when collecting this
        sample, meaning the number of samples taken per second.
    label_samples : Array of integers
        This is a 1-dimensional array contains the samples at which normal or abnormal heart beats
        occur. This array is directly related to the label_symbols array.
    label_symbols : Array of strings
        This is a 1-dimensional array contains strings 'N' and 'V' indicating normal and 
        premature ventricular contractions.
    subject_id : Array containing one string
        This array contains a string that is the ID of the subject whose 
        heart beat was taken in this sample.
    electrode : Array containing one string
        This array contains a string that specifies the type of electrode used.
    units : Array containing one string
        This array contains a string that indicates the unit of this data, mV.

    """
    
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

def plot_raw_data(signal_voltage, signal_time, units="mV", title=""):
    """
    This function creates figure 1, then plots signal volatage (mV) against 
    signal time. Lastly, it annotates the plot, adding axis labels and a title.

    Parameters
    ----------
    signal_voltage : Array of floats
        A one-dimensional array containing all voltages recorded in the trial,
        measured in mV.
    signal_time : Array of integers
        This is a one dimensional array containing the times of each recording,
        found by accounting for sampling frequency.
    units : string, optional
        The units recorded when measuring voltage. The default is "mV".
    title : string, optional
        This is the title of the plot. The default is "".

    Returns
    -------
    None.

    """
    
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
    """
    This function updates plot 1, plotting the locations of symbols, provided
    by label_samples and indicates whether the heart beat is abnormal through
    marker color, using the label argument. A legend is then created to
    explain the marker color.

    Parameters
    ----------
    label_samples : Array of floats
        This is a 1-dimensional array contains the samples at which a certain type of heart beat
        occurs. This array is directly related to the label_symbols array.
    label_symbols : Array of strings
        This is a 1-dimensional array contains strings 'N' and 'V' indicating normal and 
        premature ventricular contractions.
    signal_time : Array of floats
        This is a one dimensional array containing the times of each recordings.
    signal_voltage : Array of floats
        A one-dimensional array containing voltages recorded in the specific trial,
        measured in mV.

    Returns
    -------
    None.

    """
    
    #plot dots for each event in the signal on the same plot done in plot_raw_data()
    plt.figure(1)
    plt.plot(signal_time, signal_voltage, label=f"{label_symbols} Events", linestyle="", marker="o")

    #add a legend
    plt.legend(loc=4) #4 corresponds to correct location
    
def extract_trials(signal_voltage, trial_start_samples, trial_sample_count):
    """
    This function extracts trials from the overall signal, each trial containing
    one heart beat. It also sets the first and last recorded portions of a heart
    beat to nan so the values do not interfere with further analysis. The
    function then returns the trials.

    Parameters
    ----------
    signal_voltage : Array of floats
        A one-dimensional array containing voltages recorded,
        measured in mV.
    trial_start_samples : Array of integers
        A 1-D array containing indices of the start of each trial in the
        voltage array.
    trial_sample_count : int
        The number of samples to extract in each trial.

    Returns
    -------
    trials : Array of floats
        An array containing one trial per row and the recorded voltages in
        the columns. The first and last rows are filled with nan values,
        as explained above

    """
    
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
    """
    This function acts as a wrapper function, that effectively exctracts trials
    from the full sample. It then determines the mean values across every
    trial of the same type. It also determines the standard deviation of all
    signal readings at every time value. Next, the function creates a graph containing
    the mean signal of normal and abnormal heart beats, creating error bars
    around each of these signals. The function returns symbols, times, and mean
    trial signal.

    Parameters
    ----------
    signal_voltage : Array of floats
        A one-dimensional array containing voltages recorded,
        measured in mV.
    label_samples : Array of integers
        This is a 1-dimensional array contains the samples at which a certain type of heart beat
        occurs. This array is directly related to the label_symbols array.
    label_symbols : Array of strings
        This is a 1-dimensional array contains strings 'N' and 'V' indicating normal and 
        premature ventricular contractions.
    trial_duration_seconds : int
        This is the duration of one trial.
    fs : Array containing one integer
        This array contains the sampling frequency (Hz) used when collecting this
        sample, meaning the number of samples taken per second.
    units : Array containing one string
        This array contains a string that indicates the unit of this data, mV.
    title : string
        This is the title of the graph created.

    Returns
    -------
    symbols : Array of strings
        A 1-D array containing the two types of symbols used to classify heartbeats
    trial_time : Array of floats
        A 1-D Array containing all the time points used in every sample.
    mean_trial_signal : Array of floats
        This is an array containing the means at each time point in across every
        trial. The rows are the two types of heart beats "N" and "V" and the columns
        are the mean voltages (mV)

    """
    
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
        plt.ylabel("Voltage (mV)")
        
    plt.legend()
    
    return symbols, trial_time, mean_trial_signal

def save_means(symbols, trial_time, mean_trial_signal, out_filename = 'ecg_means.npz'):
    """
    This function saves the means trial signal, along with the symbols and time
    points that correspond with the signal, all into a .npz file.

    Parameters
    ----------
    symbols : Array of strings
        A 1-D array containing the two types of symbols used to classify heartbeats
    trial_time : Array of floats
        A 1-D Array containing all the time points used in every sample.
    mean_trial_signal : Array of floats
        This is an array containing the means at each time point in across every
        trial. The rows are the two types of heart beats "N" and "V" and the columns
        are the mean voltages (mV)
    out_filename : string, optional
        This is the name of the output file, in which data will be saved.
        The default is 'ecg_means.npz'.

    Returns
    -------
    None.

    """
    
    np.savez(out_filename, symbols, trial_time, mean_trial_signal)
    return
    
    
    
    
    
    
    
    
    
