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
tone.add_nodes(N=np.sum(num_exc),
                pop_name='tone',
                potential='exc',
                model_type='virtual')

print("making {} inh_stim nodes".format(np.sum(num_inh)))
# External inhibitory inputs
shock = NetworkBuilder('shock')
shock.add_nodes(N=np.sum(num_inh),
                pop_name='shock',
                potential='exc',
                model_type='virtual')

##################################################################################
###################################Edges##########################################

def one_to_one(source, target):
    
    sid = source.node_id
    tid = target.node_id
    if sid == tid:
    #print("connecting cell {} to {}".format(sid,tid))
        tmp_nsyn = 1
    else:
        return None

    return tmp_nsyn

# Create connections between Shock --> Pyr cells
net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrA'),
                connection_rule=3,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='shock2PN.json',
                model_template=syn['shock2PN.json']['level_of_detail'])
                
net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='PyrC'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='shock2PN.json',
                model_template=syn['shock2PN.json']['level_of_detail'])

net.add_edges(source=shock.nodes(), target=net.nodes(pop_name='Int'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='shock2INT.json',
                model_template=syn['shock2INT.json']['level_of_detail'])

# Create connections between Tone --> Pyr cells
net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PyrA'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0, 11.0],
                dynamics_params='tone2PN.json',
                model_template=syn['tone2PN.json']['level_of_detail'])
                
net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='PyrC'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0, 11.0],
                dynamics_params='tone2PN.json',
                model_template=syn['tone2PN.json']['level_of_detail'])
                
net.add_edges(source=tone.nodes(), target=net.nodes(pop_name='Int'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0, 11.0],
                dynamics_params='tone2INT.json',
                model_template=syn['tone2INT.json']['level_of_detail'])

# Create connections between Pyr --> Pyr cells
net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PyrA'),
                connection_rule=20,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='PyrC'),
                connection_rule=15,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrA'),
                connection_rule=15,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='PyrC'),
                connection_rule=6,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToExc.json',
                model_template=syn['AMPA_ExcToExc.json']['level_of_detail'])


#Create connections between Pyr --> Int cells
net.add_edges(source=net.nodes(pop_name='PyrA'), target=net.nodes(pop_name='Int'),
                connection_rule=10,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToInh.json',
                model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name='Int'),
                connection_rule=6,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='AMPA_ExcToInh.json',
                model_template=syn['AMPA_ExcToInh.json']['level_of_detail'])

#Create connections Int --> Int cells

net.add_edges(source=net.nodes(pop_name='Int'), target=net.nodes(pop_name='Int'),
                connection_rule=2,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='GABA_InhToInh.json',
                model_template=syn['GABA_InhToInh.json']['level_of_detail'])
                

#Create connections Int --> Pyr cells
net.add_edges(source=net.nodes(pop_name='Inta'), target=net.nodes(pop_name='PyrA'),
                connection_rule=10,
                syn_weight=1.0,
                target_sections=['somatic'],
                delay=0.1,
                distance_range=[10.0,11.0],
                dynamics_params='GABA_InhToExc.json',
                model_template=syn['GABA_InhToExc.json']['level_of_detail'])

net.add_edges(source=net.nodes(pop_name='Int'), target=net.nodes(pop_name='PyrC'),
                connection_rule=6,
                syn_weight=1.0,
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


#from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
#from bmtk.utils.reports.spike_trains.spikes_file_writers import write_csv

#exc_psg = PoissonSpikeGenerator(population='exc_stim')
#exc_psg.add(node_ids=range(np.sum(num_exc)),  
#        firing_rate=int(exc_fr) / 1000,    
#        times=(200.0, 500.0))    
#exc_psg.to_sonata('exc_stim_spikes.h5')

#inh_psg = PoissonSpikeGenerator(population='inh_stim')
#inh_psg.add(node_ids=range(np.sum(num_inh)), 
#        firing_rate=int(inh_fr) / 1000,  
#        times=(200.0, 1200.0))   
#inh_psg.to_sonata('inh_stim_spikes.h5')

from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(base_dir='./',
                network_dir='./network',
                tstop=4000.0, dt = 0.1,
                report_vars=['v','cai'],
                spikes_inputs=[('tone', 'tone_spikes.csv'), ('shock', 'shock_spikes.csv')],
                components_dir='biophys_components',
                compile_mechanisms=False)
