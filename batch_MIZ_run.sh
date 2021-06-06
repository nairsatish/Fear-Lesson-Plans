#!/bin/bash
#SBATCH -N 1
#SBATCH -n 10
#SBATCH --qos=normal
#SBATCH --job-name=10Cell
#SBATCH --output=Run10Cell.out
#SBATCH --time 0-02:00

module load mpi/mpich-3.2-x86_64
export LD_LIBRARY_PATH=$HOME/nrn/x86_64/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$HOME/nrn/lib/python:$PYTHONPATH
export PATH=$HOME/nrn/x86_64/bin:$PATH


rm -rf output

echo "Running 10 cell model at $(date)"

mpiexec nrniv -mpi -quiet -python run_network.py simulation_config.json

echo "Done running 10 cell model at $(date)"
