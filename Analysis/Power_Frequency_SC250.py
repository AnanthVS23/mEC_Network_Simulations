# -*- coding: utf-8 -*-
"""
@author: Ananth

Trying to automate and run for all simulations for the clamped SC250

This code extracts .pkl files for all batch simulations, or even 1 or 2 but is based on the filenames, so accordingly it needs to be modified 

This code calculates the IPSC currents based on voltage fluctuations calculated from netpyne simulations from SC 250.

It tabulates and saves for each seed.
"""
import matplotlib.pyplot as plt
from funcs import *
import glob, os
from netpyne.analysis.tools import loadData
from itertools import compress
import matplotlib.gridspec as gridspec
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from funcs import *
# Import simulation and plot code to create & visualize data
from neurodsp.plts import plot_timefrequency

# Import function for Morlet Wavelets
from neurodsp.timefrequency.wavelets import compute_wavelet_transform

def get_value(data_array):
    """
    Extracts the last two elements of an array and converts them to an integer.
    Handles cases where the second-to-last element is not a number ('_').
    """
    if not data_array:
        return None  # Handle empty array case

    last_digit = str(data_array[-1]) #Represents conductance
    first_digit = str(data_array[-3]) #Represents seed
    combined_str = first_digit +'.'+ last_digit
    return(float(combined_str))

#########################################################################################################################################

#Some Housekeeping parameters
dt = 1e-2 # in ms
fTheta = 8
thetaPeriod = 1000/fTheta

#Firstly load the files

cellTrace={}
VC = 0 #Clamped voltage
rs=1e-4
Factor = 1e3

CapCurrentLeft = 70; CapCurrentRight = 80;
b, a = signal.butter(3, [50, 300], fs=1/(dt*1e-3), btype='band')
waveletPlotPoints = 0

base_output_dir = 'Results/'

# Ensure the output directory exists
if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)

FileID = "Results/SC250_" #Output folder

dt_rec = dt; # Down sample the rates (in ms)

#freqss = np.arange(50.,300.1,0.2);

chunkLength = int(np.round(thetaPeriod/dt_rec));

#print('Chunklength value and shape is ',chunkLength, np.shape(chunkLength))

CycToPlot = 8

# Generate a test sinusoidal signal
fs = 1/(dt*1e-3)  # Sampling frequency in Hz
t = np.linspace(0, 125, chunkLength)  # Time vector from 0 to 1 second
#t = np.linspace(sim_time-11.*125.,sim_time,4*125+1)

#freq = 50  # Frequency of the test sinusoid in Hz
#signal = np.sin(2 * np.pi * freq * t)  # Sinusoidal signal

freqs = np.arange(50., 301, 1)
Power_Array = []

for file in glob.glob("../output/Varying_Seeds/*_data.pkl"):#This could change based on the output folder, needs to be consistent of where the data from netpyne simulations have been saved
    print('Loading the file from specified folder')
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][40:]
    print(fileName)
    fileName2 = fileInfo['simConfig']['filename'][-3:]
    weight_index = get_value(fileName2)
    print(fileName2,weight_index)
    #j = int(fileName[])
    sim_time = fileInfo['simConfig']['duration']
    cellTrace['0'] = fileInfo['simData']['V_soma']['cell_250']#This cell ID can be changed to any other clamped cell - see cfg.py to know which other cells have been clamped
    tSim = fileInfo['simData']['t']
    #weight_index = float(fileInfo['simConfig']['filename'][-2:])
    
    cellTr0 = np.array(cellTrace['0'])

    y0 = (VC-cellTr0)/rs*Factor
    y0 -= y0[-1] #offsetting based on zero
    try:
        index = int(np.argwhere(y0<minV)[0])
    except:
        index = CapCurrentLeft
    #print('Printing legths of cellTr, tSim, and y0 : ',len(cellTr0),len(tSim),len(y0))
    rates = signal.filtfilt(b, a, y0) #Here is where we are using the band pass filter and using the signal to get gamma waveform
    rates -= rates[-1]

    # n_cycles is the center frequency of the wavelet - w0
    # It's also the length of the filter, as the number of cycles of the oscillation with specified frequency
    # the analytic morlet wavelet in matlab uses w0 = 6

    # Compute wavelet transform using compute Morlet wavelet transform algorithm
    mwt_avg = []
    for j in range(2,CycToPlot+2):
        signal_1 = rates[(j)*chunkLength: (j+1)*chunkLength]
        mwt = compute_wavelet_transform(signal_1, fs=fs, freqs=freqs, n_cycles = 6)
        mwt_avg.append(mwt)

    factor = 2
    mwt_avg = np.array(mwt_avg)
    #print('Shape of mwt_avg is', np.shape(mwt_avg))

    mwt_avg = np.mean(mwt_avg,axis = 0)
    z = np.abs(factor*mwt_avg)**2
   
    maxPowerAvg = np.max(np.max(z))
    print('Maximum power of this signal is ',maxPowerAvg)

    # Find the frequency of peak power in each band
    max_power_index = np.argmax(np.max(z, axis=1))

    freq_at_peak_power = freqs[max_power_index]
    print('Frequency at maximum power of this signal is ',freqs[max_power_index])

    Power_Array.append([weight_index,maxPowerAvg,freq_at_peak_power])
    print(Power_Array)

    
    plt.figure()
    plotPow(z,Ncycs=1,dt=dt_rec,fs=freqs,levels=np.linspace(0.,maxPowerAvg,150,endpoint=True))
    plt.savefig(FileID+fileName2+'_Pow.eps')
    plt.savefig(FileID+fileName2+'_Pow.png')
    #plt.savefig(FileID+fileName2+'_Pow.svg')

########Plot the current figures only if the number of files to be analyzed are less than 5, otherwise use specific individual plot routine, otherwise it would overload the system.

    fig = plt.figure(figsize=(10, 8))
    outer = gridspec.GridSpec(1, 1, wspace=0.3, hspace=0.1)
    inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer[0], wspace=0.1, hspace=0.1, height_ratios=[1,1,1])

    ax0 = plt.Subplot(fig, inner[0])
    ax0.plot(tSim, y0, 'r-',alpha = 1, label='Unfiltered')
    ax0.set_xlim(sim_time-4.*125.,sim_time);
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['left'].set_visible(True)
    ax0.set_ylabel("Current (pA)")
    #ax0.set_ylim(1.2*min(y0[-1000:-1]),1.2*max(y0[-1000:-1]))
    ax0.set_ylim([-100,600])
    ax0.set_xticks([])
    ax0.set_xticklabels([])
    ax0.legend(loc='upper right')
    fig.add_subplot(ax0)

    ax1 = plt.Subplot(fig, inner[1])
    ax1.plot(tSim, rates, 'b-',label='Filtered 50-300 hz')
    ax1.set_xlim(sim_time-4.*125.,sim_time);
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(True)
    ax1.set_ylabel("Current (pA)")
    #ax1.set_ylim(1.2*min(y1[-1000:-1]),1.2*max(y1[-1000:-1]))
    ax1.set_ylim([-250,250])
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    ax1.legend(loc='upper right')
    fig.add_subplot(ax1)

    gsin = 5

    ax2 = plt.Subplot(fig, inner[2])
    t1 = np.linspace(sim_time-4.*125.,sim_time,4*125+1)
    ax2.set_xlim(sim_time-4.*125.,sim_time)
    ax2.plot(t1, gsin*np.sin(2*np.pi*fTheta*t1*1e-3-np.pi/2),color = 'k')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.set_xticks([])
    ax2.set_yticks([])
    fig.add_subplot(ax2)

    fig.tight_layout()
    fig.savefig(FileID+fileName2+'_Currents.png', bbox_inches='tight')
    fig.savefig(FileID+fileName2+'_Currents.eps', bbox_inches='tight')
    plt.clf();

power_array = np.array(Power_Array)
print(np.shape(power_array))
power_array = power_array[power_array[:, 0].argsort()]
print(power_array)
np.savetxt(FileID+'Power_Data2.txt', power_array, fmt="%f", delimiter=",")
np.savetxt(FileID+'Power_Data2.csv', power_array, fmt="%f", delimiter=",")




