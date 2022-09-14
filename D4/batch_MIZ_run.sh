#!/bin/bash
#SBATCH -N 1
#SBATCH -n 12
#SBATCH --qos=normal
#SBATCH --job-name=12Cell
#SBATCH --output=Run12Cell.out
#SBATCH --time 0-02:00

rm -rf output

echo "Running 12 cell model at $(date)"

mpiexec nrniv -mpi -quiet -python run_network.py simulation_config_W+Cai.json

echo "Done running 12 cell model at $(date)"
