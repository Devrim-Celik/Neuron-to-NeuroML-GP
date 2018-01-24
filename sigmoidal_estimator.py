import numpy as np
import matplotlib.pyplot as plt
import pandas
from auxiliary import unpack

class Sigmoidal_Estimator():

    def __init__(self, name, group, trace):
        self.name = name
        self.group = group
        self.trace = trace

        self.b = 0 # notfall, fall ich hoch oder runter muss

        self.V = np.arange(-150, 151, 5)


    # master function
    def routine(self):
        # added bias for negative function
        b_dict = {"PS": 0, "NS": 1}
        self.b = b_dict[self.group]
        # calculate parameters
        self.rate_est()
        self.midpoint_est()
        self.scale_est()
        # plotting
        #self.plot()

        if (self.rmse > 2):
            print("[!] Model({}) has RMSE of {}, please check!".format(self.name, self.rmse))

        return self.rate, self.midpoint, self.scale


    # calculate rate variable
    def rate_est(self):
        # check for "squishness"
        max_val = np.max(self.trace)
        min_val = np.min(self.trace)
        # positive or negative
        sign_dict = {"PS": 1, "NS": -1}

        self.rate = sign_dict[self.group]*(max_val-min_val)


    # calculate midpoint variable
    def midpoint_est(self):
        max_val = np.max(self.trace)
        min_val = np.min(self.trace)

        midpoint_value = (max_val-min_val)/2

        # find corresponding voltage value
        idx = (np.abs(self.trace-midpoint_value)).argmin()
        self.midpoint = self.V[idx]


    # calculate scale variable by testing different value of scale
    def scale_est(self):
        # scale, rmse
        minimum = [1, 1000]

        # iterate, try
        for scale in range(1, 50):
            self.scale = scale
            self.RMSE()
            # in case rmse is smaller
            if self.rmse < minimum[1]:
                minimum = scale, self.rmse
        self.scale = minimum[0]



    # plot against simulation
    def plot(self):

        self.RMSE()
        translated = self.calculate_values()

        plt.figure(figsize=(20,10))
        plt.title(self.name+ "\nRMSE = " + str(self.rmse) + " Group: " + self.group)
        plt.plot(self.V, self.trace, label="Simulation Trace", color="k", linewidth=4)
        plt.plot(self.V, translated, label="Translated Trace", color="r", linestyle="--")
        plt.legend()
        plt.show()


    # basic sigmoid function
    def sigmoid_function(self, V):
        return self.rate / (1 + np.exp( -(V - self.midpoint)/self.scale)) + self.b


    # return list of values over self.V
    def calculate_values(self):
        translated = []
        for V in self.V:
            translated.append(self.sigmoid_function(V))

        return translated


    # calculate RMSE
    def RMSE(self):
        # calculate values
        translated = self.calculate_values()
        self.rmse = 0

        for x, y in zip(self.trace, translated):
            self.rmse += (x-y)**2

        self.rmse = np.sqrt(self.rmse)


if (__name__=="__main__"):
    # extract all necessary datapoints
    names, groups, traces = unpack()

    for name, group, trace in zip(names, groups, traces):

        if (group == "PS" or group == "NS"):
            SE = Sigmoidal_Estimator(name, group, trace)
            SE.routine()
