from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import plot_raster
from bmtk.analyzer.spike_trains import plot_rates_boxplot
#_ = plot_traces(config_file='simulation_config.json', node_ids=[10,11], report_name='v_report',title="PV")
#_ = plot_traces(config_file='simulation_config.json', node_ids=[8,9], report_name='v_report', title='OLM')
#_ = plot_traces(config_file='simulation_config.json', node_ids=[0,1,2,3,4], report_name='v_report', title='PyrA')
#_ = plot_traces(config_file='simulation_config.json', node_ids=[5,6,7], report_name='v_report', title='pyrC')


_ = plot_traces(config_file='simulation_config.json', node_ids=[0], report_name='v_report', title='PV')
_ = plot_traces(config_file='simulation_config.json', node_ids=[1], report_name='v_report', title='OLM')
_ = plot_traces(config_file='simulation_config.json', node_ids=[2], report_name='v_report', title='PN')
_ = plot_rates_boxplot(config_file='simulation_config.json', group_by='pop_name')
#_ = plot_raster(config_file='simulation_config.json',group_by='pop_name')


