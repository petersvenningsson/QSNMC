import sciunit
from neuronunit.capabilities import ProducesSpikes
from NeuroTools.signals import AnalogSignal

import QSNMC.tests as tests
from QSNMC.capabilities import load_training_data

CURRENT,VOLTAGE = load_training_data() 

class SimpleModel(sciunit.Model,ProducesSpikes):
    def inject_current(self,current):
        assert type(current) is AnalogSignal
        print "Simulating current injection."
        
    def get_spike_trains(self):
        spike_trains = []
        for col in range(VOLTAGE.shape[1]):
            voltage_trial = VOLTAGE[:,col]
            vm_trial = AnalogSignal(voltage_trial,1e-4) # 10 kHz sampling.  
            spike_train = vm_trial.threshold_detection(0)
            spike_trains.append(spike_train)
            if len(spike_trains) > 2: # Don't use all the spike trains.  
                break
        return spike_trains

test = tests.tests[0]
model = SimpleModel()
score = test.judge(model)
score.summarize()