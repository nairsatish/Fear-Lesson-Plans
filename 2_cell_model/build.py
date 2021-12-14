import synapses
from bmtk.builder import NetworkBuilder
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
from bmtk.utils.sim_setup import build_env_bionet
import numpy as np
import os
import random
import shutil

if os.path.isdir('network'):
    shutil.rmtree('network')
if os.path.isdir('2_cell_inputs'):
    shutil.rmtree('2_cell_inputs')

seed = 967
random.seed(seed)
np.random.seed(seed)
synapses.load()
syn = synapses.syn_params_dicts()

# Initialize our network

net = NetworkBuilder("biophysical")

num_inh = [1]

num_exc = [1]

##################################################################################
###################################BIOPHY#########################################

# PN
net.add_nodes(N=1, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:Cell_C',
              morphology=None)

# PV
net.add_nodes(N=1, pop_name="PV",
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None
              )

backgroundPN_C = NetworkBuilder('bg_pn_c')
backgroundPN_C.add_nodes(N=1,
                         pop_name='tON',
                         potential='exc',
                         model_type='virtual')

backgroundPV = NetworkBuilder('bg_pv')
backgroundPV.add_nodes(N=2,
                       pop_name='tON',
                       potential='exc',
                       model_type='virtual')


# if neuron is sufficiently depolorized enough post synaptic calcium then synaptiic weight goes up

# pyr->pyr & pyr->PV
# PV->pyr PV->PV
def one_to_all(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting bio cell {} to bio cell {}".format(sid, tid))
    return 1


def BG_to_PN_C(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting BG {} to PN_C{}".format(sid, tid))
        return 1
    else:
        return 0


def BG_to_PV(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 1
    if sid == tid:
        print("connecting BG {} to PV{}".format(sid, tid))
        return 1
    else:
        return 0


conn = net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name="PV"),
                     connection_rule=one_to_all,
                     syn_weight=1.0,
                     delay=0.1,
                     distance_range=[-10000, 10000],
                     dynamics_params='PN2PV.json',
                     model_template=syn['PN2PV.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

conn = net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name="PyrC"),
                     connection_rule=one_to_all,
                     syn_weight=1.0,
                     delay=0.1,
                     distance_range=[-10000, 10000],
                     dynamics_params='PV2PN.json',
                     model_template=syn['PV2PN.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

conn = net.add_edges(source=backgroundPN_C.nodes(), target=net.nodes(pop_name='PyrC'),
                     connection_rule=BG_to_PN_C,
                     syn_weight=1.0,
                     delay=0.1,
                     distance_range=[-10000, 10000],
                     dynamics_params='BG2PNC.json',
                     model_template=syn['BG2PNC.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float])  # places syn on apic at 0.9

conn = net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
                     connection_rule=BG_to_PV,
                     syn_weight=1.0,
                     delay=0.1,
                     distance_range=[-10000, 10000],
                     dynamics_params='BG2PV.json',
                     model_template=syn['BG2PV.json']['level_of_detail'])
conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

backgroundPN_C.build()
backgroundPN_C.save_nodes(output_dir='network')

backgroundPV.build()
backgroundPV.save_nodes(output_dir='network')

net.build()
net.save(output_dir='network')
# SPIKE TRAINS
t_sim = 40000

#build_env_bionet(base_dir='./',
#                 network_dir='./network',
#                 tstop=t_sim, dt=0.1,
#                 report_vars=['v'],
#                 components_dir='biophys_components',
#                 config_file='config.json',
#                 spikes_inputs=[('bg_pn_c', '2_cell_inputs/bg_pn_c_spikes.h5'),
#                                ('bg_pv', '2_cell_inputs/bg_pv_spikes.h5')],
#                 compile_mechanisms=False)

psg = PoissonSpikeGenerator(population='bg_pn_c')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=6,  # 1 spike every 1 second Hz
        times=(0.0, t_sim / 1000))  # time is in seconds for some reason
psg.to_sonata('2_cell_inputs/bg_pn_c_spikes.h5')

print('Number of background spikes for PN_C: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_pv')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=7.7,  # 8 spikes every 1 second Hz
        times=(0.0, t_sim / 1000))  # time is in seconds for some reason
psg.to_sonata('2_cell_inputs/bg_pv_spikes.h5')

print('Number of background spikes for PV: {}'.format(psg.n_spikes()))


