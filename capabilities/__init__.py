"""Capabilities corresponding to challenge A in the 2009 competition."""

import os
import numpy as np
import pickle

from sciunit import Capability

CHALLENGE = "2009a"
PATH = os.path.split(os.path.abspath(__file__))[0]

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

def load_training_data(pickled=True):
    full_path = '%s/training/%s' % (PATH,CHALLENGE)
    if pickled:
        with open('%s/current.pickle' % full_path) as f:
            current = pickle.load(f)
        with open('%s/voltage_allrep.pickle' % full_path) as f:
            voltage = pickle.load(f)
    else:
        current = np.loadtxt('%s/current.txt' % full_path)
        voltage = np.loadtxt('%s/voltage_allrep.txt' % full_path)
    return (current,voltage)

