from bmtk.builder import NetworkBuilder
import numpy as np
import sys
import synapses

synapses.load()
syn = synapses.syn_params_dicts()

# Initialize our network

net = NetworkBuilder("biophysical")

net.add_nodes(N=5, pop_name='PyrA',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:feng_typeA',
              morphology=None)

net.add_nodes(N=3, pop_name='PyrC',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:feng_typeC',
              morphology=None)

net.add_nodes(N=2, pop_name='PV',
              mem_potential='e',
              model_type='biophysical',
              model_template='hoc:basket',
              morphology=None)



##################################################################################
###################################External Networks##############################

print("making exc_stim nodes")
tone = NetworkBuilder('tone')
tone.add_nodes(N=1,
               pop_name='tone',
               potential='exc',
               model_type='virtual')


print("making {} inh_stim nodes")
shock = NetworkBuilder('shock')
shock.add_nodes(N=1,
                pop_name='shock',
                potential='exc',
                model_type='virtual')

backgroundPN = NetworkBuilder('bg_pn')
backgroundPN.add_nodes(N=8,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')

backgroundPV = NetworkBuilder('bg_pv')
backgroundPV.add_nodes(N=2,
                   pop_name='tON',
                   potential='exc',
                   model_type='virtual')


##################################################################################
###################################Edges##########################################

def one_to_one(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting cell {} to {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn


def shock_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if (tid == 0 or tid == 3 or tid == 4 or tid == 6 or tid == 7 or tid == 8 or tid == 9):
        print("connecting shock cell {} to {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return None
    return tmp_nsyn


def tone_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if (tid == 2 or tid == 4 or tid == 6 or tid == 7 or tid == 8 or tid == 9):
        print("connecting tone cell {} to {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return None
    return tmp_nsyn


def get_node_ids(source, target):
    sid = source.node_id
    tid = target.node_id
    print("source and targets are {} and {}".format(sid, tid))
    return None


# idea for pyr_connection is that if its called it will always create a connection since all pyra cells are connected
def pyr_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting pyra cells {} and {}".format(sid, tid))
    return 1


def int_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if (sid != tid):
        print("connecting PV cell {} to {}".format(sid, tid))
        tmp_nsyn = 1
    else:
        return None
    return tmp_nsyn


# basically same as pyr connecting (always makes connection from source to target) only difference is print to make output easier to understand
def int_pyr_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting PV cells {} to pyra cell {}".format(sid, tid))
    return 1

def BG_to_PN(source, target):
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting BG {} to PN{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

def BG_to_PV(source, target):
    sid = source.node_id
    tid = target.node_id
    sid = sid + 8
    if sid == tid:
        print("connecting BG {} to pv{}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn
# Create connections between Shock --> Pyr cells
net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrA'),
              connection_rule=shock_connection,
              syn_weight=40.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='shock2PN.json',
              model_template=syn['shock2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=shock_connection,
              syn_weight=40.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='shock2PN.json',
              model_template=syn['shock2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=shock_connection,
              syn_weight=20.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='shock2INT.json',
              model_template=syn['shock2INT.json']['level_of_detail'])

# Create connections between Tone --> Pyr cells
net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PyrA'),
              connection_rule=tone_connection,
              syn_weight=10.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2PN.json',
              model_template=syn['tone2PN.json']['level_of_detail'])

net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PyrC'),
              connection_rule=tone_connection,
              syn_weight=10.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2PN.json',
              model_template=syn['tone2PN.json']['level_of_detail'])

net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=tone_connection,
              syn_weight=3.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='tone2INT.json',
              model_template=syn['tone2INT.json']['level_of_detail'])

# Create connections between Pyr --> Pyr cells
net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PyrA'),
              connection_rule=pyr_connection,
              syn_weight=1.5, # was 1.5
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PyrC'),
              connection_rule=pyr_connection,
              syn_weight=1.50,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrA'),
              connection_rule=pyr_connection,
              syn_weight=1.5, # was 1.5
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrC'),
              connection_rule=pyr_connection,
              syn_weight=1.50,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

# Create connections between Pyr --> PV cells
net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PV'),
              connection_rule=pyr_connection,
              syn_weight=1, # was 1 but forsure needs to be higher
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToInh.json',
              model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PV'),
              connection_rule=pyr_connection,
              syn_weight=1, # best 2.5
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='AMPA_ExcToInh.json',
              model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])
# Create connections PV --> PV cells

net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PV'),
              connection_rule=int_connection,
              syn_weight=3.0, # was 3
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToInh.json',
              model_template=syn['GABA_InhToInh.json']['level_of_detail'])

# Create connections PV --> Pyr cells
net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PyrA'),
              connection_rule=int_pyr_connection,
              syn_weight=5, # was 5
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToExc.json',
              model_template=syn['GABA_InhToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name='PyrC'),
              connection_rule=int_pyr_connection,
              syn_weight=5.0,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[10.0, 11.0],
              dynamics_params='GABA_InhToExc.json',
              model_template=syn['GABA_InhToExc.json']['level_of_detail'])

# background connections
# edge makes around 1 hz

net.add_edges(source=backgroundPN.nodes(), target=net.nodes(pop_name=['PyrA', 'PyrC']),
              connection_rule=BG_to_PN,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToExc.json',
              model_template='exp2syn')

net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
              connection_rule=BG_to_PV,
              syn_weight=1,
              target_sections=['somatic'],
              delay=0.1,
              distance_range=[0.0, 300.0],
              dynamics_params='AMPA_ExcToInh.json',
              model_template='exp2syn')


# Build and save our networks

net.build()
net.save(output_dir='network')


tone.build()
tone.save_nodes(output_dir='network')

shock.build()
shock.save_nodes(output_dir='network')

backgroundPN.build()
backgroundPN.save_nodes(output_dir='network')

backgroundPV.build()
backgroundPV.save_nodes(output_dir='network')


t_sim = 232500 # early extinction time is 232500 sensitization time is 40000
print("stim time is set to %s" % t_sim)

from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator

# from bmtk.utils.reports.spike_trains.spikes_file_writers import write_csv

#tone_fr = 2

#exc_psg = PoissonSpikeGenerator(population='tone')
#exc_psg.add(node_ids=0,
#            firing_rate=int(tone_fr),
#            times=(0.0, t_sim/1000))
#exc_psg.to_sonata('tone_poisson_spikes.h5')





from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(base_dir='./',
                 network_dir='./network',
                 tstop=t_sim, dt=0.1,
                 spikes_inputs=[('tone', './10_cell_spikes/tone_spikes.csv'),
                                ('shock', './10_cell_spikes/shock_spikes.csv'),
                                ('bg_pn', '10_cell_spikes/bg_pn_spikes.h5'),
                                ('bg_pv', '10_cell_spikes/bg_pv_spikes.h5')],
                 components_dir='biophys_components',
                 config_file='config.json',
                 compile_mechanisms=False)

psg = PoissonSpikeGenerator(population='bg_pn')
psg.add(node_ids=range(8),  # need same number as cells
        firing_rate=2,    # 1 spike every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('10_cell_spikes/bg_pn_spikes.h5')

print('Number of background spikes for pn: {}'.format(psg.n_spikes()))


psg = PoissonSpikeGenerator(population='bg_pv')
psg.add(node_ids=range(2),  # need same number as cells
        firing_rate=8,    # 8 spikes every 1 second Hz
        times=(0.0, t_sim/1000))  # time is in seconds for some reason
psg.to_sonata('10_cell_spikes/bg_pv_spikes.h5')
print('Number of background spikes for pv: {}'.format(psg.n_spikes()))
