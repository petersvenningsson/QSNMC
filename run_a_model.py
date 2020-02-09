###########
# IMPORTS #
###########
# 3rd party
import matplotlib.pyplot as plt

from QSNMC.tests import tests
from QSNMC.models import models
print(tests)
print(models)

for model in models:
    print("Model: %s" % model)
    for test in tests:
        print("Test: %s" % test)
        score = test.judge(model,deep_error=True)
        score.summarize()
        print("\r")
model = models[0]

v = model.v
u = model.u
I = model.i_ext
dt = model.dt

time = [dt*x for x in range(0,len(I))]


def plot_input_output(time, v, I, title:str, filename:str):
    """ beautification of results.
    """
    # Initialize
    fig, ax1 = plt.subplots(figsize=(12, 3))
    ax1.plot(time, v, 'tab:blue', label='Output', alpha = 0.4)
    ax1.set_xlabel('time (ms)')
    fig.suptitle(title, fontsize=8)

    # Plot output
    ax1.set_ylabel('Output mV', color='tab:blue')
    ax1.tick_params('y', colors='tab:blue')
    ax1.set_ylim(-150, 55)
    ax2 = ax1.twinx()

    # Plot input current
    ax2.plot(time, I, 'tab:red', label='Input', alpha = 0.4)
    ax2.set_ylim(-2500, 2500)
    ax2.set_ylabel('Input (mV)', color='tab:red')
    ax2.tick_params('y', colors='tab:red')

    fig.tight_layout()
    ax1.legend(loc=1)
    ax2.legend(loc=3)
    plt.savefig(filename+'.jpg')

# Plot measured data
plot_input_output(time, test.observation['gold_voltages'][0],I, "measured data", 'measured_voltage')

#Plot model performance
plot_input_output(time, v,I, "The score achieved is " + score.raw, 'summary_of_model_results')
