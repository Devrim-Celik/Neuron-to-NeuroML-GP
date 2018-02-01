import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from auxiliary import unpack

def analysis(file_path="data/analysis_df.pickle", show_plot=True):
    """
    creating a histogram plot with (nr_types*4) subplots. Each row will stand
    for a type of ion, each calumn either for a parameters or the rmse error.
    the idea is to display them side by side, so we can compare them
    """
    # assigning colors
    colors = {"Na": "blue", "K": "red", "Ca": "green"}
    # types we behaviour will consider for now
    allowed = ["PS", "NS"]


    # read data
    df = pd.read_pickle(file_path)

    # figure
    plt.figure("Comparison Sigmoidal", figsize=(20,10))
    plt.title("Comparison of sigmoidal shaped inf. gates")


    # SODIUM: Grap al Sodium channels, we want to consider
    NA_S = df[(df['Type']=="Na") & (df['Group'].isin(allowed))]

    plt.subplot(3,4,1)
    plt.title("Sodium - Rate")
    plt.hist(list(NA_S["Rate"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[NA_S["Type"].iloc[0]], histtype='bar')

    plt.subplot(3,4,2)
    plt.title("Sodium - Midpoint")
    plt.hist(list(NA_S["Midpoint"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[NA_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,3)
    plt.title("Sodium - Scale")
    plt.hist(list(NA_S["Scale"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[NA_S["Type"].iloc[0]], histtype='bar')

    plt.subplot(3,4,4)
    plt.title("Sodium - RMSE")
    plt.hist(list(NA_S["RMSE"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[NA_S["Type"].iloc[0]], histtype='bar')



    # Potssium
    K_S = df[(df['Type']=="K") & (df['Group'].isin(allowed))]

    plt.subplot(3,4,5)
    plt.title("Potassium - Rate")
    plt.hist(list(K_S["Rate"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[K_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,6)
    plt.title("Potassium - Midpoint")
    plt.hist(list(K_S["Midpoint"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[K_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,7)
    plt.title("Potassium - Scale")
    plt.hist(list(K_S["Scale"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[K_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,8)
    plt.title("Potassium - RMSE")
    plt.hist(list(K_S["RMSE"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[K_S["Type"].iloc[0]] ,histtype='bar')



    # Calcium
    Ca_S = df[(df['Type']=="Ca") & (df['Group'].isin(allowed))]

    plt.subplot(3,4,9)
    plt.title("Calcium - Rate")
    plt.hist(list(Ca_S["Rate"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[Ca_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,10)
    plt.title("Calcium - Midpoint")
    plt.hist(list(Ca_S["Midpoint"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[Ca_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,11)
    plt.title("Calcium - Scale")
    plt.hist(list(Ca_S["Scale"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[Ca_S["Type"].iloc[0]] ,histtype='bar')

    plt.subplot(3,4,12)
    plt.title("Calcium - RMSE")
    plt.hist(list(Ca_S["RMSE"]), 25, edgecolor='black', linewidth=1.2, \
        facecolor=colors[Ca_S["Type"].iloc[0]] ,histtype='bar')


    plt.tight_layout()
    plt.savefig("./plots/sigmoidal_parameters_comparison.png")
    if show_plot:
        plt.show()


if (__name__=="__main__"):
    analysis()
