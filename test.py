from bmtk.builder import NetworkBuilder
from bmtk.utils.sim_setup import build_env_bionet
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
import numpy as np
import sys
import synapses

synapses.load()
syn = synapses.syn_params_dicts()

net = NetworkBuilder("biophysical")


net.add_nodes(N=1, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)

net.add_nodes(N=1, pop_name='OLM',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:SOM_Cell',
              morphology=None)

net.add_nodes(N=1, pop_name='PYR',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:feng_typeC',
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

backgroundOLM = NetworkBuilder('bg_olm')
backgroundOLM.add_nodes(N=1,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

"""
tone = NetworkBuilder('tone')

tone.add_nodes(N=1,
               pop_name='tone',
               potential='exc',
               model_type='virtual')

shock = NetworkBuilder('shock')

shock.add_nodes(N=1,
               pop_name='shock',
               potential='exc',
               model_type='virtual')



net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PYR'),
              connection_rule=1,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToExc.json',
              model_template=syn['GABA_InhToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='OLM'),
              connection_rule=1,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToInh.json',
              model_template=syn['GABA_InhToInh.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='SOM'), target=net.nodes(pop_name='PYR'),
              connection_rule=1,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToExc.json',
              model_template=syn['GABA_InhToExc.json']['level_of_detail'])

net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=1,
              syn_weight=3.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2INT.json',
              model_template=syn['tone2INT.json']['level_of_detail'])


net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PYR'),
              connection_rule=1,
              syn_weight=10.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2PN.json',
              model_template=syn['tone2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='OLM'),
              connection_rule=1,
              syn_weight=10.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='Shock2INT_12.json',
              model_template=syn['Shock2INT_12.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=1,
              syn_weight=10.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='Shock2INT_12.json',
              model_template=syn['Shock2INT_12.json']['level_of_detail'])
"""

def BG_to_PN(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 2
    if sid == tid:
        print("connecting BG {} to PN{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

def BG_to_PV(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting BG {} to pv{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

def BG_to_OLM(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 1
    if sid == tid:
        print("connecting BG {} to olm{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn


net.add_edges(source=backgroundPN.nodes(), target=net.nodes(pop_name='PYR'),
              connection_rule=BG_to_PN,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template='exp2syn')

net.add_edges(source=backgroundOLM.nodes(), target=net.nodes(pop_name='OLM'),
              connection_rule=BG_to_OLM,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToInh.json',
              model_template='exp2syn')

net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=BG_to_PV,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToInh.json',
              model_template='exp2syn')

net.build()
net.save(output_dir='network')

backgroundPN.build()
backgroundPN.save(output_dir='network')

backgroundPV.build()
backgroundPV.save(output_dir='network')

backgroundOLM.build()
backgroundOLM.save(output_dir='network')

#tone.build()
#tone.save(output_dir='network')

#shock.build()
#shock.save(output_dir='network')

t_stim = 1000
build_env_bionet(base_dir='./',
                 network_dir='./network',
                 tstop=t_stim, dt=0.1,
                 report_vars=['v'],
                spikes_inputs=[('bg_pn', '12_cell_inputs/bg_pn_spikes.h5'),
                               ('bg_pv', '12_cell_inputs/bg_pv_spikes.h5'),
                               ('bg_olm', '12_cell_inputs/bg_olm_spikes.h5')],
                components_dir='biophys_components',
                config_file='config.json',
                compile_mechanisms=False)


psg = PoissonSpikeGenerator(population='bg_pn')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=1,    # 1 spike every 1 second Hz
        times=(0.0, t_stim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pn_spikes.h5')

print('Number of background spikes for pn: {}'.format(psg.n_spikes()))


psg = PoissonSpikeGenerator(population='bg_pv')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=8,    # 8 spikes every 1 second Hz
        times=(0.0, t_stim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pv_spikes.h5')

print('Number of background spikes for pv: {}'.format(psg.n_spikes()))

psg = PoissonSpikeGenerator(population='bg_olm')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=2,    # 8 spikes every 1 second Hz
        times=(0.0, t_stim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_olm_spikes.h5')

print('Number of background spikes for olm: {}'.format(psg.n_spikes()))