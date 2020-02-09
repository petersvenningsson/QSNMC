import numpy as np
import matplotlib.pyplot as plt
from NeuroTools.signals import AnalogSignal

##########
# SCRIPT #
##########
# Reproduces some results from Simple Model of Spiking Neurons E. Izhikevich
# with the aim to verify the calculated model.
from QSNMC.models import iz

IZ_model = iz

#### Model Input
dt = 0.5
input_onset = 300             # Onset of input
input_amp = 5                 # AMPLITUDE OF INPUT


time = np.arange(0,1000.1,dt)  # time period 1000ms (1s)

def Input(input_onset,input_amp):
    I=np.zeros((len(time)))     # CURRENT (INPUT)

    for k in range (0,len(time)):
        if time[k] >input_onset:
            I[k]=input_amp # Input change
    return I

I = Input(input_onset, input_amp)
plt.plot(time,I)
plt.savefig('input_current_izen.jpg')

current = AnalogSignal(I, dt)
IZ_model.set_external_current(current)
IZ_model.simulate()


def plot_input_output(time, v, I):
    # PLOTTING
    fig, ax1 = plt.subplots(figsize=(12, 3))
    ax1.plot(time, v, 'b-', label='Output')
    ax1.set_xlabel('time (ms)')
    # Make the y-axis label, ticks and tick labels match the line color.
    # Plotting out put
    ax1.set_ylabel('Output mV', color='b')
    ax1.tick_params('y', colors='b')
    ax1.set_ylim(-95, 40)
    ax2 = ax1.twinx()
    # Plotting input on a different axis
    ax2.plot(time, I, 'r', label='Input')
    ax2.set_ylim(0, 2000 * 20)
    ax2.set_ylabel('Input (mV)', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    ax1.legend(loc=1)
    ax2.legend(loc=3)
    plt.savefig('output_voltage_izen.jpg')


#plot_input_output(time, IZ_model.v, I)

print("s")