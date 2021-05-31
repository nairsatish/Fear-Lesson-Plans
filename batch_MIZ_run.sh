#!/bin/bash
#SBATCH -N 1
#SBATCH -n 10
#SBATCH --qos=normal
#SBATCH --job-name=10Cell
#SBATCH --output=Run10Cell.out
#SBATCH --time 0-02:00

rm -rf output

echo "Running 10 cell model at $(date)"

mpiexec nrniv -mpi -quiet -python run_save_network.py simulation_config.json

echo "Done running 10 cell model at $(date)"
