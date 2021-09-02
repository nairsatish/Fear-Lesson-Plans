from bmtk.builder import NetworkBuilder
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
from bmtk.utils.sim_setup import build_env_bionet
import numpy as np
import sys
import synapses

synapses.load()
syn = synapses.syn_params_dicts()

# Initialize our network

net = NetworkBuilder("biophysical")

net.add_nodes(N=1, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:feng_typeC',
              morphology=None)

# External excitatory inputs
tone = NetworkBuilder('tone')
tone.add_nodes(N=1,
               pop_name='tone',
               potential='exc',
               model_type='virtual')

# External inhibitory inputs
shock = NetworkBuilder('shock')
shock.add_nodes(N=1,
                pop_name='shock',
                potential='exc',
                model_type='virtual')
#backgrounds
backgroundPN = NetworkBuilder('bg_pn')
backgroundPN.add_nodes(N=1,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

# Create connections between Tone --> Pyr cells
net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=1,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2PN.json',
              model_template=syn['tone2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=1,
              syn_weight=1.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='shock2INT12.json',
              model_template=syn['shock2INT12.json']['level_of_detail'])

net.add_edges(source=backgroundPN.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=1,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template='exp2syn')

net.build()
net.save(output_dir='network')

tone.build()
tone.save_nodes(output_dir='network')

shock.build()
shock.save_nodes(output_dir='network')

backgroundPN.build()
backgroundPN.save_nodes(output_dir='network')

t_sim = 40000 # early extinction time is 232500 sensitization time is 40000
print("stim time is set to %s" % t_sim)

build_env_bionet(base_dir='../',
                 network_dir='./network',
                 tstop=t_sim, dt=0.1,
                 report_vars=['v'],
                 spikes_inputs=[('tone', './12_cell_inputs/tone_spikes.csv'),
                                ('shock', './12_cell_inputs/shock_spikes.csv'),
                                ('bg_pn', '12_cell_inputs/bg_pn_spikes.h5')],
                 components_dir='../biophys_components',
                 config_file='config.json',
                 compile_mechanisms=False)

psg = PoissonSpikeGenerator(population='bg_pn')
psg.add(node_ids=range(1),  # need same number as cells
        firing_rate=1,    # 1 spike every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('12_cell_inputs/bg_pn_spikes.h5')

print('Number of background spikes for pn: {}'.format(psg.n_spikes()))



