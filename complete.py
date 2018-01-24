from auxiliary import trace_to_np, unpack, generate_plots
from extract_df import get_gate_values
from sigmoidal_estimator import Sigmoidal_Estimator
from dim_reduction import dim_reduction

names, groups, traces = unpack()

get_gate_values()
generate_plots()
dim_reduction(names, groups, traces)
SE = Sigmoidal_Estimator(names[5], groups[5], traces[5])
SE.routine()
