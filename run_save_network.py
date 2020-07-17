import sys, os
from bmtk.simulator import bionet
import numpy as np
import pandas as pd
import h5py
from neuron import h
from scipy.stats import skew
import synapses
from bmtk.simulator.bionet.pyfunction_cache import add_weight_function

synapses.load()

pc = h.ParallelContext()  # object to access MPI methods
MPI_size = int(pc.nhost())
MPI_rank = int(pc.id())


config_file = 'simulation_config.json'



conf = bionet.Config.from_json(config_file, validate=True)
conf.build_env()

graph = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=graph)

cells = graph.get_local_cells()


sim.run()
pc.barrier()




