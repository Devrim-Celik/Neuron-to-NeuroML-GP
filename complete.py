import os, shutil
from auxiliary import trace_to_np, unpack, generate_plots
from extract_df import get_gate_values
from sigmoidal_estimator import Sigmoidal_Estimator, generate_analysis_df
from dim_reduction import dim_reduction
from analysis import analysis
from generate_property_lines_for_gates import generate_sigmoidal_properties

def clear_project():
    delete_content = ["./data", "./plots"]
    for folder in delete_content:
        for file_ in os.listdir(folder):
            file_path = os.path.join(folder, file_)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


# first off, clear whole project outputs
clear_project()

# get data into dataframe
get_gate_values()
# load into variables
names, ion_types, groups, traces = unpack()
# plot gating behviour
generate_plots(names, ion_types, groups, traces)

# fit small sigmoid model on them
generate_analysis_df(show_problems=False)
# generate iteration values over sigmoidal parameters
generate_sigmoidal_properties()
# clustering and plotting
dim_reduction(names, ion_types, groups, traces)
# analysis plot
analysis(show_plot=False)
