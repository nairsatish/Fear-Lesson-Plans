from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot
import pandas as pd
import matplotlib.pyplot as plt
import numpy


_ = plot_raster(config_file='simulation_config_W+Cai.json', group_by='pop_name', title='raster')
#_ = plot_rates_boxplot(config_file='config.json', group_by='pop_name', title='boxplot')
_ = plot_traces(config_file='simulation_config_W+Cai.json', node_ids=[0], report_name='v_report')
#_ = plot_traces(config_file='simulation_config_W+Cai.json', node_ids=[2,4,6,7], report_name='v_report')