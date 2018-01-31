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



def unpack(file_name="extraced_df.pickle", only_sig=True, return_df=False):
    # extract all necessary datapoints
    df = pd.read_pickle("./data/extracted_df.pickle")

    if only_sig:
        df = df[(df['Group']=="PS") | (df['Group']=="NS")]
        df.index = range(len(df[(df['Group']=="PS") | (df['Group']=="NS")]))

    # filter out outliers
    to_drop = []
    for nr, element in enumerate(df["Trace"]):

        if (max(element[0][0])>1) or (min(element[0][0])<0):
            #to_drop.append(nr)
            df = df.drop(df.index[[nr]])
    #df = df.drop(df.index[to_drop])
    df.index = range(len(df))

    if return_df:
        return df
    else:
        return df["Name"], df["Type"], df["Group"], trace_to_np(df["Trace"])



def save_fig(name, ion_type, group, trace):

    time = np.arange(-150, 151, 5)
    # remove parent directory
    # remove ending
    # remove instances of "/"
    name = name[11:-8].replace("/", "-")

    # plot
    plt.figure()
    plt.plot(time, trace)
    # title
    plt.title("Name: " + name + "\n Group: " + str(group) + " Type: " + ion_type)
    # save in group folder for better manual analysis
    plt.savefig("plots/"+group+"/"+ion_type+"/"+name+".png")




def generate_plots(names, types, groups, traces):
    time = np.arange(-150, 151, 5)

    # check if group folder exist, if not create them
    group_folders = ["./plots/PS", "./plots/NS", "./plots/G", "./plots/F"]
    for folder in group_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for nr in range(traces.shape[0]):
        save_fig(names[nr], types[nr], groups[nr], traces[nr], time)

if __name__=="__main__":
    a,b,c,d = unpack()
    generate_plots(a,b,c,d)
