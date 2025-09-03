# mEC Model
 
 This code was written using NetPyNE (Networks with Python and NEURON). For more information about the tool, see [NetPyNE docs](http://doc.netpyne.org/)

## Download the Repository

To clone the dev branch of the repository, open a terminal in the directory where you'd like to store the project and run:

```bash
git clone --branch dev --single-branch https://github.com/RomanB22/mEC_model2025.git
````

After that, make sure to move to the repo folder using `cd mEC_Network_Simulations`.

## Installation

Install the required Python packages using:

```bash
pip install -r Requirements.txt
```

## Simulations Setup

Add the root directory to `PYTHONPATH`, and compile the mechanisms:

```bash
export PYTHONPATH=PYTHONPATH:$PWD
nrnivmodl mod
```
## ▶Running Simulations

### Run a Single Simulation

All simulation parameters are defined in the `cfg.py` file. To run a single simulation:

```bash
python -u init.py
```
-- In the cfg.py the duration of the simulation, the optogenetic drives to the cell populations, connection probabilities, reversal potentials, clamping simulations can be modified
-- In that file, gapjunctions, synaptic depression can also be modified based on the simulation need 
-- Since the primary focus of this paper is on excitatory to inhibitory synaptic weight, the Weight_EI parameter plays a crucial role.For individual simulations, the output filename incorporates the optodrives and this EI_Weight as well. 
-- For pure ING simulations, we set the E-I and I-E connection probabilities to 0 and also the optodrive to E cells is set to 0. 

### Run Batch Simulations

To run multiple simulations on the terminal using the batch submitter:

```bash
python -u batch.py
```

### Output
The output from all the simulations get saved in the ~/output/ folder. Individual simulations by running init.py have the filenames tailor-made to have parameter values. The batch simulations get saved based on the batch array and the parameters corresponding to the simulations can be understood from batch.py.

### Analysis

The analysis folder has python codes that would extract data from simulations through the .pkl files to analyze the output whether in the form of rasters, scalograms, current waveforms, etc. 

> ⚠️ Note: For running Batch simulations, batch.py needs to be edited to match the local system or HPC system at the place of simulation.

## Model Description

- 
