from bmtk.builder import NetworkBuilder
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
from bmtk.utils.sim_setup import build_env_bionet
import numpy as np
import sys
import synapses
import random

seed = 967
random.seed(seed)
np.random.seed(seed)

synapses.load()
syn = synapses.syn_params_dicts()

net = NetworkBuilder("biophysical")

net.add_nodes(N=2, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:feng_typeC',
              morphology=None)

net.add_nodes(N=1, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)

backgroundPN = NetworkBuilder('bg_pn')
backgroundPN.add_nodes(N=1,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

backgroundPV = NetworkBuilder('bg_pv')
backgroundPV.add_nodes(N=1,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

def pn2pv(source, target):
    sid = source.node_id
    tid = target.node_id
    if(sid == 0):
        return 1
    else:
        return 0

def pv2pn(source, target):
    sid = source.node_id
    tid = target.node_id
    if(tid==1):
        return 1
    else:
        return 1 #change this from 0 to 1 and that will miss up the synapse

def bg2pn(source, target):
    tid = target.node_id
    if(tid==0):
        return 1
    else:
        return 0

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PV'),
              connection_rule=pn2pv,
              syn_weight=1,
              target_sections=['basal'],
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PN2PV.json',
              model_template=syn['PN2PV.json']['level_of_detail'])

conn = net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PyrC'),
              connection_rule=pv2pn,
              syn_weight=1.0,
              delay=0.1,
              distance_range=[-10000, 10000],
              dynamics_params='PV2PN.json',
              model_template=syn['PV2PN.json']['level_of_detail'])

conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float]) # places syn on apic at 0.9

#net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
#              connection_rule=1,
#              syn_weight=1.0,
#              target_sections=['somatic'],
#              delay=0.1,
#              distance_range=[-10000, 10000],
#              dynamics_params='AMPA_ExcToInh.json',
#              model_template='exp2syn')

#net.add_edges(source=backgroundPN.nodes(), target=net.nodes(pop_name='PyrC'),
#              connection_rule=bg2pn,
#              syn_weight=1.0,
#              target_sections=['apical'],
#              sec_x=0.9,
#              delay=0.1,
#              distance_range=[-10000, 10000],
#              dynamics_params='AMPA_ExcToExc.json',
#              model_template='exp2syn')

net.build()
net.save(output_dir='network')

#backgroundPN.build()
#backgroundPN.save_nodes(output_dir='network')

backgroundPV.build()
backgroundPV.save_nodes(output_dir='network')

psg = PoissonSpikeGenerator(population='bg_pn')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=2,    # 1 spike every 1 second Hz
        times=(0.0, 40000/1000))  # time is in seconds for some reason
psg.to_sonata('2_cell_inputs/bg_pn_spikes.h5')

print('Number of background spikes for pn: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_pv')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=4,    # 8 spikes every 1 second Hz
        times=(0.0, 40000/1000))  # time is in seconds for some reason
psg.to_sonata('2_cell_inputs/bg_pv_spikes.h5')

print('Number of background spikes for pv: {}'.format(psg.n_spikes()))