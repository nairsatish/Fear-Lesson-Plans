"""Script for running the network built in build_network.py
Also saves a file called Connections.csv that consists of information about
each synapse in the simulation.
"""

import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)

from bmtk.simulator import bionet
import numpy as np
from neuron import h
import synapses
import pandas as pd



def save_connections(graph, sim):
    cells = graph.get_local_cells()
    cell = cells[list(cells.keys())[0]]
    h.distance(sec=cell.hobj.soma[0])
    sec_types = []  # soma, apic, or dend
    dists = []
    names = []  # full NEURON str representation of postsynaptic segment

    for c in cell.connections():
        con = c._connector
        seg = con.postseg()
        fullsecname = seg.sec.name()
        names.append(str(seg))
        sec_types.append(fullsecname.split(".")[1][:4])
        dists.append(float(h.distance(seg)))

    df = pd.DataFrame()
    df["Type"] = sec_types
    df["Name"] = names
    df.to_csv("Connections.csv", index=False)

synapses.load()
config_file = '2Cell_SC.json'
conf = bionet.Config.from_json(config_file, validate=True)
conf.build_env()
graph = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=graph)

save_connections(graph,sim)
