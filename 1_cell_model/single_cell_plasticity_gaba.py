from bmtk.builder import NetworkBuilder
import numpy as np
import sys

from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator


net = NetworkBuilder("biophysical")
"""
net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:olmcell',
        morphology=None)
"""

"""
net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:feng_typeA',
        morphology=None)
"""

"""
net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:feng_typeC',
        morphology=None)
"""


net.add_nodes(N=1, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)


net.build()
net.save(output_dir='network')


