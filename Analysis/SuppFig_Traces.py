import numpy as np
#from funcsAux import *
import matplotlib.pyplot as plt
import glob, os
from netpyne.analysis.tools import loadData
from itertools import compress
import matplotlib.gridspec as gridspec
gsin = 5
f = 8
dt_rec = 1e-2 # Down sample the rates
#minFreq=30.
#maxFreq=350.
#maxPower= 500 # 100. # Sets the maximum for the scalogram. Varies according to the power of the signal. Change it for better visualization
#colorbar=True
#numBins = 2*125+1
###################################
#fs = np.arange(minFreq,maxFreq,3.)
#levelsWav = np.linspace(0., maxPower, 20, endpoint=True)

i = 0
spktFSAux = {}
spktSCAux = {}
FScellTrace={}
SCcellTrace={}

fileID = 'Traces/'
if not os.path.exists(fileID):
    os.makedirs(fileID)


for file in glob.glob("../Data_Single_Sims/More_Inhib_0_data.pkl"):
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][8:]
    print(fileName)
    sim_time = fileInfo['simConfig']['duration']
    FScellTrace['0'] = fileInfo['simData']['V_soma']['cell_35']
    FScellTrace['1'] = fileInfo['simData']['V_soma']['cell_55']
    #maskFS = np.array(fileInfo['simData']['spkid'])< 100
    #spktFSAux['0'] = np.array( list( compress(fileInfo['simData']['spkt'], maskFS) ) )
    tSim = fileInfo['simData']['t']
    i += 1

#spktFS0 = spktFSAux['0']
cellTrFS0 = FScellTrace['0']
cellTrFS1 = FScellTrace['1']

for file in glob.glob("../Data_Single_Sims/More_Inhib_2_data.pkl"):
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][8:]
    print(fileName)
    sim_time = fileInfo['simConfig']['duration']
    FScellTrace['2'] = fileInfo['simData']['V_soma']['cell_35']
    FScellTrace['3'] = fileInfo['simData']['V_soma']['cell_55']
    #maskFS = np.array(fileInfo['simData']['spkid'])< 100
    #spktFSAux['0'] = np.array( list( compress(fileInfo['simData']['spkt'], maskFS) ) )
    i += 1

#spktFS0 = spktFSAux['0']
cellTrFS2 = FScellTrace['2']
cellTrFS3 = FScellTrace['3']

for file in glob.glob("../Data_Single_Sims/Ant*gsinInh4.0*gsinExc3.0*Hyper*_Noise_T*.pkl"):
    fileInfo = loadData(file)
    fileName = fileInfo['simConfig']['filename'][8:]
    print(fileName)
    sim_time = fileInfo['simConfig']['duration']
    FScellTrace['4'] = fileInfo['simData']['V_soma']['cell_35']
    FScellTrace['5'] = fileInfo['simData']['V_soma']['cell_55']
    #maskFS = np.array(fileInfo['simData']['spkid'])< 100
    #spktFSAux['0'] = np.array( list( compress(fileInfo['simData']['spkt'], maskFS) ) )
    i += 1

#spktFS0 = spktFSAux['0']
cellTrFS4 = FScellTrace['4']
cellTrFS5 = FScellTrace['5']




fig = plt.figure(figsize=(10, 8))
outer = gridspec.GridSpec(1, 2, wspace=0.3, hspace=0.1)

inner = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=outer[0], wspace=0.1, hspace=0.1, height_ratios=[1,4,4,4])


ax0 = plt.Subplot(fig, inner[0])
t = np.linspace(sim_time-4.*125.,sim_time,2*125+1)
ax0.plot(t, gsin*np.sin(2*np.pi*f*t*1e-3-np.pi/2),color = 'k')
ax0.set_xlim(sim_time-4.*125.,sim_time)
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.set_xticks([])
ax0.set_yticks([])
fig.add_subplot(ax0)

ax1 = plt.Subplot(fig, inner[1], label='FS - Stimulate only FS')
y = cellTrFS0
ax1.plot(tSim, y, 'b-', label='FS - Stimulate only FS')
ax1.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax1)

ax2 = plt.Subplot(fig, inner[2], label='FS - Stimulate FS and SC')
y = cellTrFS2
ax2.plot(tSim, y, 'b-', label='FS - Stimulate FS and SC')
ax2.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax2)

ax3 = plt.Subplot(fig, inner[3], label='SC - Stimulate FS and SC')
y = cellTrFS4
ax3.plot(tSim, y, 'b-', label='SC - Stimulate FS and SC')
ax3.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax3)

inner = gridspec.GridSpecFromSubplotSpec(4, 1, subplot_spec=outer[1], wspace=0.1, hspace=0.1, height_ratios=[1,4,4,4])

ax0 = plt.Subplot(fig, inner[0])
t = np.linspace(sim_time-4.*125.,sim_time,2*125+1)
ax0.plot(t, gsin*np.sin(2*np.pi*f*t*1e-3-np.pi/2),color = 'k')
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.set_xlim(sim_time-4.*125.,sim_time)
ax0.set_xticks([])
ax0.set_yticks([])
fig.add_subplot(ax0)

ax1 = plt.Subplot(fig, inner[1])
y = cellTrFS1
ax1.plot(tSim, y, 'b-', label='FS - Stimulate only FS')
ax1.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax1)


ax2 = plt.Subplot(fig, inner[2])
y = cellTrFS3
ax2.plot(tSim, y, 'b-', label='FS - Stimulate FS and SC')
ax2.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax2)


ax3 = plt.Subplot(fig, inner[3])
y = cellTrFS5
ax3.plot(tSim, y, 'b-', label='SC - Stimulate FS and SC')
ax3.set_xlim(sim_time-4.*125.,sim_time)
fig.add_subplot(ax3)

fig.tight_layout()
#fileName = '0110_Plots/FS_gsin5nS_gsinEx2nS_Hyper_Traces'
fig.savefig(fileID+'Traces_2.png', bbox_inches='tight',dpi = 300)
fig.savefig(fileID+'Traces_2.eps', bbox_inches='tight', dpi = 300)
#fig.savefig(fileID+'.svg', bbox_inches='tight')

