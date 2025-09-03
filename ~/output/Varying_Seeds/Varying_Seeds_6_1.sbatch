#!/bin/bash
#SBATCH --job-name=Varying_Seeds_6_1
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH -o ~/output/Varying_Seeds/Varying_Seeds_6_1.run
#SBATCH -e ~/output/Varying_Seeds/Varying_Seeds_6_1.err
#SBATCH --mail-user=a@b.c
#SBATCH --mail-type=end


source ~/.bashrc
cd ~/output
mpiexec -n 1 nrniv -python -mpi init.py simConfig=~/output/Varying_Seeds/Varying_Seeds_6_1_cfg.json netParams=~/output/Varying_Seeds/Varying_Seeds_netParams.py
wait
    