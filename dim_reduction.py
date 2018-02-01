import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import pickle
from tsne import bh_sne
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from mpldatacursor import datacursor
from auxiliary import unpack

# assign each group a color
group_to_color = {"PS": "red", "NS": "blue", "G": "green", "F": "black"}
# assign each group a color
type_to_color = {"Na": "blue", "K": "red", "Ca": "green"}
# value to color
vtc = ["red", "blue", "yellow", "green"]
# marker size for plotting
ms = 15

def dim_reduction(names, ion_types, groups, traces, reduced_dim=2, perplexity=15,
    use_tSNE=False, add_generated=True, interactive=False):

    # tag for plots to differentiate
    if use_tSNE:
        model = "tSNE-"
    else:
        model = "PCA-"

    # get line data in case i wanna plot them (makes sense right?)
    if (add_generated):
        gen_data, gen_names, length = fetch_gen()
        sog = gen_data.shape[0]

    if use_tSNE:
        # in case we have generated lines, pack them together with the traces,
        # reduces them, and then separate them again
        if (add_generated):
            dim_red_a = np.vstack((traces, gen_data))
            temp_data2d = bh_sne(dim_red_a, d=reduced_dim, perplexity=perplexity)
            data2d, gen2d = temp_data2d[:-sog], temp_data2d[-sog:]
        else:
            data2d = bh_sne(traces, d=reduced_dim, perplexity=perplexity)
            print(data2d.shape)
    else:
        # tranform data using pca
        pca = PCA(n_components=reduced_dim)
        data2d = pca.fit_transform(traces)
        # if wanted, also used found eigenvector on gen data
        if (add_generated):
            gen2d = pca.transform(gen_data)


    ############################################################################
    # plot by group
    ############################################################################
    plt.figure("By_Group", figsize=(20,10))
    plt.title("Clustered by " + model[1:] + \
        ", Colored by Groups. Together with generated lines: " + \
        str(add_generated))
    # interatctive or legend?
    if interactive:
        for nr, dp in enumerate(data2d):
            # plot in 2d space
            plt.scatter(dp[0], dp[1], label=names[nr], \
            c=group_to_color[groups[nr]], s=ms)

            # interatctive plot
            datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))
    else:
        for nr, dp in enumerate(data2d):
            plt.scatter(dp[0], dp[1], label=groups[nr], \
            c=group_to_color[groups[nr]], s=ms)

        # add legend in case of non interactive (not possible for interactive)
        patch_PS = mpatches.Patch(color=group_to_color["PS"], \
            label="Positive Sigmoid")
        patch_NS = mpatches.Patch(color=group_to_color["NS"], \
            label="Negative Sigmoid")
        plt.legend(loc="upper left", handles=[patch_PS, patch_NS])

    plt.savefig("plots/"+model+"clustering_group.png")


    ############################################################################
    # plot by ion type
    ############################################################################
    plt.figure("By_Type", figsize=(20,10))
    plt.title("Clustered by " + model[1:] + \
        ", Colored by Ion Type. Together with generated lines: " + \
        str(add_generated))

    if interactive:
        for nr, dp in enumerate(data2d):
            plt.scatter(dp[0], dp[1], label=names[nr], \
            c=type_to_color[ion_types[nr]], s=ms)

        datacursor(formatter='{label}'.format, bbox=dict(fc='white'),       \
                 arrowprops=dict(arrowstyle='simple', fc='black', alpha=0.5))
    else:
        for nr, dp in enumerate(data2d):
            plt.scatter(dp[0], dp[1], label=names[nr], \
            c=type_to_color[ion_types[nr]], s=ms)

        patch_Na = mpatches.Patch(color=type_to_color["Na"], \
            label="Sodium(Na)")
        patch_K = mpatches.Patch(color=type_to_color["K"], \
            label="Potassium(K)")
        patch_Ca = mpatches.Patch(color=type_to_color["Ca"], \
            label="Calcium(Ca)")
        plt.legend(loc="upper left", handles=[patch_Na, patch_K, patch_Ca])


    plt.savefig("plots/"+model+"clustering_type.png")


    ############################################################################
    # plot generated lines onto consisting scatter plot
    ############################################################################
    if (add_generated):


        ############################################################################
        # for midpoint
        plt.figure("Generated_Midpoint", figsize=(20,10))

        # plot clusters
        for nr, dp in enumerate(data2d):
            plt.scatter(dp[0], dp[1], color="k", s=ms)

        # changing midpoint
        for i, name_ in enumerate(gen_names[:4]):

            # get corresponding datapoints
            dat = gen2d[i*length:(i+1)*length]
            # get the right name
            name = gen_names[i]
            # plot
            plt.plot(dat[:,0], dat[:,1], linewidth=0.75, marker="o", c=vtc[i], label=name)
            plt.legend(loc="upper left")

        plt.savefig("plots/"+model+"clustering_gen_lines_midpoint.png")

        ############################################################################
        # for scale
        plt.figure("Generated_Scale", figsize=(20,10))

        # plot clusters
        for nr, dp in enumerate(data2d):
            plt.scatter(dp[0], dp[1], color="k", s=ms)

        #  changing scale
        for i, name_ in enumerate(gen_names[4:]):

            # get correspondi   ng datapoints
            dat = gen2d[(i+4)*length:(i+5)*length]
            # get the right name
            name = gen_names[i+4]
            # plot
            plt.plot(dat[:,0], dat[:,1], linewidth=0.75, marker="o", c=vtc[i], label=name)
            plt.legend(loc="upper left")

        plt.savefig("plots/"+model+"clustering_gen_lines_scaling.png")
        ############################################################################
        ############################################################################


def fetch_gen(file_name="./data/generated_lines.pickle"):
    # load data
    with open(file_name, 'rb') as handle:
        gen_dict = pickle.load(handle)

    # create np with

    # fill it up with the data
    for setup in gen_dict.keys():
        # try to append to array
        try:
            gen_np = np.vstack((gen_np, gen_dict[setup]["trace"]))
        # in case there is no array to append to yet, set it to first element
        except:
            gen_np = gen_dict[setup]["trace"]
            setup_len = gen_dict[setup]["trace"].shape[0]

    # return data, description list, len of one setup
    return gen_np, [gen_dict[dic]["description"] for dic in gen_dict.keys()], setup_len


if (__name__=="__main__"):
    # extract all necessary datapoints
    names, ion_types, groups, traces = unpack(only_sig=True)
    dim_reduction(names, ion_types, groups, traces)
