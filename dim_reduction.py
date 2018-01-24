import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpldatacursor import datacursor
from auxiliary import unpack

def dim_reduction(names, groups, traces, reduced_dim=2, perplexity=15,
    use_tSNE=True):

    if use_tSNE:
        data2d = bh_sne(traces, d=reduced_dim, perplexity=perplexity)
    else:
        pca = PCA(n_components=reduced_dim)
        data2d = pca.fit_transform(traces)

    # assign each group a color
    group_to_color = {"PS": "red", "NS": "blue", "G": "green", "F": "black"}

    plt.figure(figsize=(20,10))

    for nr, dp in enumerate(data2d):
        plt.scatter(dp[0], dp[1], label=names[nr], c=group_to_color[groups[nr]])

    datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))

    plt.savefig("plots/clustering.png")
    plt.show()


if (__name__=="__main__"):
    # extract all necessary datapoints
    names, groups, traces = unpack()

    dim_reduction(names, groups, traces)
