"""
Sairam

batch.py 

Batch simulation for mEC model using NetPyNE

Contributors: @Ananth @Roman
"""
import os
from netpyne.batch import Batch
from netpyne import specs
import numpy as np

# ----------------------------------------------------------------------------------------------
# Parameter for Changing Weights of Synaptic Connections
# ----------------------------------------------------------------------------------------------

def Vary_Weight_Seeds():#This varies multiple seeds and the E-->I connections
    params = specs.ODict()

    # Define a list of seed dictionaries
    num_simulations = 15 #Can use 2 to start and test out
    seed_list = []
    for i in range(num_simulations):
        seed_list.append({'conn': 4321 + i, 'stim': 1234 + i, 'loc': 4321 + i, 'Inet': 7894 + i , 'seed_index': i}) # Example of varying seeds

    params['seeds'] = seed_list
    weight_list = np.arange(0.000,0.00105,0.00005) #Can use a smaller number to testout [0.000, 0.001]
    weights = weight_list
    params['Weight_E2I'] = weights

    groupedParams = []
    initCfg = {}
    b = Batch(params=params, initCfg=initCfg, groupedParams=groupedParams)
    return b

def GE_GI():# This one is for varying both E->I and I->E conductance simultaneously
    params = specs.ODict()
    num_simulations = 9
    seed_list = []
    for i in range(num_simulations):
    	seed_list.append({'conn': 4321 + i, 'stim': 1234 + i, 'loc': 4321 + i, 'Inet': 7894 + i , 'seed_index': i}) # Example of varying seeds

    params['seeds'] = seed_list
    
    weight_list = np.arange(0.00005,0.00105,0.00005)
    weights = weight_list
    params['Weight_E2I'] = weights
    #scale_factors = np.arange(0.0, 5.5, 0.5)
    params['Weight_I2E'] = ['0.25*lognormal(1.65,2.17)*1e-3','0.5*lognormal(1.65,2.17)*1e-3','0.75*lognormal(1.65,2.17)*1e-3','1.0*lognormal(1.65,2.17)*1e-3','1.25*lognormal(1.65,2.17)*1e-3','1.5*lognormal(1.65,2.17)*1e-3','1.75*lognormal(1.65,2.17)*1e-3','2.0*lognormal(1.65,2.17)*1e-3','2.25*lognormal(1.65,2.17)*1e-3','2.5*lognormal(1.65,2.17)*1e-3','2.75*lognormal(1.65,2.17)*1e-3','3.0*lognormal(1.65,2.17)*1e-3','3.25*lognormal(1.65,2.17)*1e-3','3.5*lognormal(1.65,2.17)*1e-3','3.75*lognormal(1.65,2.17)*1e-3','4.0*lognormal(1.65,2.17)*1e-3','4.25*lognormal(1.65,2.17)*1e-3','4.5*lognormal(1.65,2.17)*1e-3','4.75*lognormal(1.65,2.17)*1e-3','5.0*lognormal(1.65,2.17)*1e-3']
    groupedParams = []
    initCfg = {}
    b = Batch(params=params, initCfg=initCfg, groupedParams=groupedParams)
    return b

# ----------------------------------------------------------------------------------------------
# Run configurations #Needs to be adjusted based on the HPC facilities available.
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi_bulletin', nodes=1, coresPerNode=8):
    if type=='mpi_bulletin':
        b.runCfg = {'type': 'mpi_bulletin', 
            'script': 'init.py', 
            'skip': True}

    elif type=='mpi_direct':
        b.runCfg = {'type': 'mpi_direct',
            'cores': 4,
            'script': 'init_cell.py',
            'mpiCommand': 'mpirun',
            'skip': True}

    elif type=='tigerfish':
        b.runCfg = {'type': 'hpc_slurm', 
            'nodes': 1,
            'coresPerNode': 1,  
            'script': 'init.py', 
            'skip': True,
            'mpiCommand': 'mpiexec', 
            'vmem': '2G',
            'walltime': "04:00:00",
            'skipCustom': '_raster.png'}

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------

if __name__ == '__main__': 

    b = Vary_Weight_Seeds()
    b.batchLabel = 'Varying_Seeds'
    folder = 'Output/'
    os.makedirs(folder, exist_ok = True) 
    b.saveFolder = folder
    b.method = 'grid'  # evol
    setRunCfg(b, 'tigerfish', nodes=1, coresPerNode=1)  # cores = nodes * 8 
    b.run() # run batch 
