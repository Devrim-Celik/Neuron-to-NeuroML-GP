from auxiliary import trace_to_np, unpack, generate_plots
from extract_df import get_gate_values
from sigmoidal_estimator import Sigmoidal_Estimator
from dim_reduction import dim_reduction
from analysis import analysis


get_gate_values()
names, ion_types, groups, traces = unpack()

generate_plots(names, ion_types, groups, traces)
dim_reduction(names, ion_types, groups, traces)
SE = Sigmoidal_Estimator(names[5], ion_types[5], groups[5], traces[5])
SE.routine()
analysis()
