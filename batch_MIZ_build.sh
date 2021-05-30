#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --qos=normal
#SBATCH --job-name=10cell
#SBATCH --output=build10Cell.out
#SBATCH --time 0-00:30

echo "building 10 cell model at $(date)"

rm -rf network

python3 build_network.py

echo "Done building 10 cell model at $(data)"

