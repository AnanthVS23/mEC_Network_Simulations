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

def Vary_Weight_Seeds():
    params = specs.ODict()

    # Define a list of seed dictionaries
    num_simulations = 10 #Can use 2 to start and test out
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
            'folder': '/mnt/beegfs/home/avedur/NetPyNe_Sims/Automated/mEC_Network_Simulations/',  #This ishould be the path to the folder where init.py exists
            'script': 'init.py', 
            'mpiCommand': 'mpiexec', 
            'skipCustom': '_raster.png'}

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------

if __name__ == '__main__': 

    b = Vary_Weight_Seeds()
    b.batchLabel = 'Varying_Seeds'
    path = '/mnt/beegfs/home/avedur/NetPyNe_Sims/Automated/mEC_Network_Simulations/output/' #This is for creating the output
    os.makedirs(path, exist_ok = True) 
    b.saveFolder = path+b.batchLabel
    b.method = 'grid'  # evol
    setRunCfg(b, 'tigerfish', nodes=1, coresPerNode=1)  # cores = nodes * 8 
    b.run() # run batch 
