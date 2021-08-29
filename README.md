# PlasticityToyModel
## Running the models
### Build 12 cell
```
python build_12Cell.py
```
#####batch files for building 12 cell
```
sbatch batch_MIZ_build.sh
```
##### background inputs are stored in cell_inputs folder

### To run network
####Single core
```
python run_network.py simulation_config_W+Cai.json
``` 
####Parallel using mpi
#####replace 12 with 4 if using a personal computer with 4 cores
```
mpirun -n 12 nrniv -mpi -python run_network.py simulation_config_W+Cai.json
```
####Batch command
```
sbatch batch_MIZ_run.sh
```

###Analysis of the model
####histogram plots
```
python plot_12Cell.py
```
####graphs of cai and W for tone2pyr
```
python tone2pyr_plot.py
```
