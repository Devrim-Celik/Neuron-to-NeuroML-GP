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
        self.V = np.arange(-150, 151, 5)

    # master function
    def routine(self):
        # calculate parameters
        self.rate_est()
        self.midpoint_est()
        self.scale_est()

        # calculate RMSE
        self.RMSE()

        # check for outliers, probably non sigmoidal shaped
        if (self.rmse > 0.1):
            print("[!] Model({}) has RMSE of {}; it will be removed!".format(self.name, self.rmse))
            self.plot()
            return None, None, None

        return self.rate, self.midpoint, self.scale



    # calculate rate variable
    def rate_est(self):
        # check for "squisyhness", how far max and min are
        self.max_val = np.max(self.trace)
        self.min_val = np.min(self.trace)

        if self.group == "PS":
            self.rate = (self.max_val-self.min_val)
            self.b = self.min_val # bias
        elif self.group == "NS":
            self.rate = -(self.max_val-self.min_val)
            self.b = self.max_val # bias



    # calculate midpoint variable
    def midpoint_est(self):
        # find value in the middle of the y value interval
        midpoint_value = (self.max_val-self.min_val)/2 + self.min_val

        # find corresponding voltage value
        idx = (np.abs(self.trace-midpoint_value)).argmin()
        self.midpoint = self.V[idx]



    # calculate scale variable by testing different value of scale and finding
    # optimum
    def scale_est(self):
        # scale, rmse
        minimum = [1, 1000]
        # iterate, try to find better scale
        for scale in range(1, 50):
            self.scale = scale
            self.RMSE()
            # in case rmse is smaller we found ourselves a better model
            if self.rmse < minimum[1]:
                minimum = scale, self.rmse

        self.scale = minimum[0]



    # plot against simulation
    def plot(self):

        self.RMSE()
        translated = self.calculate_values()

        plt.figure(figsize=(20,10))
        plt.title(self.name+ "\nRMSE = " + str(self.rmse) + " Group: " + self.group + " M: " + str(self.midpoint) + "R: " + str(self.rate) + " S " +  str(self.scale) + " B " + str(self.b))
        plt.plot(self.V, self.trace, label="Simulation Trace", color="k", linewidth=4)
        plt.plot(self.V, translated, label="Translated Trace", color="r", linestyle="--")
        plt.legend()
        plt.show()



    # basic sigmoid function
    def sigmoid_function(self, V):
        return self.rate / (1 + np.exp( -(V - self.midpoint)/self.scale)) + self.b



    # return list of values over self.V with our extraced parameters
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

        self.rmse = np.sqrt(self.rmse/len(self.trace))



if (__name__=="__main__"):
    # extract all necessary datapoints
    names, ion_types, groups, traces = unpack()
    # create dataframe to collect all information
    analysis_df = pd.DataFrame(index=range(len(traces)), \
        columns=["Name", "Type", "Group", "Trace", "Rate", \
            "Midpoint", "Scale", "RMSE"])

    iterator = 0
    for name, ion_type, group, trace in zip(names, ion_types, groups, traces):
        # filter out non sigmoidal
        if (group == "PS" or group == "NS"):
            # get parameters for gate
            SE = Sigmoidal_Estimator(name, ion_type, group, trace)
            rate, midpoint, scale = SE.routine()
            # if flawed value, dont include
            if not (rate == None and midpoint == None and scale == None):
                # add channel to dataframe
                analysis_df.loc[iterator]["Name"] = name
                analysis_df.loc[iterator]["Type"] = ion_type
                analysis_df.loc[iterator]["Group"] = group
                analysis_df.loc[iterator]["Trace"] = trace
                analysis_df.loc[iterator]["Rate"] = rate
                analysis_df.loc[iterator]["Midpoint"] = midpoint
                analysis_df.loc[iterator]["Scale"] = scale
                analysis_df.loc[iterator]["RMSE"] = SE.rmse

                iterator += 1
    # save
    analysis_df.to_pickle("data/analysis_df.pickle")
