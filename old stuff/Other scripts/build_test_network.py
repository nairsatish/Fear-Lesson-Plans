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


net.add_nodes(N=1, pop_name='Int',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)

thalamus = NetworkBuilder('mthalamus')
thalamus.add_nodes(N=1,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

thalamus.add_edges(source={'pop_name': 'tON'}, target=net.nodes(pop_name=['Int']),
                   connection_rule=1,
                   syn_weight=1,
                   delay=2.0,
                   weight_function=None,
                   target_sections=['somatic'],
                   distance_range=[0.0, 150.0],
                   dynamics_params='AMPA_ExcToExc.json',
                   model_template='exp2syn')

net.build()
net.save(output_dir='network')
thalamus.build()
thalamus.save(output_dir='network')

psg = PoissonSpikeGenerator(population='mthalamus')
psg.add(node_ids=1,  # Have 5 nodes to match mthalamus
        firing_rate=8,    # 2 Hz
        times=(0.0, 1))  # time is in seconds for some reason
psg.to_sonata('virtual_spikes.h5')
print('Number of background spikes: {}'.format(psg.n_spikes()))

from bmtk.utils.sim_setup import build_env_bionet
build_env_bionet(base_dir='../',
                 network_dir='./network',
                 tstop=1000.0, dt = 0.1,
                 report_vars=['v'],
                 spikes_inputs=[('mthalamus', 'virtual_spikes.h5')],
                 #current_clamp={
                 #    'amp': -0.100,
                 #    'delay': 250.0,
                 #    'duration': 200 #200 for bask 600 for pyr
                 #},
                 components_dir='../biophys_components',
                 config_file='../simulation_config.json',
                 compile_mechanisms=False)

