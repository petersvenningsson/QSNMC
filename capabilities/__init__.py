"""Capabilities corresponding to challenge A in the 2009 competition."""

import os
import numpy as np
import pickle

from sciunit import Capability

CHALLENGE = "2009a"
PATH = os.path.split(os.path.abspath(__file__))[0]
full_path = '%s/training/%s' % (PATH,CHALLENGE)

####################
# Old capabilities #
####################

from neuronunit.neuroconstruct.capabilities import ProducesSpikes_NC

####################
# New capabilities #
####################

class TrainVoltageOnCurrent(Capability):
    """
    The capability to observe a current and a set of voltages in response
    to that current, and then produce a new voltage in response to a 
    novel current.
    """

    def observe_current(current):
        """Should take a current and train the model."""
        raise NotImplementedError("")

    def observe_voltage(voltage):
        """Should take an array of voltage traces to go with the current."""
        raise NotImplementedError("")

#######################################
# Functions to implement capabilities #
#######################################

def get_full_path():
    full_path = '%s/training/%s' % (PATH,CHALLENGE)
    return full_path

def load_training_data(pickled=True):
    full_path = get_full_path()
    if pickled:
        current_pickle_path = '%s/current.pickle' % full_path
        voltage_pickle_path = '%s/voltage_allrep.pickle' % full_path
        if not (os.path.isfile(current_pickle_path) \
                and os.path.isfile(voltage_pickle_path)):
            print "Pickled data not found; pickling from raw data files..."
            pickle_training_data()
        print "Loading training data from pickled files..."
        with open(current_pickle_path) as f:
            current = pickle.load(f)
        with open(voltage_pickle_path) as f:
            voltage = pickle.load(f)
    else:
        print "Loading training data from raw data files..."
        current = np.loadtxt('%s/current.txt' % full_path)
        voltage = np.loadtxt('%s/voltage_allrep.txt' % full_path)
    return (current,voltage)

def pickle_training_data():
    full_path = get_full_path()
    current, voltage = load_training_data(pickled=False)
    current_pickle_path = '%s/current.pickle' % full_path
    voltage_pickle_path = '%s/voltage_allrep.pickle' % full_path
    with open(current_pickle_path,'w') as f:
        pickle.dump(current,f)
    with open(voltage_pickle_path,'w') as f:
        pickle.dump(voltage,f)
