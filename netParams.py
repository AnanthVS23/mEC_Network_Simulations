from SetupModels.CreateNetworkParameters import *
import numpy as np
from numpy import exp, log, pi
#from neuron import gui #this line is absolutely necessary if importing cells from hoc templates
#from neuron import h
from netpyne import specs
import scipy.stats as stats
#h.load_file("stdrun.hoc")
#from cfg import gmsScale, ggsScale, g_sin, g_sinExc, fsin, GAP, WODepression, Esyn_inh, N, HOMOGENEOUS, NumModels, FactorKv3, FactorKv7, FactorTau, ChemycalConnProb, GapJunctProb, OPTODRIVE, NOISE, ConnProbIE, ConnProbEI, MeanENoise, MeanINoise, StdENoise, StdINoise, Clamp, Vclamp, ClampCells 
try:
    from __main__ import cfg
except:
    from cfg import cfg

# Network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters
netParams.defaultDelay = 0 #This is because it creates gap junctions with defaultDelay = 1 ms if not 
netParams.defaultThreshold = -30.0
###############################################################################
## Create and load parameters for the neurons and simulations
###############################################################################
gLs, ELs, CapsOrig, ConductWithGapJunct, ReversPotWithGapJunct, CapsMod, gNas, gKv3s, gKv7s, thm1s, thh2s, thn1s, tha1s, SharedParams, syns, delays, gms, synsgj, ggs = NetworkParams(NumNeurons=cfg.N, FactorTau=cfg.FactorTau, FactorKv3=cfg.FactorKv3, FactorKv7=cfg.FactorKv7, GapJunctProb=cfg.GapJunctProb, ChemycalConnProb=cfg.ChemycalConnProb, delaymin=.6, delaymax=1., meangms=0., sigmagms=1.,homogeneous=cfg.HOMOGENEOUS, randomseed = cfg.seeds['Inet'])
#To get a length from net capacitence most literature assumes neurons have 1uf/cm^2. This capacitence is in nF
SAOrig=CapsOrig*1e-3
SAGapJunct=CapsMod*1e-3
#neuron does length in um so lets make it um^2
SAumOrig=SAOrig*1e8
SAumGapJunct=SAGapJunct*1e8
#we're going to assume a diameter of 20um to get a radius of 10um
#SA of a cyclinder(not including ends)=2*pi*r*L
lengthsOrig=SAumOrig/(20*np.pi)
lengthsGapJunct=SAumGapJunct/(20*np.pi)
# Active conductances
# Heterogeneous peak conductances for active currents. This gave me nanosiemens. I need siemens/cm^2 for it's conductance, so I need to multiple by e-9 to get nanosiemens then divide by the surface area in cm^2
gLsSA = gLs*1e-9/SAOrig
ConductWithGapJunctSA = ConductWithGapJunct*1e-9/SAGapJunct
gNasSA = gNas*1e-9/SAOrig
gNasWithGapJunctSA = gNas*1e-9/SAGapJunct
gKv3sSA = gKv3s*1e-9/SAOrig
gKv3sWithGapJunctSA = gKv3s*1e-9/SAGapJunct
gKv7sSA = gKv7s*1e-9/SAOrig
gKv7sWithGapJunctSA = gKv7s*1e-9/SAGapJunct
###############################################################################
# NETWORK PARAMETERS
###############################################################################
# Population parameters
netParams.popParams['FS'] = {'cellType': 'FS', 'numCells': cfg.N, 'diversity': True} # add dict with params for this pop
netParams.popParams['SC'] = {'cellType': 'SC', 'numCells': 4*cfg.N} # add dict with params for this pop
#netParams.popParams['PYR'] = {'cellType': 'PYR', 'numCells': 1} 
###############################################################################
## Cell types
###############################################################################
# Fast Spiking PV+ Basket Cell from mEC

np.random.seed(42)  # Fixed seed
drives = np.random.normal(loc=cfg.g_sin, scale=0.1*cfg.g_sin, size=cfg.N)
print(cfg.g_sin,drives)

for k in range(cfg.NumModels):
    cellRule = {'conds': {'cellType': 'FS'}, 'diversityFraction': 1/cfg.NumModels , 'secs': {}}  # cell rule dict        
    if cfg.OPTODRIVE==False:
        cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}} 
    else:
        cellRule['secs']['soma'] = {'geom': {}, 'mechs': {}, 'pointps': {}}
        cellRule['secs']['soma']['pointps']['optodrive'] = {'mod' : 'optodrive', 'gsin': drives[k], 'Ese': 0 , 'f': cfg.fsin}
    if cfg.NOISE==True:
        cellRule['secs']['soma']['pointps']['InVivoNoise'] = {'mod' : 'Gfluct','g_e0': cfg.MeanENoise, 'g_i0': cfg.MeanINoise, 'std_e': cfg.StdENoise, 'std_i': cfg.StdINoise}
    if cfg.GAP==True:
        cellRule['secs']['soma']['geom'] = {'diam': 20, 'L': lengthsGapJunct[k], 'cm': 1}   # soma geometry
        cellRule['secs']['soma']['mechs']['pas'] = {'g': ConductWithGapJunctSA[k], 'e': ReversPotWithGapJunct[k]}
        cellRule['secs']['soma']['mechs']['naG'] = {'gbar': gNasWithGapJunctSA[k], 'thm1': thm1s[k], 'thh2': thh2s[k] }
        cellRule['secs']['soma']['mechs']['kv7'] = {'gbar': gKv7sWithGapJunctSA[k], 'tha1': tha1s[k], 'ka1': SharedParams[13], 'ka2':SharedParams[14] }
        cellRule['secs']['soma']['mechs']['kv3'] = {'gbar': gKv3sWithGapJunctSA[k], 'thn1': thn1s[k], 'kn1':SharedParams[10], 'kn2':SharedParams[11] }
    else:
        cellRule['secs']['soma']['geom'] = {'diam': 20, 'L': lengthsOrig[k], 'cm': 1}   # soma geometry
        cellRule['secs']['soma']['mechs']['pas'] = {'g': gLsSA[k], 'e': ELs[k]}
        cellRule['secs']['soma']['mechs']['naG'] = {'gbar': gNasSA[k], 'thm1': thm1s[k], 'thh2': thh2s[k] }
        cellRule['secs']['soma']['mechs']['kv7'] = {'gbar': gKv7sSA[k], 'tha1': tha1s[k], 'ka1': SharedParams[13],'ka2':SharedParams[14]}
        cellRule['secs']['soma']['mechs']['kv3'] = {'gbar': gKv3sSA[k], 'thn1': thn1s[k], 'kn1':SharedParams[10], 'kn2':SharedParams[11] }    
    cellRule['secs']['soma']['vinit'] = np.random.uniform(-75,-65) # set initial membrane potential
    netParams.cellParams['FS'+str(k)+'rule'] = cellRule


# Stellate Cell from mEC (Modified Hodgkin Huxley)
SCcell = {'secs': {}}
if cfg.OPTODRIVE==False:
    SCcell['secs']['soma'] = {'geom': {}, 'mechs': {}} 
else:
    SCcell['secs']['soma'] = {'geom': {}, 'mechs': {}, 'pointps': {}}
    SCcell['secs']['soma']['pointps']['optodrive'] = {'mod' : 'optodrive', 'gsin': cfg.g_sinExc, 'Ese': 0, 'f': cfg.fsin }
if cfg.NOISE==True:
    SCcell['secs']['soma']['pointps']['InVivoNoise'] = {'mod' : 'Gfluct', 'g_e0': cfg.MeanENoise, 'g_i0': cfg.MeanINoise, 'std_e': cfg.StdENoise, 'std_i': cfg.StdINoise}
SCcell['secs']['soma']['geom'] = {'diam': 18.2, 'L': 18.2, 'Ra': 150, 'cm':1}                           # soma geometry
#SCcell['secs']['soma']['mechs']['hh'] = {'gnabar': '0.12*uniform(1,5e-4)', 'gkbar': '0.036*uniform(1,1e-4)', 'gl': '0.0000357*uniform(1.2,1e-3)', 'el': -72} 
#SCcell['secs']['soma']['mechs']['hh'] = {'gnabar': '0.12*normal(1,7e-2)', 'gkbar': '0.036*normal(1,7e-2)', 'gl': '0.0000357*normal(1.2,2e-1)', 'el': '-68*normal(1,2e-1)'} # soma hh mechanism
SCcell['secs']['soma']['mechs']['hh'] = {'gnabar': '0.12*normal(1,3e-2)', 'gkbar': '0.036*normal(1,3e-2)', 'gl': '0.0000357*normal(1.2,1e-1)', 'el': -68}  
#SCcell['secs']['soma']['mechs']['hh'] = {'gnabar': '0.12*uniform(1,7e-2)', 'gkbar': '0.036*uniform(1,7e-2)', 'gl': '0.0000357*uniform(1.2,1e-1)', 'el': '-68*uniform(1,2e-1)'}
SCcell['secs']['soma']['vinit'] = np.random.uniform(-65,-58) # set initial membrane potential
netParams.cellParams['SC'] = SCcell

###############################################################################
## Synaptic mechs
###############################################################################
# Inhibitory synapses FS-> FS
tau_fall=2.
tau_rise=0.3
c_fall = 1/tau_fall
c_rise = 1/tau_rise
f = 1/( exp(-c_fall*log(c_rise/c_fall)/(c_rise-c_fall)) - exp(-c_rise*log(c_rise/c_fall)/(c_rise-c_fall)) )
U_SE=0.3; tau_d=100.
#Lets add synapses  
if cfg.WODepression==True:
    netParams.synMechParams['inhFSFS'] = {'mod': 'synact', 'tau_rise': tau_rise, 'tau_fall': tau_fall, 'f' : f, 'Es': cfg.Esyn_inh}        
else:
    gms = [i/U_SE for i in gms]
    netParams.synMechParams['inhFSFS'] = {'mod': 'synactdep', 'tau_rise': tau_rise, 'tau_fall': tau_fall, 'f' : f, 'xs' : 1, 'U_SE' : U_SE, 'tau_d' : tau_d, 'Es':cfg. Esyn_inh}
gms = [cfg.gmsScale*i for i in gms]
ggs = [cfg.ggsScale*i for i in ggs]
#Connectivity parameters
netParams.connParams['FS->FS_chem'] = {
        'preConds': {'pop': 'FS'},         # presynaptic conditions
        'postConds': {'pop': 'FS'},        # postsynaptic conditions
        'sec':'soma',
        'connList': syns,
        #am subbing weight for conductance, gms was in nanosiemens and needs to be converted to uS
        'weight': gms,                      # weight of each connection#gms*0.001
        'synMech': 'inhFSFS',                   # target inh synapse
         'delay': delays}                    # delay
if cfg.GAP==True:
    netParams.synMechParams['gap'] = {'mod': 'ElectSyn', 'g': 1}
    #Connectivity parameters
    netParams.connParams['FS->FS_gap'] = {
            'preConds': {'pop': 'FS'},         # presynaptic conditions
            'postConds': {'pop': 'FS'},        # postsynaptic conditions
            'connList': synsgj,
            'gapJunction': True, #Netpyne auto makes these junctions bidirectional so we don't want to read the direction in twice
            'sec':'soma',
            #am subbing weight for conductance, gms was in nanosiemens and needs to be converted to uS
            'weight': ggs,                      # weight of each connection
            'synMech': 'gap',                   # target inh synapse
            'delay': 0}

###############################################################################
## VoltageClamp
###############################################################################

if cfg.Clamp==True:
	netParams.stimSourceParams['Vclamp'] = {'type': 'SEClamp', 'dur1': 1e9, 'amp1': cfg.Vclamp, 'rs': 1e-4}

## Stimulation mapping parameters
	netParams.stimTargetParams['Vclamp->Cells'] = {
        'source': 'Vclamp',
        'sec': 'soma',
        'loc': 0.5,
        'conds': {'cellList': cfg.ClampCells}}

# Inhibitory synapses FS -> SC
tau_riseExc=0.4
tau_fallExc=6.
c_fall = 1./tau_fallExc; c_rise = 1./tau_riseExc
norm_synExc = 1./( exp(-c_fall*log(c_rise/c_fall)/(c_rise-c_fall)) - exp(-c_rise*log(c_rise/c_fall)/(c_rise-c_fall)) )
netParams.synMechParams['inhFSSC'] = {'mod': 'synactdep', 'tau_rise': tau_riseExc, 'tau_fall': tau_fallExc, 'f' : norm_synExc, 'xs' : 1, 'U_SE' : U_SE, 'tau_d' : tau_d, 'Es': -65.}
#Connectivity parameters
netParams.connParams['FS->SC'] = {
        'preConds': {'pop': 'FS'},         # presynaptic conditions
        'postConds': {'pop': 'SC'},        # postsynaptic conditions
        'sec':'soma',
        'probability': cfg.ConnProbIE,
        #am subbing weight for conductance, gms was in nanosiemens and needs to be converted to uS
        'weight': 'lognormal(1.65,2.17)*1e-3/0.3',                      # weight of each connection# Take into account that numpy and NEURON arguments are different (numpy args are mean and std for subjacent normal distribution, not the lognorm as in NEURON)
        'synMech': 'inhFSSC',                   # target inh synapse
         'delay': '0.6+(1-0.6)*uniform(0,1)'}                    # delay


# Excitatory synapses SC -> FS
netParams.synMechParams['AMPA'] = {'mod': 'ExpSyn', 'tau': 1, 'e': 0}  # excitatory synaptic mechanism
## Synaptic mechanism parameters
netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0}  # NMDA synaptic mechanism (NOT IMPLEMENTED YET)
#Connectivity parameters
netParams.connParams['SC->FS'] = {
        'preConds': {'pop': 'SC'},         # presynaptic conditions
        'postConds': {'pop': 'FS'},        # postsynaptic conditions
        'sec':'soma',
        'probability': cfg.ConnProbEI,
        #am subbing weight for conductance, gms was in nanosiemens and needs to be converted to uS
        'weight': cfg.Weight_E2I,#'0.0039*lognormal(0.01,1e-1)',       #'0.8*lognormal(0.01,1e-1)'               # weight of each connection#gms*0.001
        'synMech': 'AMPA',                   # target inh synapse
         'delay': '0.6+(1-0.6)*uniform(0,1)'} #'0.6+(1-0.6)*uniform(0,1)'                   # delay
