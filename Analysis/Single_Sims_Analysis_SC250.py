# -*- coding: utf-8 -*-
"""
@author: Ananth

Extracts and analyzes data for single simulation for the clamped SC250

This code extracts .pkl file

This code calculates the IPSC currents based on voltage fluctuations calculated from netpyne simulations from SC 250.

It gives the IPSC waveforms and the correspondings scalogram
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

# Import simulation and plot code to create & visualize data
from neurodsp.plts import plot_timefrequency

# Import function for Morlet Wavelets
from neurodsp.timefrequency.wavelets import compute_wavelet_transform

#########################################################################################################################################

#Some Housekeeping parameters
dt = 1e-2 # in ms
fTheta = 8
thetaPeriod = 1000/fTheta

#Firstly load the files

base_output_dir = 'Single_Sim_Plots/'

# Ensure the output directory exists
if not os.path.exists(base_output_dir):
    os.makedirs(base_output_dir)


cellTrace={}
VC = 0 #Clamped voltage
rs=1e-4
Factor = 1e3
for file in glob.glob("../output/Ant*EI_0.03*gsinInh7.0_gsinExc3.0*_II_0.5_GAP_T_*.pkl"):#Since this is a single simulation based plot, ensure that the file name matches whatever you want to extract
    print('Loading the file from specified folder')
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][13:]
    print(fileName)
    fileName = fileInfo['simConfig']['filename'][29:36]
    sim_time = fileInfo['simConfig']['duration']
    cellTrace['0'] = fileInfo['simData']['V_soma']['cell_250']#20
    tSim = fileInfo['simData']['t']

cellTr0 = np.array(cellTrace['0'])
FileID = base_output_dir+"PING" 

CapCurrentLeft = 70; CapCurrentRight = 80;
waveletPlotPoints = 0
y0 = (VC-cellTr0)/rs*Factor
y0 -= y0[-1] #offsetting based on zero
try:
    index = int(np.argwhere(y0<minV)[0])
except:
    index = CapCurrentLeft
#print('Printing legths of cellTr, tSim, and y0 : ',len(cellTr0),len(tSim),len(y0))

#########################################################################################################################################

b, a = signal.butter(3, [50, 300], fs=1/(dt*1e-3), btype='band')
rates = signal.filtfilt(b, a, y0) #Here is where we are using the band pass filter and using the signal to get gamma waveform
rates -= rates[-1] #again, offsetting based on zero
#print('Length of the assigned array is',np.shape(rates))

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

# n_cycles is the center frequency of the wavelet - w0
# It's also the length of the filter, as the number of cycles of the oscillation with specified frequency
# the analytic morlet wavelet in matlab uses w0 = 6

# Compute wavelet transform using compute Morlet wavelet transform algorithm
mwt_avg = []
for j in range(2,CycToPlot+2):
    #print('Value of j and starting point of the value is ',j,j*chunkLength, (j+1)*chunkLength)
    signal_1 = rates[(j)*chunkLength: (j+1)*chunkLength]
    #print('Length of Signal snd time array is given by ',len(signal_1), len(t))
    mwt = compute_wavelet_transform(signal_1, fs=fs, freqs=freqs, n_cycles = 6)
    mwt_avg.append(mwt)

band1_indices = np.where((freqs >= 50) & (freqs <= 100))[0]
band2_indices = np.where((freqs > 100) & (freqs <= 300))[0]
# the magnitude of the coefficients are amplitude of the sine wave, not peak to peak
# multiply by factor of 2 for peak to peak magnitude - same as matlab

factor = 2
mwt_avg = np.array(mwt_avg)
print('Shape of mwt_avg is', np.shape(mwt_avg))

mwt_avg = np.mean(mwt_avg,axis = 0)
z = np.abs(factor*mwt_avg)**2

maxPowerAvg = np.max(np.max(z))
print('Maximum power of this signal is ',maxPowerAvg)


# Plot morlet wavelet transform
plt.figure()
y_ticks = np.linspace(50,300,11)
plot_timefrequency(t, freqs, z, x_ticks=5, y_ticks=y_ticks)
plt.set_cmap('hot')
plt.savefig(FileID+fileName+"_Power.png", bbox_inches='tight')
#plt.show()



fig = plt.figure(figsize=(10, 8))
outer = gridspec.GridSpec(1, 1, wspace=0.3, hspace=0.1)

inner = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[0], wspace=0.1, hspace=0.1, height_ratios=[1,1,1])

ax0 = plt.Subplot(fig, inner[0])
ax0.plot(tSim, y0, 'r-',alpha = 1, label='Unfiltered')
ax0.set_xlim(sim_time-4.*125.,sim_time);
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(True)
ax0.set_ylabel("Current (pA)")
ax0.set_ylim([-100,1000])#This needs to be adjusted depending on the amplitude of the current
ax0.set_xticks([])
ax0.set_xticklabels([])
ax0.legend(loc='upper right')
fig.add_subplot(ax0)

gsin = 5

ax2 = plt.Subplot(fig, inner[1])
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
fig.savefig(FileID+fileName+'_Currents.png', bbox_inches='tight')
fig.savefig(FileID+fileName+'_Currents.eps', bbox_inches='tight')
plt.clf();

#maxPowerAvg = 2000 #Uncomment this line if you want to scale the powerbar uniformly instead of themaximum that is generated
plt.figure()
plotPow(z,Ncycs=1,dt=dt_rec,fs=freqs,levels=np.linspace(0.,maxPowerAvg,150,endpoint=True))
#plt.ylabel("Gamma Frequency (Hz)")
#plt.xlabel("Stim Theta Phase (rad)")
#plt.rcParams['font.family'] = 'Arial'  # Use LaTeX for text rendering
#plt.rcParams['ps.usedistiller'] = 'xpdf' # or 'ghostscript'
plt.savefig(FileID+fileName+'_Pow.eps')
plt.savefig(FileID+fileName+'_Pow.png')
#plt.rcParams['text.usetex'] = False #return to default.
#plt.rcParams['ps.usedistiller'] = None #return to default.


#########################################################################################################################################


