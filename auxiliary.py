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
    # check if group folder exist, if not create them
    group_folders = ["./plots/PS", "./plots/NS", "./plots/G", "./plots/F"]
    ion_types = ["/Na", "/K", "/Ca"]
    for folder in group_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
        for ion in ion_types:
            if not os.path.exists(folder+ion):
                os.makedirs(folder+ion)

    for nr in range(traces.shape[0]):
        save_fig(names[nr], types[nr], groups[nr], traces[nr])


def write_exception(name, nr, remove_path="./data/removed.txt"):
    # check if text file is already set up, if not create it and write
    # explanational line
    if not os.path.exists(remove_path):
        f = open(remove_path, "w+")
        f.write("List of gating models to further inspect:\n\
        - 1 indicates a constant value over the the whole value range\n\
        - 2 indicates non-sigmoidal shape in some cases\n\
        - 3 indicates wrong size of voltage values (!= 61)\n\
        - 4 indicates too high(>1)/low(<0) values for the probability\n")
        f.close()

    # construct string, which should be added
    add_string = name + "\t" + str(nr) + "\n"

    # open to read and get list of lines
    f = open(remove_path, "r+")
    lines = f.read().strip().split()
    f.close()

    # check if string is already in there
    if not (add_string in lines):
        f = open(remove_path, "a+")
        f.write(add_string)
        f.close()


if __name__=="__main__":
    a,b,c,d = unpack()
    generate_plots(a,b,c,d)
