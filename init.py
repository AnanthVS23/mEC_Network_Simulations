"""
init.py

Starting script to run NetPyNE-based mEC model.
"""
import numpy as np
from netpyne import sim
#from neuron import gui #this line is absolutely necessary if importing cells from hoc templates
#from neuron import h
#h.load_file("stdrun.hoc")
#from cfg import gmsScale, ggsScale, g_sin, g_sinExc, fsin, GAP, WODepression, Esyn_inh, N, HOMOGENEOUS, NumModels, FactorKv3, FactorKv7, FactorTau, ChemycalConnProb, GapJunctProb, SYNAPSES, #OPTODRIVE, NOISE, ConnProbIE, ConnProbEI, ICLAMP, CONSTANTOPTO, NumNetw, Vclamp  
###############################################################################
#cfg, netParams = sim.loadFromIndexFile('index.npjson') 
cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')
#comment here for batch smulations
cfg.filename = 'output/Ant&Ca_Weight_EI_%2.2f_gsinInh%2.1f_gsinExc%2.1f_EI_%2.1f_IE_%2.1f_II_%2.1f_GAP_%s_VC%2.1f' % (cfg.Weight_E2I*1e3,cfg.g_sin*1e3,cfg.g_sinExc*1e3,cfg.ConnProbEI,cfg.ConnProbIE,cfg.ChemycalConnProb,str(cfg.GAP)[0],cfg.Vclamp) + cfg.SYNAPSES + '_Noise_' + str(cfg.NOISE)[0]        # Set file output names
sim.create(netParams = netParams, simConfig = cfg)
sim.simulate()
sim.analyze()
