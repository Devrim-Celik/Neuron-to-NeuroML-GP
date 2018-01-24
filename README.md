# NEURON .mod simulation translation into the NeuroML environment for probability of gating particles

## Task
The [Ion Channel Genealogy Website](https://icg.neurotheory.ox.ac.uk/) tries to analyze, compare and evaluate Ion Channel Models from different databases (e.g. [ModelDB](https://senselab.med.yale.edu/modeldb/)). These models are currently written in the [NEURON](https://www.neuron.yale.edu/neuron/) simulation environment. Although the addition of Ion Channel models is always pleasent, right now there is no real possibility to compare these models and put them into a big picture. One intresting application is, given there is a Ion Channel database, if experimentally gathered voltage traces are submitted, without many information about the origin channel, one could compare this model with already existing one and draw conclusions about the experimentally recorded channel. A requirement for such an application is an easy manipulation environment of the given model. Although NEURON has its advantages, easy manipulation is none of them, since, among other things, the definition of underlying ion channel properties can be implemented in many more ways then just a few. Thus we plan on using the NeuroML environment. For this purpose, we have to translate a vast amount of NEURON .mod files into the NeuroML language. Due to the previously described way NEURON operates, the extrapolation and translation of many variables can not be easily automated. For this reason, we will infere them not from their source code, but from their computational responses for given stimulus.
In this Github repository, I will try to find, for every NEURON model, a fitting template in the NeuroML environment.

## Scripts
* [extract_df.py](): Extracts ".dat" files from "./raw_data", group them by their behaviour into either (positive) sigmoidal (PS), negative sigmoidal (NS), Gaussian (G) and Flawed (F) and save them as a pandas dataframe in "./data" as type pickle.
* [auxiliary.py](): auxiliary functions. among others:
  * "unpack": returning the dataframe from the previously pickled dataframe
  * "generate_plots": uses the saved dataframe and creates a simple plot of the behviour of every gating particle
* [dim_reduction.py](): Uses pickled dataframe, reduces every trace from their original 61 dimensions (timesteps) and reduces them using tSNA (or PCA) onto 2 dimensions. Used to analyze difference/similarity in data.
* [sigmoidal_estimator.py](): Uses pickled data and estimates/calculates parameters for a functional equivalent NeuroML template ([HHSigmoidVariable](https://www.neuroml.org/NeuroML2CoreTypes/Channels.html#HHSigmoidVariable)).
* [complete.py](): Executing all scripts for a full run.
