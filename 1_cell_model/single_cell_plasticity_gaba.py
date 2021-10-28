from bmtk.builder import NetworkBuilder
import numpy as np
import sys
import synapses
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator

net = NetworkBuilder("biophysical")

net.add_nodes(N=3, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:Cell_Cf',
              morphology=None)

net.build()
net.save(output_dir='network')



