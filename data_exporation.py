from QSNMC import capabilities
from NeuroTools.signals import AnalogSignal

#############
# CONSTANTS #
#############
dt = 1e-4 # 10 kHz sampling.

current_array, voltage_array = capabilities.load_training_data(pickled=True)

spike_trains = []

for col in range(voltage_array.shape[1]):
    voltage_trial = voltage_array[:, col]
    vm_trial = AnalogSignal(voltage_trial, dt)
    spike_train = vm_trial.threshold_detection(0)
    spike_trains.append(spike_train)

current = AnalogSignal(current_array, dt)
observation = {'current': current, 'spike_trains': spike_trains}

print("")