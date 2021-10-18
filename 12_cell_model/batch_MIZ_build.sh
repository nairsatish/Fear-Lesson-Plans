#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=12cell
#SBATCH --output=build12Cell.out
#SBATCH --time 0-00:30

echo "building 10 cell model at $(date)"

rm -rf network

python3 build_12Cell.py

echo "Done building 10 cell model at $(date)"

