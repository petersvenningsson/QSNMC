
###########
# IMPORTS #
###########

# Third party
import sciunit
import numpy as np
from neuronunit.capabilities import ProducesSpikes
from NeuroTools.signals import AnalogSignal
import matplotlib.pyplot as plt


#############
# CONSTANTS #
#############
TMAX = 39.0
a = 0.02
b = 0.2
c = -65
d = 8

class IZModel(sciunit.Model, ProducesSpikes):
    """
    Model of a Izhikevich neuron. Extends sciunit.Model and ProducesSpikes.
    """

    def __init__(self, a, b, c, d, v_spike=30.0, **kwargs):
        self.a = a  # Recovery parameter for variable u. Low a provides long recovery.
        self.b = b  # Sensativity of u to subthreshhold dynamics of v.
        self.c = c  # Reset value of potential v after action potential spike.
        self.d = d  # Reset value of potential u after action potential spike.
        self.v_spike = v_spike
        self.u = None # Initialized in simulate method.
        self.v = None # Initialized in simulate method.
        self.dt = None # Initialized by set_external_current method.
        self.i_ext = None # Initialized by set_external_current method.
        self.dt = None # Initialized by set_external_current method.
        self.steps = None # Initialized by set_external_current method.

        super().__init__(**kwargs)

    def set_external_current(self, current):
        """ Parsing function for the NeuroTools AnalogSignal type object current.
        """
        assert type(current) is AnalogSignal, \
            "Current should be a NeuroTools AnalogSignal, not a %s" % type(current)
        print("Simulating current injection...")

        self.i_ext = current.signal
        self.dt = current.dt
        self.steps = len(self.i_ext)

    def euler_forward(self, u, v, I):
        """ Calculates one Euler step for the Izhikevich neuron.
        Inputs:
            v - the current voltage
            u - the current recovery
        Returns:
            _v - the proceeding voltage
            _u - the proceeding recovery
            """
        _v = v + self.dt * (0.04 * v ** 2 + 5 * v + 140 - u + I)
        _u = u + self.dt * (self.a * (self.b * v - u))
        return _v, _u

    def simulate(self, T_max=None):
        """ Simulates the pulse train of the Izhikevich neuron by setting self.v_model.
        Inputs:
            T_max - Maximum simulation time in ms
        Outputs:
        """
        if T_max is None:
            steps = self.steps
        else:
            steps = int(T_max / self.dt)

        # Initialize variables
        self.u = np.zeros(steps)
        self.v = -65*np.ones(steps)

        # Initial conditions
        self.u[0]=self.b*self.v[0]

        # Given initial conditions and Izhikevich neuron parameters approximate a solution for v(t).
        for t in range(1, steps):
            i_ext = self.i_ext[t - 1]
            v_iteration = self.v[t - 1]
            u_iteration = self.u[t - 1]

            if v_iteration > self.v_spike:
                v_iteration = self.c
                u_iteration = u_iteration + self.d

            v_iteration_next, u_iteration_next = self.euler_forward(u_iteration, v_iteration, i_ext)

            self.v[t] = v_iteration_next
            self.u[t] = u_iteration_next

        #### Temporary graphing code ###
        x = [_x * self.dt for _x in range(0, len(self.v))]
        plt.plot(x, self.v)
        plt.savefig('predicted_voltage.jpg')


    def get_spike_trains(self, current=None):
        """ Calculates the spike train produced by the external current.
        Inputs:
            current - AnalogSignal type instance describing the external current.
        Outputs:

        """

        # For compability with sciunit as many spike trains are generated as there exists ground truth observations
        spike_trains = []
        for trial in range(13):
            if current:
                self.set_external_current(current)
            self.simulate(T_max=TMAX)
            voltage_trial = self.v
            vm_trial = AnalogSignal(voltage_trial, self.dt)
            spike_train = vm_trial.threshold_detection(0)
            spike_trains.append(spike_train)
            if len(spike_trains) >= 13:  # Don't use all the spike trains.
                break
        return spike_trains



# Instantiate a model.

iz_model = IZModel(a,b,c,d, name='Izhikevich')