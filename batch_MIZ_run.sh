#!/bin/bash
#SBATCH -N 1
#SBATCH -n 10
#SBATCH --qos=normal
#SBATCH --job-name=12Cell
#SBATCH --output=Run12Cell.out
#SBATCH --time 0-02:00

rm -rf output

echo "Running 10 cell model at $(date)"

mpiexec nrniv -mpi -quiet -python run_network.py config.json

echo "Done running 10 cell model at $(date)"
