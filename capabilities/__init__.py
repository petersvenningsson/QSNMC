"""Capabilities corresponding to challenge A in the 2009 competition."""

from sciunit import Capability

CHALLENGE = "2009a"

################
# Capabilities #
################

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

def load_training_data():
    current = np.loadtxt('../capabilities/training/%s/current.txt' % CHALLENGE)
    voltage = np.loadtxt('../capabilities/training/%s/voltage_allrep.txt' % CHALLENGE)
    return (current,voltage)

