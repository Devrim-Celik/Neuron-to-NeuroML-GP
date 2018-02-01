import numpy as np
import pickle

def generate_sigmoidal_properties(nr_steps=500):
    final_dict = {}

    # setups for changing midpoint
    # setups: (rate(constant), midpoint_start, midpoint_end, scale(constant))
    mid_setups = [(1, -100, 40, 3), (1, -100, 40, 7), \
        (-1, -100, 40, 3), (-1, -100, 40, 7)]

    # setups for changing scale
    # setups: (rate(constant), midpoint(constant), scale_start, scale_end)
    scale_setups = [(1, -60, 1, 20), (1, -30, 1, 20), \
        (-1, -60, 1, 20), (-1, -30, 1, 20)]

    # midpoint setups
    for i, setup in enumerate(mid_setups):
        single_dict = {}
        single_dict["setup"] = setup
        single_dict["description"] = "Rate({}), Midpoint([({})-({})]), Scale({})".format(setup[0], setup[1], setup[2], setup[3])
        single_dict["trace"] = sigmoid_fun_mid(setup[0], setup[1], setup[2], setup[3], nr_steps)
        final_dict["Setup{}".format(i+1)] = single_dict
    # scale setups
    for i, setup in enumerate(scale_setups):
        single_dict = {}
        single_dict["setup"] = setup
        single_dict["description"] = "Rate({}), Midpoint(({})), Scale([({})-({})])".format(setup[0], setup[1], setup[2], setup[3])
        single_dict["trace"] = sigmoid_fun_sca(setup[0], setup[1], setup[2], setup[3], nr_steps)
        final_dict["Setup{}".format(i+1+len(scale_setups))] = single_dict


    with open('./data/generated_lines.pickle', 'wb') as fp:
        pickle.dump(final_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)



def sigmoid_fun_mid(rate, m_s, m_e, scale, nr_steps):
    if (rate == -1):
        b = 1
    else:
        b = 0

    # interate over voltage and midpoint
    voltage = np.arange(-150, 151, 5)
    steps = np.arange(m_s, m_e, abs(m_e-m_s)/nr_steps)

    # for saving values
    trace = np.zeros((len(steps),len(voltage)))

    # calculate values
    for i,midpoint in enumerate(steps):
        for j,V in enumerate(voltage):
            trace[i,j] = rate / (1 + np.exp( -(V - midpoint)/scale)) + b

    return trace


def sigmoid_fun_sca(rate, midpoint, s_s, s_e, nr_steps):
    if (rate == -1):
        b = 1
    else:
        b = 0

    # interate over voltage and scale
    voltage = np.arange(-150, 151, 5)
    steps = np.arange(s_s, s_e, abs(s_e-s_s)/nr_steps)

    # for saving values
    trace = np.zeros((len(steps),len(voltage)))

    # calculate values
    for i,scale in enumerate(steps):
        for j,V in enumerate(voltage):
            trace[i,j] = rate / (1 + np.exp( -(V - midpoint)/scale)) + b

    return trace



if (__name__=="__main__"):
    generate_sigmoidal_properties()
