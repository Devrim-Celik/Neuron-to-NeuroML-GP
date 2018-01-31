import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from auxiliary import unpack

def analysis(file_path="data/analysis_df.pickle"):
    """
    creating a plot with (nr_types*4) subplots. Each row will stand for a
    type of ion, each calumn either for a parameters or the rmse error.
    the idea is to display them side by side, so we can compare them
    """

    # read data
    df = unpack(return_df=True)
    # open figure
    plt.figure("Comparison Sigmoidal", figsize=(20,10))
    plt.title("Comparison Sigmoidal")
    # thickness of different bar plots, necessary since plt.bar acts rather
    # weird in terms of automatic thickness
    a,b1,b2,c1,c2,d = 0.07, 1.5, 3, 0.3, 0.6, 0.01
    # assigning colors
    colors = {"Na": "blue", "K": "red", "Ca": "green"}
    # types we behaviour will consider for now
    ok = ["PS", "NS"]


    # SODIUM: Grab al Sodium channels, we want to consider
    NA_S = df[(df['Type']=="Na") & (df['Group'].isin(ok))]

    # get bins, amount in each bin, indice for each bin & stepsize
    am, bins, indice, step = bin_gen(NA_S["Rate"])
    # create a plot, with correspoinding title, plot the bins and display
    # right indices
    plt.subplot(3,4,1)
    plt.title("Na - Rate")
    plt.bar(bins[:-1], am, a , color=colors[NA_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(NA_S["Midpoint"])
    plt.subplot(3,4,2)
    plt.title("Na - Midpoint")
    plt.bar(bins[:-1], am, b1, color=colors[NA_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(NA_S["Scale"])
    plt.subplot(3,4,3)
    plt.title("Na - Scale")
    plt.bar(bins[:-1], am, c1, color=colors[NA_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(NA_S["RMSE"], ind_normal=False)
    plt.subplot(3,4,4)
    plt.title("Na - RMSE")
    plt.bar(bins[:-1], am, d, color=colors[NA_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)



    # Potssium
    K_S = df[(df['Type']=="K") & (df['Group'].isin(ok))]

    am, bins, indice, step = bin_gen(K_S["Rate"])
    plt.subplot(3,4,5)
    plt.title("K - Rate")
    plt.bar(bins[:-1], am, a, color=colors[K_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(K_S["Midpoint"])
    plt.subplot(3,4,6)
    plt.title("K - Midpoint")
    plt.bar(bins[:-1], am, b2, color=colors[K_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(K_S["Scale"])
    plt.subplot(3,4,7)
    plt.title("K - Scale")
    plt.bar(bins[:-1], am, c2, color=colors[K_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(K_S["RMSE"], ind_normal=False)
    plt.subplot(3,4,8)
    plt.title("K - G - RMSE")
    plt.bar(bins[:-1], am, d, color=colors[K_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)




    # Calcium
    Ca_S = df[(df['Type']=="Ca") & (df['Group'].isin(ok))]

    am, bins, indice, step = bin_gen(Ca_S["Rate"])
    plt.subplot(3,4,9)
    plt.title("Ca - PS - Rate")
    plt.bar(bins[:-1], am, a, color=colors[Ca_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(Ca_S["Midpoint"])
    plt.subplot(3,4,10)
    plt.title("Ca - NS - Midpoint")
    plt.bar(bins[:-1], am, b2, color=colors[Ca_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(Ca_S["Scale"])
    plt.subplot(3,4,11)
    plt.title("Ca - F - Scale")
    plt.bar(bins[:-1], am, c2, color=colors[Ca_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)

    am, bins, indice, step = bin_gen(Ca_S["RMSE"], ind_normal=False)
    plt.subplot(3,4,12)
    plt.title("Ca - G - RMSE")
    plt.bar(bins[:-1], am, d, color=colors[Ca_S["Type"].iloc[0]])
    plt.xticks(bins[:-1], indice)


    plt.tight_layout()

    plt.savefig("./plots/S_parameters_comparison.png")

    plt.show()



def bin_gen(features, n_bins=13, ind_normal=True):

    # exclude last & first 5% entries, since they are procacly proclem cases
    features = features.sort_values()[int(len(features)*0.05):-int(len(features)*0.05)]
    my_max = np.amax(features)
    my_min = np.amin(features)

    # calculate interval of interest and create bins
    diff = my_max-my_min
    step = diff/n_bins
    bins = [my_min+step*i for i in range(n_bins+1)]
    amount = [0]*n_bins

    # fill bins
    for feature in features:
        for i, bin_val in enumerate(bins):
            if feature <= bin_val:
                amount[i-1] += 1
                break
    # generate indices
    if ind_normal:
        indice = [">{:0.2f}".format(bin_value) if i%3==0 else " " for i, bin_value in enumerate(bins)]
    else:
        indice = [">"+format(bin_value, '.1e') if i%3==0 else " " for i, bin_value in enumerate(bins)]
    return amount, bins, indice, step


if (__name__=="__main__"):
    analysis()
