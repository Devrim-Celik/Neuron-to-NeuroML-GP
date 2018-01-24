import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def trace_to_np(trace_series):
    # container array
    array = np.zeros((len(trace_series),len(trace_series[0][0][0])))

    # read values inside
    for counter, series in enumerate(trace_series):
        array[counter] = series[0][0]

    # return
    return array



def unpack(file_name="extraced_df.pickle"):
    # extract all necessary datapoints
    df = pd.read_pickle("./data/extracted_df.pickle")

    return df["Name"], df["Group"], trace_to_np(df["Trace"])



def save_fig(name, group, trace, time):

    # remove parent directory
    # remove ending
    # remove instances of "/"
    name = name[11:-8].replace("/", "-")

    # plot
    plt.figure()
    plt.plot(time, trace)
    # title
    plt.title("Name: " + name + "\n Group: " + str(group) + "\n Difference: " + str(trace[-1]-trace[0]))
    # save in group folder for better manual analysis
    plt.savefig("plots/"+group+"/"+name+".png")




def generate_plots(names, groups, traces):
    time = np.arange(-150, 151, 5)

    # check if group folder exist, if not create them
    group_folders = ["./plots/PS", "./plots/NS", "./plots/G", "./plots/F"]
    for folder in group_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for nr in range(traces.shape[0]):
        save_fig(names[nr], groups[nr], traces[nr], time)




if __name__=="__main__":
    generate_plots()
