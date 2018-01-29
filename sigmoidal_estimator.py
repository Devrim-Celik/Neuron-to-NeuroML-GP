import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from auxiliary import unpack

class Sigmoidal_Estimator():

    def __init__(self, name, ion_type, group, trace):
        self.name = name
        self.ion_type = ion_type
        self.group = group
        self.trace = trace

        self.b = 0 # notfall, fall ich hoch oder runter muss

        self.V = np.arange(-150, 151, 5)


    # master function
    def routine(self):
        # added bias for negative function
        b_dict = {"PS": 0, "NS": np.max(self.trace)}
        self.b = b_dict[self.group]
        # calculate parameters
        self.rate_est()
        self.midpoint_est()
        self.scale_est()
        # plotting
        #self.plot()


        self.RMSE()

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
        plt.title(self.name+ "\nRMSE = " + str(self.rmse) + " Group: " + self.group + " M: " + str(self.midpoint) + "R: " + str(self.rate) + " S " +  str(self.scale))
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
    names, ion_types, groups, traces = unpack()

    # TODO do it for all
    # for group F --> just constant value as property
    # for G --> Gaussian fit with properties : mean, variance, factor (a*(...))

    analysis_df = pd.DataFrame(index=range(len(traces)), \
        columns=["Name", "Type", "Group", "Trace", "Rate", \
            "Midpoint", "Scale", "RMSE"])

    iterator = 0
    for name, ion_type, group, trace in zip(names, ion_types, groups, traces):

        if (group == "PS" or group == "NS"):
            SE = Sigmoidal_Estimator(name, ion_type, group, trace)
            rate, midpoint, scale = SE.routine()


            analysis_df.loc[iterator]["Name"] = name
            analysis_df.loc[iterator]["Type"] = ion_type
            analysis_df.loc[iterator]["Group"] = group
            analysis_df.loc[iterator]["Trace"] = trace
            analysis_df.loc[iterator]["Rate"] = rate
            analysis_df.loc[iterator]["Midpoint"] = midpoint
            analysis_df.loc[iterator]["Scale"] = scale

            if SE.rmse > 2:
                analysis_df.loc[iterator]["RMSE"] = 2
            else:
                analysis_df.loc[iterator]["RMSE"] = SE.rmse

            iterator += 1

    analysis_df.to_pickle("data/analysis_df.pickle")
