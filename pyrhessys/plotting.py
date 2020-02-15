import seaborn as sns
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import pkg_resources

OUTPUT = pkg_resources.resource_filename(
        __name__, 'meta/output_variables.json')
with open(OUTPUT, 'r') as f:
    OUTPUT_VARIABLE = json.load(f)

class Plotting:

	def __init__(self, filepath):
		self.filepath = filepath
		#self.start_date = PARAMETER_META['start_date']
		#self.end_date = PARAMETER_META['end_date']

	def ts_plot(self, data, sim_output_variable, sim_label, pre_trim: int=0, post_trim: int=-1):
		self.filepath
		# set output variables and variable description
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# Plotting 
		plt.figure(figsize=(17,10))
		ax = plt.gca()
		ax.plot(data["Date"][pre_trim:post_trim], data[sim_output_variable][pre_trim:post_trim], label=sim_label)
		ax.grid(True)
		ax.set_ylabel(y_axis, fontsize=18)
		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)
		ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)

	def ts_plot_obs(self, sim_data, sim_output_variable, sim_label, obs_data, obs_variable: str="", obs_label: str="", pre_trim: int=0, post_trim: int=-1, ):
		self.filepath
		# set output variables and variable description
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# Plotting 
		plt.figure(figsize=(17,10))
		ax = plt.gca()
		ax.plot(sim_data["Date"][pre_trim:post_trim], sim_data[sim_output_variable][pre_trim:post_trim], label=sim_label)
		ax.plot(obs_data.index[pre_trim:post_trim], obs_data[obs_variable][pre_trim:post_trim], label=obs_label)
		ax.grid(True)
		ax.set_ylabel(y_axis, fontsize=18)
		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)
		ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)