from bmtk.builder import NetworkBuilder
import numpy as np
import sys
import synapses

synapses.load()
syn = synapses.syn_params_dicts()


# Initialize our network

net = NetworkBuilder("biophysical")


#num_inh = [int(lognormal(43, 13)) for i in range(N)]
num_inh = [1]

#num_exc = [int(lognormal(25, 10)) for i in range(N)]
num_exc = [1]

##################################################################################
###################################Pyr Type C#####################################

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


net.add_nodes(N=2, pop_name='Int',
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:basket',
        morphology=None)


##################################################################################
###################################External Networks##############################

#print("Internal nodes built")

print("making {} exc_stim nodes".format(np.sum(num_exc)))

# External excitatory inputs
tone = NetworkBuilder('tone')
tone.add_nodes(N=1,
                pop_name='tone',
                potential='exc',
                model_type='virtual')

print("making {} inh_stim nodes".format(np.sum(num_inh)))
# External inhibitory inputs
shock = NetworkBuilder('shock')
shock.add_nodes(N=1,
                pop_name='shock',
                potential='exc',
                model_type='virtual')

##################################################################################
###################################Edges##########################################

def one_to_one(source, target):
    
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
        print("connecting cell {} to {}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

def shock_connection(source,target):
    sid = source.node_id
    tid = target.node_id
    if(tid == 0 or tid == 3 or tid == 4 or tid == 6 or tid == 7 or tid == 8 or tid == 9):
        print("connecting shock cell {} to {}".format(sid,tid))
        tmp_nsyn=1
    else:
        return None
    return tmp_nsyn

def tone_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if(tid == 2 or tid == 4 or tid == 6 or tid == 7 or tid == 8 or tid == 9):
        print("connecting tone cell {} to {}".format(sid,tid))
        tmp_nsyn=1
    else:
        return None
    return tmp_nsyn

def get_node_ids(source, target):
    sid = source.node_id
    tid = target.node_id
    print("source and targets are {} and {}".format(sid,tid))
    return None

#idea for pyr_connection is that if its called it will always create a connection since all pyra cells are connected
def pyr_connection(source,target):
    sid = source.node_id
    tid = target.node_id
    print("connecting pyra cells {} and {}".format(sid,tid))
    return 1

def int_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    if(sid != tid):
        print("connecting int cell {} to {}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None
    return tmp_nsyn

#basically same as pyr connecting (always makes connection from source to target) only difference is print to make output easier to understand
def int_pyr_connection(source, target):
    sid = source.node_id
    tid = target.node_id
    print("connecting int cells {} to pyra cell {}".format(sid,tid))
    return 1

# Create connections between Shock --> Pyr cells
net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrA'),
                connection_rule=shock_connection,
                syn_weight=40.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='shock2PN.json',
                model_template=syn['shock2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrC'),
                connection_rule=shock_connection,
                syn_weight=40.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='shock2PN.json',
                model_template=syn['shock2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='Int'),
                connection_rule=shock_connection,
                syn_weight=20.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
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

net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='Int'),
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
                syn_weight=1.50,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PyrC'),
                connection_rule=pyr_connection,
                syn_weight=1.50,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrA'),
                connection_rule=pyr_connection,
                syn_weight=1.50,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrC'),
                connection_rule=pyr_connection,
                syn_weight=1.50,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])


#Create connections between Pyr --> Int cells
net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='Int'),
                connection_rule=pyr_connection,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToInh.json',
                model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='Int'),
                connection_rule=pyr_connection,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToInh.json',
                model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])

#Create connections Int --> Int cells

net.add_edges(source=net.nodes(pop_name='Int'), target=net.nodes(pop_name='Int'),
                connection_rule=int_connection,
                syn_weight=3.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='GABA_InhToInh.json',
                model_template=syn['GABA_InhToInh.json']['level_of_detail'])


#Create connections Int --> Pyr cells
net.add_edges(source=net.nodes(pop_name='Int'), target=net.nodes(pop_name='PyrA'),
                connection_rule=int_pyr_connection,
                syn_weight=5.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='GABA_InhToExc.json',
                model_template=syn['GABA_InhToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='Int'), target=net.nodes(pop_name='PyrC'),
                connection_rule=int_pyr_connection,
                syn_weight=5.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='GABA_InhToExc.json',
                model_template=syn['GABA_InhToExc.json']['level_of_detail'])

# Build and save our networks

net.build()
net.save_nodes(output_dir='network')
net.save_edges(output_dir='network')

tone.build()
tone.save_nodes(output_dir='network')

shock.build()
shock.save_nodes(output_dir='network')


from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
#from bmtk.utils.reports.spike_trains.spikes_file_writers import write_csv

tone_fr = 2
shock_fr = 2

exc_psg = PoissonSpikeGenerator(population='tone')
exc_psg.add(node_ids=0,
        firing_rate=int(tone_fr))
        #times=(200.0, 500.0))
exc_psg.to_sonata('tone_poisson_spikes.h5')

inh_psg = PoissonSpikeGenerator(population='shock')
inh_psg.add(node_ids=0,
        firing_rate=int(shock_fr))
        #times=(200.0, 1200.0))
inh_psg.to_sonata('shock_poisson_spikes.h5')

from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(base_dir='./',
                network_dir='./network',
                tstop=43000.0, dt = 0.1,
                report_vars=['v','cai'],
                spikes_inputs=[('tone', 'tone_spikes.csv'), ('shock', 'shock_spikes.csv')],
                components_dir='biophys_components',
                compile_mechanisms=False)
