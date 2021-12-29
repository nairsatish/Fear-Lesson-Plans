import streamlit as st
from bmtk.analyzer.compartment import plot_traces
from bmtk.simulator import bionet
import glob
import json
from bmtk.simulator.bionet.pyfunction_cache import add_synapse_model
from neuron import h
from bmtk.builder import NetworkBuilder
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
import os
import shutil
import numpy as np
import random


def bg2PN(syn_params, sec_x, sec_id):
    lsyn = h.bg2pyr(sec_x, sec=sec_id)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
    return lsyn

def pyr2int(syn_params, sec_x, sec_id):
    """Create a pyr2int synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.pyr2intKIM(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params['initW'])
        # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    if syn_params.get('bACH'):
        lsyn.bACH = float(syn_params['bACH'])  # par.x(17)
    if syn_params.get('aDA'):
        lsyn.aDA = float(syn_params['aDA'])  # par.x(18)
    if syn_params.get('bDA'):
        lsyn.bDA = float(syn_params['bDA'])  # par.x(19)
    if syn_params.get('wACH'):
        lsyn.wACH = float(syn_params['wACH'])  # par.x(20)

    return lsyn

def int2pyr(syn_params, sec_x, sec_id):
    """Create a int2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.int2pyrKIM(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params[
                               'initW'])  # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    return lsyn

def Shock2Pyr(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.shock2pyr(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params[
                               'initW'])  # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    if syn_params.get('bACH'):
        lsyn.bACH = float(syn_params['bACH'])  # par.x(17)
    if syn_params.get('aDA'):
        lsyn.aDA = float(syn_params['aDA'])  # par.x(18)
    if syn_params.get('bDA'):
        lsyn.bDA = float(syn_params['bDA'])  # par.x(19)
    if syn_params.get('wACH'):
        lsyn.wACH = float(syn_params['wACH'])  # par.x(20)

    return lsyn

def Tone2Pyr(syn_params, sec_x, sec_id):
    """Create a tone2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """
    lsyn = h.tone2pyr(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params[
                               'initW'])  # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    if syn_params.get('bACH'):
        lsyn.bACH = float(syn_params['bACH'])  # par.x(17)
    if syn_params.get('aDA'):
        lsyn.aDA = float(syn_params['aDA'])  # par.x(18)
    if syn_params.get('bDA'):
        lsyn.bDA = float(syn_params['bDA'])  # par.x(19)
    if syn_params.get('wACH'):
        lsyn.wACH = float(syn_params['wACH'])  # par.x(20)

    return lsyn

def Shock2Int(syn_params, sec_x, sec_id):
    """Create a int2pyr synapse
    :param syn_params: parameters of a synapse
    :param sec_x: normalized distance along the section
    :param sec_id: target section
    :return: NEURON synapse object
    """

    lsyn = h.shock2int(sec_x, sec=sec_id)

    if syn_params.get('AlphaTmax_ampa'):
        lsyn.AlphaTmax_ampa = float(syn_params['AlphaTmax_ampa'])  # par.x(21)
    if syn_params.get('Beta_ampa'):
        lsyn.Beta_ampa = float(syn_params['Beta_ampa'])  # par.x(22)
    if syn_params.get('Cdur_ampa'):
        lsyn.Cdur_ampa = float(syn_params['Cdur_ampa'])  # par.x(23)
    if syn_params.get('gbar_ampa'):
        lsyn.gbar_ampa = float(syn_params['gbar_ampa'])  # par.x(24)
    if syn_params.get('Erev_ampa'):
        lsyn.Erev_ampa = float(syn_params['Erev_ampa'])  # par.x(16)

    if syn_params.get('AlphaTmax_nmda'):
        lsyn.AlphaTmax_nmda = float(syn_params['AlphaTmax_nmda'])  # par.x(25)
    if syn_params.get('Beta_nmda'):
        lsyn.Beta_nmda = float(syn_params['Beta_nmda'])  # par.x(26)
    if syn_params.get('Cdur_nmda'):
        lsyn.Cdur_nmda = float(syn_params['Cdur_nmda'])  # par.x(27)
    if syn_params.get('gbar_nmda'):
        lsyn.gbar_nmda = float(syn_params['gbar_nmda'])  # par.x(28)
    if syn_params.get('Erev_nmda'):
        lsyn.Erev_nmda = float(syn_params['Erev_nmda'])  # par.x(16)

    if syn_params.get('initW'):
        lsyn.initW = float(syn_params[
                               'initW'])  # * random.uniform(0.5,1.0) # par.x(0) * rC.uniform(0.5,1.0)//rand.normal(0.5,1.5) //`rand.repick()

    if syn_params.get('Wmax'):
        lsyn.Wmax = float(syn_params['Wmax']) * lsyn.initW  # par.x(1) * lsyn.initW
    if syn_params.get('Wmin'):
        lsyn.Wmin = float(syn_params['Wmin']) * lsyn.initW  # par.x(2) * lsyn.initW
    # delay = float(syn_params['initW']) # par.x(3) + delayDistance
    # lcon = new NetCon(&v(0.5), lsyn, 0, delay, 1)

    if syn_params.get('lambda1'):
        lsyn.lambda1 = float(syn_params['lambda1'])  # par.x(6)
    if syn_params.get('lambda2'):
        lsyn.lambda2 = float(syn_params['lambda2'])  # par.x(7)
    if syn_params.get('threshold1'):
        lsyn.threshold1 = float(syn_params['threshold1'])  # par.x(8)
    if syn_params.get('threshold2'):
        lsyn.threshold2 = float(syn_params['threshold2'])  # par.x(9)
    if syn_params.get('tauD1'):
        lsyn.tauD1 = float(syn_params['tauD1'])  # par.x(10)
    if syn_params.get('d1'):
        lsyn.d1 = float(syn_params['d1'])  # par.x(11)
    if syn_params.get('tauD2'):
        lsyn.tauD2 = float(syn_params['tauD2'])  # par.x(12)
    if syn_params.get('d2'):
        lsyn.d2 = float(syn_params['d2'])  # par.x(13)
    if syn_params.get('tauF'):
        lsyn.tauF = float(syn_params['tauF'])  # par.x(14)
    if syn_params.get('f'):
        lsyn.f = float(syn_params['f'])  # par.x(15)

    return lsyn

def load():
    add_synapse_model(bg2PN, 'bg2pn', overwrite=False)
    add_synapse_model(bg2PN, overwrite=False)

    add_synapse_model(Tone2Pyr, 'tone2pyr', overwrite=False)
    add_synapse_model(Tone2Pyr, overwrite=False)

    add_synapse_model(Shock2Pyr, 'shock2pyr', overwrite=False)
    add_synapse_model(Shock2Pyr, overwrite=False)

    add_synapse_model(Shock2Int, 'shock2int', overwrite=False)
    add_synapse_model(Shock2Int, overwrite=False)

    add_synapse_model(pyr2int, 'pyr2int', overwrite=False)
    add_synapse_model(pyr2int, overwrite=False)

    add_synapse_model(int2pyr, 'int2pyr', overwrite=False)
    add_synapse_model(int2pyr, overwrite=False)
    return

def syn_params_dicts(syn_dir='biophys_components/synaptic_models'):
    """
    returns: A dictionary of dictionaries containing all
    properties in the synapse json files
    """
    files = glob.glob(os.path.join(syn_dir, '*.json'))
    data = {}
    for fh in files:
        with open(fh) as f:
            data[os.path.basename(fh)] = json.load(f)  # data["filename.json"] = {"prop1":"val1",...}
    return data

def build_model():
    if os.path.isdir('network'):
        shutil.rmtree('network')
    if os.path.isdir('2_cell_inputs'):
        shutil.rmtree('2_cell_inputs')

    seed = 967
    random.seed(seed)
    np.random.seed(seed)
    load()
    syn = syn_params_dicts()

    # Initialize our network

    net = NetworkBuilder("biophysical")

    num_inh = [1]

    num_exc = [1]

    ##################################################################################
    ###################################BIOPHY#########################################

    # PN
    net.add_nodes(N=1, pop_name='PyrC',
                  mem_potential='e',
                  model_type='biophysical',
                  model_template='hoc:Cell_C',
                  morphology=None)

    # PV
    net.add_nodes(N=1, pop_name="PV",
                  mem_potential='e',
                  model_type='biophysical',
                  model_template='hoc:basket',
                  morphology=None
                  )

    backgroundPN_C = NetworkBuilder('bg_pn_c')
    backgroundPN_C.add_nodes(N=1,
                             pop_name='tON',
                             potential='exc',
                             model_type='virtual')

    backgroundPV = NetworkBuilder('bg_pv')
    backgroundPV.add_nodes(N=2,
                           pop_name='tON',
                           potential='exc',
                           model_type='virtual')

    # if neuron is sufficiently depolorized enough post synaptic calcium then synaptiic weight goes up

    # pyr->pyr & pyr->PV
    # PV->pyr PV->PV
    def one_to_all(source, target):
        sid = source.node_id
        tid = target.node_id
        print("connecting bio cell {} to bio cell {}".format(sid, tid))
        return 1

    def BG_to_PN_C(source, target):
        sid = source.node_id
        tid = target.node_id
        if sid == tid:
            print("connecting BG {} to PN_C{}".format(sid, tid))
            return 1
        else:
            return 0

    def BG_to_PV(source, target):
        sid = source.node_id
        tid = target.node_id
        sid = sid + 1
        if sid == tid:
            print("connecting BG {} to PV{}".format(sid, tid))
            return 1
        else:
            return 0

    conn = net.add_edges(source=net.nodes(pop_name='PyrC'), target=net.nodes(pop_name="PV"),
                         connection_rule=one_to_all,
                         syn_weight=1.0,
                         delay=0.1,
                         distance_range=[-10000, 10000],
                         dynamics_params='PN2PV.json',
                         model_template=syn['PN2PV.json']['level_of_detail'])
    conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

    conn = net.add_edges(source=net.nodes(pop_name='PV'), target=net.nodes(pop_name="PyrC"),
                         connection_rule=one_to_all,
                         syn_weight=1.0,
                         delay=0.1,
                         distance_range=[-10000, 10000],
                         dynamics_params='PV2PN.json',
                         model_template=syn['PV2PN.json']['level_of_detail'])
    conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

    conn = net.add_edges(source=backgroundPN_C.nodes(), target=net.nodes(pop_name='PyrC'),
                         connection_rule=BG_to_PN_C,
                         syn_weight=1.0,
                         delay=0.1,
                         distance_range=[-10000, 10000],
                         dynamics_params='BG2PNC.json',
                         model_template=syn['BG2PNC.json']['level_of_detail'])
    conn.add_properties(['sec_id', 'sec_x'], rule=(2, 0.9), dtypes=[np.int32, np.float])  # places syn on apic at 0.9

    conn = net.add_edges(source=backgroundPV.nodes(), target=net.nodes(pop_name='PV'),
                         connection_rule=BG_to_PV,
                         syn_weight=1.0,
                         delay=0.1,
                         distance_range=[-10000, 10000],
                         dynamics_params='BG2PV.json',
                         model_template=syn['BG2PV.json']['level_of_detail'])
    conn.add_properties(['sec_id', 'sec_x'], rule=(1, 0.9), dtypes=[np.int32, np.float])

    backgroundPN_C.build()
    backgroundPN_C.save_nodes(output_dir='network')

    backgroundPV.build()
    backgroundPV.save_nodes(output_dir='network')

    net.build()
    net.save(output_dir='network')
    # SPIKE TRAINS
    t_sim = 40000

    # build_env_bionet(base_dir='./',
    #                 network_dir='./network',
    #                 tstop=t_sim, dt=0.1,
    #                 report_vars=['v'],
    #                 components_dir='biophys_components',
    #                 config_file='config.json',
    #                 spikes_inputs=[('bg_pn_c', '2_cell_inputs/bg_pn_c_spikes.h5'),
    #                                ('bg_pv', '2_cell_inputs/bg_pv_spikes.h5')],
    #                 compile_mechanisms=False)

    psg = PoissonSpikeGenerator(population='bg_pn_c')
    psg.add(node_ids=range(1),  # need same number as cells
            firing_rate=6,  # 1 spike every 1 second Hz
            times=(0.0, t_sim / 1000))  # time is in seconds for some reason
    psg.to_sonata('2_cell_inputs/bg_pn_c_spikes.h5')

    print('Number of background spikes for PN_C: {}'.format(psg.n_spikes()))

    psg = PoissonSpikeGenerator(population='bg_pv')
    psg.add(node_ids=range(1),  # need same number as cells
            firing_rate=7.7,  # 8 spikes every 1 second Hz
            times=(0.0, t_sim / 1000))  # time is in seconds for some reason
    psg.to_sonata('2_cell_inputs/bg_pv_spikes.h5')

    print('Number of background spikes for PV: {}'.format(psg.n_spikes()))

def run(config_file):
    load()
    h.nrnmpi_init()
    pc = h.ParallelContext()  # object to access MPI methods
    MPI_size = int(pc.nhost())
    MPI_rank = int(pc.id())

    config_file = 'config.json'

    conf = bionet.Config.from_json(config_file, validate=True)
    conf.build_env()

    graph = bionet.BioNetwork.from_config(conf)
    sim = bionet.BioSimulator.from_config(conf, network=graph)

    cells = graph.get_local_cells()

    sim.run()

    pc.barrier()
    pc.gid_clear()
    pc.done()


st.write("""
# Simple 1 cell model
""")

if st.button("build model"):
    path = os.getcwd()
    path = os.path.basename(path)
    #st.write(path)
    if (path!="streamlit"):
        os.chdir("streamlit")
    if os.path.isdir('biophys_components/mechanisms/x86_64'):
        shutil.rmtree('biophys_components/mechanisms/x86_64')
    os.chdir('biophys_components/mechanisms')
    os.system('nrnivmodl modfiles')
    os.chdir("../..")
    st.write("Building model")
    build_model()
    st.write("Done building")

bg_pn = st.slider('Generate PN background')
if st.button("Push to Generate"):
    os.remove('2_cell_inputs/bg_pn_c_spikes.h5')
    psg = PoissonSpikeGenerator(population='bg_pn_c')
    psg.add(node_ids=range(1),  # need same number as cells
            firing_rate=bg_pn,  # 1 spike every 1 second Hz
            times=(0.0, 40000 / 1000))  # time is in seconds for some reason
    psg.to_sonata('2_cell_inputs/bg_pn_c_spikes.h5')
    st.write('Generated background of PN at : {} Hz'.format(bg_pn))

if st.button("Push to run model"):
    st.write("running model")
    run(config_file='config.json')
    st.write("done running")

if st.button("Plot results"):
    _ = plot_traces(config_file='config.json', node_ids=[0], report_name='v_report', show=False, title="PN")
    st.pyplot(_)

