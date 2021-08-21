from bmtk.analyzer.compartment import plot_traces
from bmtk.analyzer.spike_trains import plot_raster, plot_rates_boxplot

_ = plot_raster(config_file='config.json', group_by='pop_name', title='raster')
_ = plot_rates_boxplot(config_file='config.json', group_by='pop_name', title='boxplot')
_ = plot_traces(config_file='config.json', node_ids=[7], report_name='v_report')

