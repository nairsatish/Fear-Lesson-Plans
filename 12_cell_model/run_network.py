import os, sys
from bmtk.simulator import bionet
import numpy as np
import synapses
import warnings
import random

def run(config_file):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    synapses.load()

    conf = bionet.Config.from_json(config_file, validate=True)
    conf.build_env()
    graph = bionet.BioNetwork.from_config(conf)
    sim = bionet.BioSimulator.from_config(conf, network=graph)

    sim.run()
    bionet.nrn.quit_execution()


if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        seed = 967
        random.seed(seed)
        np.random.seed(seed)
        run(sys.argv[-1])
    else:
        seed = 967
        random.seed(seed)
        np.random.seed(seed)
        run('simulation_config_W+Cai.json')
