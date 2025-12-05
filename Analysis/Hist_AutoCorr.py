# -*- coding: utf-8 -*-
"""
@author: Ananth

Extracts and analyzes data for single simulation

This code extracts .pkl file

This code calculates the spike time histograms and wavelet scalograms corresponding to that.

Using the Histograms, the auto-correlation is also calculated
"""
import numpy as np
from funcsAux import *
import matplotlib.pyplot as plt
import glob, os
from netpyne.analysis.tools import loadData
from itertools import compress
import matplotlib.gridspec as gridspec
from scipy.signal import correlate # NEW IMPORT for ACF

# --- ORIGINAL PARAMETERS ---
gsin = 5
f = 8
dt_rec = 1e-2 # Down sample the rates
minFreq=30.
maxFreq=350.
maxPower= 700 # 100. # Sets the maximum for the scalogram. Varies according to the power of the signal. Change it for better visualization
colorbar=True
numBins = 2*125+1
###################################
fs = np.arange(minFreq,maxFreq,3.)
levelsWav = np.linspace(0., maxPower, 20, endpoint=True)

FileID = '1118_NoII/' # RESTORED ORIGINAL FILEID FOR HISTOGRAMS
if not os.path.exists(FileID):
    os.makedirs(FileID)

i = 0
spktFSAux = {}
spktSCAux = {}

# Analysis constants based on the histogram's effective binning:
THETA_PERIOD_MS = 1.0 / f * 1000 # 125.0 ms
THETA_CYCLE_INTERVALS = 125 # Intervals in one theta cycle (250 intervals / 2 cycles)
NUM_CYCLES_TO_AVERAGE = 2
DT_HIST_EFFECTIVE = (250.0 / (numBins - 1)) / 1000.0 # Effective 1 ms (1e-3 s) bin width

# --- ACF FUNCTION (NEW) ---
def calculate_and_average_acf(hist_array, num_cycles, cycle_intervals):
    """Calculates and averages the ACF for 2 segments (cycles)."""
    
    # Use the first 250 points, which represent the 250 intervals (2*125)
    hist_array = hist_array[:num_cycles * cycle_intervals]
         
    # Segment 1 (Cycle 1)
    segment1 = hist_array[0:cycle_intervals]
    acf1 = correlate(segment1, segment1, mode='full')
    
    # Segment 2 (Cycle 2)
    segment2 = hist_array[cycle_intervals:2*cycle_intervals]
    acf2 = correlate(segment2, segment2, mode='full')

    # Normalize ACFs by their zero lag
    zero_lag_index = cycle_intervals - 1
    if acf1[zero_lag_index] > 1e-9: acf1 = acf1 / acf1[zero_lag_index]
    if acf2[zero_lag_index] > 1e-9: acf2 = acf2 / acf2[zero_lag_index]

    # Average the two normalized ACFs
    avg_acf = (acf1 + acf2) / 2.0
    return avg_acf

# --- YOUR ORIGINAL LOOP STARTS HERE (UNTIL END OF WAVELET PLOTTING) ---
print("Starting analysis and histogram plotting...")

for file in glob.glob("../output/*.pkl"):#Mention the exact file that needs to be analyzed
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][13:]
    print(fileName)
    #base_name = os.path.basename(file)
    #current_fileName = os.path.splitext(base_name)[0]
    #fileName2 = current_fileName # Use the full, current filename for saving
    sim_time = fileInfo['simConfig']['duration']
    maskFS = np.array(fileInfo['simData']['spkid'])< 100
    spktFSAux['0'] = np.array( list( compress(fileInfo['simData']['spkt'], maskFS) ) )
    maskSC = np.array(fileInfo['simData']['spkid'])>= 100
    tSim = fileInfo['simData']['t']
    spktSCAux['0'] = np.array( list( compress(fileInfo['simData']['spkt'], maskSC) ) )
    
    spktFS = spktFSAux['0']
    spktSC = spktSCAux['0']

    # plot it
    fig = plt.figure(figsize=(10, 8))
    outer = gridspec.GridSpec(1, 2, wspace=0.3, hspace=0.1)

    inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer[0], wspace=0.1, hspace=0.1, height_ratios=[1,4,4])
    
    ax0 = plt.Subplot(fig, inner[0])
    t = np.linspace(sim_time-2.*125.,sim_time,2*125+1)
    ax0.plot(t, gsin*np.sin(2*np.pi*f*t*1e-3-np.pi/2),color = 'k')
    ax0.set_xlim(sim_time-2.*125.,sim_time)
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.set_xticks([])
    ax0.set_yticks([])
    fig.add_subplot(ax0)
    
    ax1 = plt.Subplot(fig, inner[1])
    histFS, foo1, foo = ax1.hist(spktFS, np.linspace(sim_time-2.*125.,sim_time, numBins),color = 'k', label='FS.')
    ax1.set_xlim(sim_time-2.*125.,sim_time); tmp = ax1.set_ylim(0.,60.)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(True)
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    ax1.set_ylabel('Counts')
    ax1.legend(loc='upper right')
    fig.add_subplot(ax1)

    ax2 = plt.Subplot(fig, inner[2])
    histSC, foo, foo = ax2.hist(spktSC, np.linspace(sim_time-2.*125.,sim_time, numBins), color = 'k', label='SC.')
    ax2.set_xlim(sim_time-2.*125.,sim_time); tmp = ax2.set_ylim(0.,60.)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(True)
    ax2.set_ylabel('Counts')
    ax2.set_xticks([])
    ax2.set_xticklabels([])
    ax2.legend(loc='upper right')
    fig.add_subplot(ax2)

    # WAVELET PLOTS
    inner1 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=outer[1], wspace=0.3, hspace=0.1)

    ax4 = plt.Subplot(fig, inner1[0])
    cwtPowFS, cwtPhaseFS = compPWT(histFS,1e-3,fs=fs)

    maxPowerFS = np.max(np.max(cwtPowFS))
    # print('Maximum Power in the FS case',maxPowerFS) # Removed internal print
    # Find the indices of the maximum power
    max_power_indexFS = np.unravel_index(np.argmax(cwtPowFS), cwtPowFS.shape)
    max_freq_indexFS, max_time_indexFS = max_power_indexFS
    # Get the frequency and time at the maximum power
    max_freqFS = fs[max_freq_indexFS]
    # print(f"Maximum power for FS firing occurs at frequency: {max_freqFS} Hz") # Removed internal print

    plotPow(cwtPowFS,dt=1e-3,fs=fs,levels=levelsWav, cmap="hot", ax=ax4, fig=fig, colorbar=colorbar)
    #plotPow(cwtPowFS,dt=dt_rec,fs=fs, cmap="hot", ax=ax3, fig=fig, colorbar=colorbar)
    ax4.set_xticks([]) 
    ax4.set_ylabel("Freq (Hz)")
    fig.add_subplot(ax4)

    ax5 = plt.Subplot(fig, inner1[1])
    cwtPowSC, cwtPhaseSC = compPWT(histSC,1e-3,fs=fs)

    maxPowerSC = np.max(np.max(cwtPowSC))
    # print('Maximum Power in the SC case',maxPowerSC) # Removed internal print
    # Find the indices of the maximum power
    max_power_indexSC = np.unravel_index(np.argmax(cwtPowSC), cwtPowSC.shape)
    max_freq_indexSC, max_time_indexSC = max_power_indexSC
    # Get the frequency and time at the maximum power
    max_freqSC = fs[max_freq_indexSC]
    # print(f"Maximum power for SC firing occurs at frequency: {max_freqSC} Hz") # Removed internal print
    plotPow(cwtPowSC,dt=1e-3,fs=fs,levels=levelsWav, cmap="hot", ax=ax5, fig=fig, colorbar=colorbar)
    #plotPow(cwtPowSC,dt=dt_rec,fs=fs, cmap="hot", ax=ax4, fig=fig, colorbar=colorbar)
    ax5.set_xticks([]) 
    ax5.set_ylabel("Freq (Hz)")    	
    fig.add_subplot(ax5)


    fig.tight_layout()
    # SAVING HISTOGRAMS + WAVELETS TO ORIGINAL FOLDER (1104_Hist/)
    fig.savefig(FileID+fileName+'_Hist.png', bbox_inches='tight')
    fig.savefig(FileID+fileName+'_Hist.eps', bbox_inches='tight')
    #fig.savefig(fileID+'.svg', bbox_inches='tight')
    plt.close(fig) # CLOSE ORIGINAL FIGURE

    # ----------------------------------------------------------------------
    # --- NEW, ISOLATED ACF ANALYSIS AND PLOTTING ---
    # ----------------------------------------------------------------------
    
    try:
        avg_acfFS = calculate_and_average_acf(histFS, NUM_CYCLES_TO_AVERAGE, THETA_CYCLE_INTERVALS)
        avg_acfSC = calculate_and_average_acf(histSC, NUM_CYCLES_TO_AVERAGE, THETA_CYCLE_INTERVALS)
    except Exception as e:
        print(f"Error during ACF calculation for {fileName}: {e}. Skipping ACF plot.")
        continue
    
    # --- ACF PLOTTING ---
    fig_acf, (axFS, axSC) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    
    # Time lag axis for plotting (from -125 ms to +125 ms)
    max_lag_s = (THETA_CYCLE_INTERVALS - 1) * DT_HIST_EFFECTIVE
    time_lags_ms = np.linspace(-max_lag_s * 1000, 
                                max_lag_s * 1000, 
                                len(avg_acfFS))

    # Plot FS ACF
    axFS.plot(time_lags_ms, avg_acfFS, color='darkblue')
    axFS.set_title(f'{fileName}: FS Population Averaged ACF (2 Cycles)')
    axFS.set_ylabel('Normalized ACF')
    #axFS.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    #axFS.axvline(THETA_PERIOD_MS, color='red', linestyle=':', linewidth=1.0)
    #axFS.axvline(-THETA_PERIOD_MS, color='red', linestyle=':', linewidth=1.0)
    #axFS.grid(True, alpha=0.4)
    axFS.set_xlim(time_lags_ms[0], time_lags_ms[-1])
    
    # Plot SC ACF
    axSC.plot(time_lags_ms, avg_acfSC, color='darkgreen')
    axSC.set_title(f'{fileName}: SC Population Averaged ACF (2 Cycles)')
    axSC.set_xlabel('Time Lag (ms)')
    axSC.set_ylabel('Normalized ACF')
    #axSC.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    #axSC.axvline(THETA_PERIOD_MS, color='red', linestyle=':', linewidth=1.0)
    #axSC.axvline(-THETA_PERIOD_MS, color='red', linestyle=':', linewidth=1.0)
    #axSC.grid(True, alpha=0.4)
    axSC.set_xlim(time_lags_ms[0], time_lags_ms[-1])

    # Save the ACF figure to the NEW folder (1107_ACF/)
    #save_name_acf = os.path.join(FileID, f'{fileName}_AvgACF.eps')
    fig_acf.tight_layout()
    fig_acf.savefig(FileID+fileName+'_ACF_Hist.png', bbox_inches='tight')
    fig_acf.savefig(FileID+fileName+'_ACF_Hist.eps', bbox_inches='tight')
    plt.close(fig_acf)
    #print(f"Saved Averaged ACF plot to: {save_name_acf}")
# END OF MAIN LOOP

print("\nAll analysis complete.")


#########################################################################################################################################


