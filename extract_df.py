import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from auxiliary import write_exception

def get_gate_values(directory="./raw_data", remove_path="./data/removed.txt"):




    # get list with paths to all folders in the current directory
    folder_list = [x[0] for x in os.walk(directory) if ".mod" in x[0]]

    total_df = pd.DataFrame(index=range(0,10000), columns=["Name", "Type", "Group", "Trace"])
    index_counter = 0

    # look into every folder in the list, check if there is a file which
    # describes the probability of gate opening. Save values in a list
    # also save corresponding file names
    for folder_name in folder_list:
        # get tuple with:
        #   tuple[0] = folder name
        #   tuple[2] = list of file
        for file_tuple in os.walk(folder_name):
            for file_name in file_tuple[2]:
                # check if intresting data
                if "inf.dat" in file_name:
                    # name of the data
                    name = file_tuple[0] + "/" + file_name
                    # data
                    data = np.loadtxt(name)[:,1]

                    # check if standard type
                    if data.shape[0] == 61:

                        data = data.reshape(1,61)

                        # filter out outliers
                        if (np.amax(data)>1) or (np.amin(data)<0):
                            write_exception(name, 4)

                        else:
                            # group id, NOTE
                            #   Assignment of the groups:
                            #   - "PS": Positive Sigmoidal of form 1/(1+exp(-t))
                            #   - "NS": Negative Sigmoidal of form -1/(1+exp(-t))
                            #   - "G": Gaussian Distributed
                            #   - "R": Rest --> Probably Screwed Data

                            # assign groups, given slope
                            if (data[0,-1] - data[0,0]) < -0.1:
                                group = "NS"
                            elif (data[0,-1] - data[0,0]) > 0.1:
                                group = "PS"

                            # very similiar start at end point, if max == min:
                            # --> screwed data
                            else:
                                if (np.max(data) != np.min(data)):
                                    group = "G"
                                else:
                                    group = "F"
                                    # add to removed list, since this grouping
                                    # most likely indicates a problem with the
                                    # value generation of the mod file
                                    write_exception(name, 1)

                            # find out which ion type
                            if "/K/" in name:
                                type_ion = "K"
                            elif "/Na/" in name:
                                type_ion = "Na"
                            elif "/Ca/" in name:
                                type_ion = "Ca"
                            else:
                                print("[-] Type not found")

                            if not np.isnan(data).any():
                                # add values to dataframe
                                total_df.loc[index_counter]["Name"] = name
                                total_df.loc[index_counter]["Type"] = type_ion
                                total_df.loc[index_counter]["Group"] = group
                                total_df.loc[index_counter]["Trace"] = pd.Series([data])



                                index_counter += 1

                    else:
                        write_exception(name, "3")



    # since there wasnt another way that give more indexes than we need
    # at the start, of dynamically locating them, remove all empty rows
    total_df = total_df.dropna()#[np.isfinite(total_df['Name'])]

    total_df.to_pickle("data/extracted_df.pickle")

    return total_df



if (__name__=="__main__"):
    get_gate_values()
