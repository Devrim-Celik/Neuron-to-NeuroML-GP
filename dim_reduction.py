import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpldatacursor import datacursor
from auxiliary import unpack

# assign each group a color
group_to_color = {"PS": "red", "NS": "blue", "G": "green", "F": "black"}
# assign each group a color
type_to_color = {"Na": "blue", "K": "red", "Ca": "green"}

def dim_reduction(names, ion_types, groups, traces, reduced_dim=2, perplexity=15,
    use_tSNE=True):

    # marker size
    ms = 15

    if use_tSNE:
        data2d = bh_sne(traces, d=reduced_dim, perplexity=perplexity)
    else:
        pca = PCA(n_components=reduced_dim)
        data2d = pca.fit_transform(traces)



    plt.figure("By_Group", figsize=(20,10))

    for nr, dp in enumerate(data2d):
        plt.scatter(dp[0], dp[1], label=names[nr], \
        c=group_to_color[groups[nr]], s=ms)

    datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))

    plt.savefig("plots/clustering_group.png")





    plt.figure("By_Type", figsize=(20,10))

    for nr, dp in enumerate(data2d):
        plt.scatter(dp[0], dp[1], label=names[nr], \
        c=type_to_color[ion_types[nr]], s=ms)

    datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))

    plt.savefig("plots/clustering_type.png")



def create_legends():
    """
    create legends for the clustering plots, since you have to choose to either
    add a legend or make the plot interactive
    """

    plt.figure("Leg1", figsize=(20,10))
    patch1 = mpatches.Patch(color=group_to_color["PS"], label="Positive Sigmoid")
    patch2 = mpatches.Patch(color=group_to_color["NS"], label="Negative Sigmoid")
    patch3 = mpatches.Patch(color=group_to_color["G"], label="Gaussian")
    patch4 = mpatches.Patch(color=group_to_color["F"], label="Flawed")
    plt.legend(loc="upper left", handles=[patch1, patch2, patch3, patch4], prop={'size': 60})
    plt.savefig("plots/clustering_group_legend.png")

    plt.figure("Leg2", figsize=(20,10))
    patch1 = mpatches.Patch(color=type_to_color["Na"], label="Sodium(Na)")
    patch2 = mpatches.Patch(color=type_to_color["K"], label="Potassium(K)")
    patch3 = mpatches.Patch(color=type_to_color["Ca"], label="Calcium(Ca)")
    plt.legend(loc="upper left", handles=[patch1, patch2, patch3], prop={'size': 60})
    plt.savefig("plots/clustering_type_legend.png")



if (__name__=="__main__"):
    # extract all necessary datapoints
    names, ion_types, groups, traces = unpack()

    dim_reduction(names, ion_types, groups, traces)
    create_legends()
