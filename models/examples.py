from __future__ import division

import sciunit
import numpy as np
from neuronunit.capabilities import ProducesSpikes
from NeuroTools.signals import AnalogSignal

TMAX = 39.0 # Figure out where this should get passed.  

class LIFModel(sciunit.Model,ProducesSpikes):
    """
    Simple leaky integrate-and-fire model for testing.
    dV_m/dt = I/C 
    = (I_m+I_injected)/C 
    = (g_leak*(V_rest - V_m) + I_injected)/C
    """

    def __init__(self,C,v_rest,g_leak,v_thresh,v_reset,v_spike=30.0,**kwargs):
        self.C = C # Capacitance
        self.v_rest = v_rest # Resting membrane potential  
        self.g_leak = g_leak # Leak conductance
        self.v_thresh = v_thresh # Leak conductance
        self.v_reset = v_reset
        self.v_spike = v_spike
        super(LIFModel,self).__init__(**kwargs)
    
    def set_external_current(self,current):
        assert type(current) is AnalogSignal, \
            "Current should be a NeuroTools AnalogSignal, not a %s" % type(current)
        print("Simulating current injection...")
        self.i_ext = current.signal
        self.dt = current.dt
        self.steps = len(self.i_ext)

    def integrate(self, T_max=None):
        if T_max is None:
            steps = self.steps
        else:
            steps = int(T_max / self.dt)
        self.v_m = np.zeros(steps)
        self.v_m[0] = self.v_rest
        for t in range(1,steps):
            i_ext = self.i_ext[t-1]
            v_m = self.v_m[t-1]
            if v_m == self.v_spike:
                v_m = self.v_reset
            dV = self.dVdt(v_m,i_ext) * self.dt
            if t > 0:
                v_m += dV
            if v_m > self.v_thresh:
                v_m = self.v_spike # AP height.  
            self.v_m[t] = v_m

    def dVdt(self,v,i_ext):
        g_leak, v_rest, C = self.g_leak, self.v_rest, self.C
        dVdt = (g_leak * (v_rest - v) + i_ext) / C
        #print i_ext,v,dVdt
        return dVdt

    def get_spike_trains(self,current=None):
        spike_trains = []
        for trial in range(5):
            if current:
                self.set_external_current(current)
            self.integrate(T_max = TMAX)
            voltage_trial = self.v_m
            vm_trial = AnalogSignal(voltage_trial,self.dt)  
            spike_train = vm_trial.threshold_detection(0)
            spike_trains.append(spike_train)
            if len(spike_trains) >= 3: # Don't use all the spike trains.  
                break
        return spike_trains

# Parameters to instantiate a model.  
C = 1.0
v_rest = -65.0
g_leak = 1.0
v_thresh = -45.0
v_reset = -70.0

model1 = LIFModel(C,v_rest,g_leak,v_thresh,v_reset,name='Example')

models = [model1,]