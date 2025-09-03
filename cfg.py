from netpyne import specs

# Simulation options
cfg = specs.SimConfig()       # object of class SimConfig to store simulation configuration
cfg.duration = 12*125          # Duration of the simulation, in ms
cfg.dt = 1e-2                # Internal integration timestep to use
cfg.verbose = False           # Show detailed messages
cfg.ClampCells = [1,20,40,50,90,105,110,120,130,230,250,270,290,300,350]
recordedCells2 = [1,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,350,400]
recordedCells3 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,350,400]
for_raster = [16,18,27,31,35,50,56,59,72,73,77,81,93,250]
offset = 0
timeRange = [8*125.,cfg.duration+offset]
cfg.recordCells = recordedCells3
cfg.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'},'i_soma': {'sec':'soma','loc':0.5, 'stim': 'Vclamp->Cells', "var": 'ic'} }  # Dict with traces to record
cfg.recordStep = 1e-2         # Step size in ms to save data (e.g. V traces, LFP, etc)
cfg.savePickle = True        # Save params, network and sim output to pickle file
#cfg.analysis['plotRaster'] = {'include': recordedCells2,'saveFig': True, 'timeRange': timeRange}                  # Plot a raster
#cfg.analysis['plotSpikeHist'] = {'saveFig': True, 'timeRange': timeRange, 'binSize': 1, 'measure': 'rate', 'histtype': 'stepfilled'}                  # Plot a Spike Histogram
cfg.analysis['plotSpikeHist'] = {'saveFig': True, 'timeRange': timeRange, 'binSize': 1, 'measure': 'rate'}                  # Plot a Spike Histogram
cfg.analysis['plotTraces'] = {'include': for_raster, 'saveFig': True, 'timeRange': timeRange}  # Plot recorded traces for this list of cells
#cfg.analysis['spikes'] = {'include': recordedCells3, 'timeRange': timeRange, 'saveData':True, 'fileName':Spikes, 'fileType':.pkl, 'fileDir'=None}
#cfg.analysis.spikes.prepareSpikeData(include=['allCells'], sim=None, timeRange=None, maxSpikes=100000000.0, orderBy='gid', popRates=True, syncLines=True, saveData=False, fileName=None, fileDesc=None, fileType=None, fileDir=None, colorbyPhase=None, **kwargs)
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321, 'Inet': 7894}
#cfg.seeds = {'conn': 4322, 'stim': 1235, 'loc': 4322, 'Inet': 7895} #Seed 2
cfg.saveJson = False #Make it true only for individual simulations to see the connections
cfg.saveCellConns = True
cfg.saveDataInclude = ['simData', 'simConfig', 'net']
###############################################################################
## SimParams
############################################################################### 
cfg.fsin = 8
cfg.Vclamp = -70
cfg.g_sin = 7.*1e-3                   
cfg.g_sinExc = 3.*1e-3
#IClamp                                                                                                                                                       
cfg.ICLAMP=False                                                                                                                                                                                 
cfg.OPTODRIVE=True                                                                                                                                                                               
cfg.CONSTANTOPTO=False  
cfg.Weight_E2I = 0.0001
#Condition whether to CLAMP or NO!! Thie leads to clamping in netParams.py
cfg.Clamp=True                                                                                                                                                                                                                                                                                                                                                                                                                                                       
cfg.gmsScale = 1 # Scaling for the synaptic conductances                                                                                                                                         
cfg.ggsScale = 1 # Scaling for gap junction conductances                                                                                                                                                                                                                                                                                                                                      
#Which Synapses?                                                                                                                                                                             
cfg.GAP=True #False                                                                                                                                                                         
cfg.WODepression=False # Without short-term depression                                                                                                                                           
#Some of Guillem's variables                                                                                                                                                                 
cfg.SYNAPSES = 'Hyper' # ['Hyper','Shunt','Uniform']                                                                                                                                             
if cfg.SYNAPSES == 'Hyper':
    cfg.Esyn_inh = -75     
elif cfg.SYNAPSES == 'Shunt':
    cfg.Esyn_inh = -55              
elif cfg.SYNAPSES == 'Uniform':
    cfg.Esyn_inh = 'uniform(-70,-55)'          
else:
    print('Synaptic reversal potential not defined')  
cfg.N=100 # Number of Inhibitory neurons
cfg.HOMOGENEOUS = False 
if cfg.HOMOGENEOUS and cfg.GAP==False:
    cfg.NumModels = 1
else:
    cfg.NumModels = cfg.N

cfg.GapJunctProb, cfg.ChemycalConnProb = 0.01, 0.3 # Probability connections from FS PV+ to FS PV+                          
                                                                          
cfg.ConnProbIE, cfg.ConnProbEI = 0.2, 0.3 # FS PV+ to SC and SC to FS PV+ probability connections          
                                                                                  
cfg.FactorTau, cfg.FactorKv3, cfg.FactorKv7 = 1, 1, 1   # To modify the activation curves for ion channels and the membrane time constant     
                                                            
cfg.NumNetw = 1  # Number of networks     

cfg.NOISE=False # If true, adds a random fluctuating current simulating in-vivo like CORTEX noise. TODO: Adjust parameters for mEC region 
cfg.MeanENoise, cfg.MeanINoise, cfg.StdENoise, cfg.StdINoise = 0, 0*0.0001, 0.000001, 0.000001                                             
cfg.I_sin=0   
