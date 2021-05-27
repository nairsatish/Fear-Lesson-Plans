from bmtk.builder import NetworkBuilder
import numpy as np
import sys
import synapses


net = NetworkBuilder("biophysical")

net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:feng_typeA',
        morphology=None)


"""
net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:feng_typeC',
        morphology=None)
"""

"""
net.add_nodes(
        mem_potential='e',
        model_type='biophysical',
        model_template='hoc:basket',
        morphology=None)
"""

net.build()
net.save_nodes(output_dir='network')
from bmtk.utils.sim_setup import build_env_bionet
build_env_bionet(base_dir='./',
                network_dir='./network',
                tstop=800.0, dt = 0.1,
                report_vars=['v'],
                current_clamp={
                    'amp': 0.300,
                    'delay': 50.0,
                    'duration': 600 #200 for bask 600 for pyr
                },
                components_dir='biophys_components',
                compile_mechanisms=False)


from bmtk.simulator import bionet


config_file = 'simulation_config.json'
conf = bionet.Config.from_json(config_file, validate=True)
conf.build_env()
net = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=net)
sim.run()

from bmtk.analyzer.compartment import plot_traces
_ = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='v_report')