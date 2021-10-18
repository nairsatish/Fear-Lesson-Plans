# PlasticityToyModel
## Running the models
##The main model is the 12 cell all others are used for debugging
```
cd 12_cell_model
```
### Build 12 cell
```
python build_12Cell.py
```
#####batch files for building 12 cell(not very important currently)
```
sbatch batch_MIZ_build.sh
```
#####background inputs are stored in cell_inputs folder
#####To compile the mod files
```
cd biophys_components/mechanisms
nrnivmodl modfiles
cd ..
cd ..
```

#####To run network
######Single core
```
python run_network.py simulation_config_W+Cai.json
``` 
######Parallel using mpi
replace 12 with 4 if using a personal computer with 4 cores
```
mpirun -n 12 nrniv -mpi -python run_network.py simulation_config_W+Cai.json
```
####Batch command
```
sbatch batch_MIZ_run.sh
```

####Analysis of the model
histogram plots
```
python plot_12Cell.py
```
#####graphs for the syn weight of each synapse
```
python syn_weight_plotter.py
```
#####graphs for the cai inside each synapse
```
python cai_plotter.py
```
