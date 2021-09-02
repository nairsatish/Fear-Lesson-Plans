import h5py
import pandas
import numpy
import matplotlib.pyplot as plt
from bmtk.analyzer.compartment import plot_traces

_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_tone2pyr.h5', title='tone2pyr')
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2int.h5', title='pyr2int')
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2pyr.h5', title='pyr2pyr')
_ = plot_traces(config_file='simulation_configWEIGHTS.json', report_path='output/syns_pyr2int.h5', title='pyr2int')

