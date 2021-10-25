from bmtk.builder import NetworkBuilder
import numpy as np
import sys
import synapses
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator

synapses.load()
syn = synapses.syn_params_dicts()

net = NetworkBuilder("biophysical")

net.add_nodes(N=1, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)

shock = NetworkBuilder('shock')
shock.add_nodes(N=1,
                pop_name='shock',
                potential='exc',
                model_type='virtual')

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=1,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='shock2INT12.json',
              model_template=syn['shock2INT12.json']['level_of_detail'])

net.build()
net.save(output_dir='network')

shock.build()
shock.save(output_dir='network')

psg = PoissonSpikeGenerator(population='shock')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=200,    # 1 spike every 1 second Hz
        times=(0.0, 5))  # time is in seconds for some reason
psg.to_sonata('1_cell_inputs/shock.h5')


