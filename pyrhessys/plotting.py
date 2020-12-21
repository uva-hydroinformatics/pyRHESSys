import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import pkg_resources
import seaborn as sns

OUTPUT = pkg_resources.resource_filename(
        __name__, 'meta/output_variables.json')
with open(OUTPUT, 'r') as f:
    OUTPUT_VARIABLE = json.load(f)

class Plotting:

	def __init__(self, filepath):
		self.filepath = filepath
		#self.start_date = PARAMETER_META['start_date']
		#self.end_date = PARAMETER_META['end_date']

	def sim_basin_daily_plot(self, basin_daily_output, sim_output_variable, sim_label, pre_trim: int=0, post_trim: int=-1, log_unit=False):
		self.filepath
		daily_data = pd.read_csv(basin_daily_output, delimiter=" ")
		daily_data['date'] = pd.to_datetime(daily_data[['year', 'month', 'day']])
		daily_data.set_index('date', inplace=True)
		# set output variables and variable description
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# Plotting 
		plt.figure(figsize=(17,7))
		ax = plt.gca()

		if log_unit is True:
    			plt.yscale('log')

		ax.plot(daily_data.index[pre_trim:post_trim], daily_data[sim_output_variable][pre_trim:post_trim], label=sim_label)
		ax.grid(True)
		ax.set_ylabel(y_axis, fontsize=15)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
		ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
		plt.savefig("basin_daily_plot.png")

	def ts_plot_obs(self, sim_data, sim_date_col_name, sim_output_variable, sim_label, obs_data, obs_variable: str="", obs_label: str="", pre_trim: int=0, post_trim: int=-1):
		self.filepath
		# set output variables and variable description
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# Plotting 
		plt.figure(figsize=(17,7))
		ax = plt.gca()
		ax.plot(sim_data[sim_date_col_name][pre_trim:post_trim], sim_data[sim_output_variable][pre_trim:post_trim], label=sim_label)
		ax.plot(obs_data.index[pre_trim:post_trim], obs_data[obs_variable][pre_trim:post_trim], label=obs_label)
		ax.grid(True)
		ax.set_ylabel(y_axis, fontsize=18)
		plt.xticks(fontsize=18)
		plt.yticks(fontsize=18)
		ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
		plt.savefig("figure.png")

	def ensemble_plot(self, sim_data, sim_date_col_name, name_list, num_config, sim_output_variable, pre_trim: int=0, post_trim: int=-1):
		LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dashdot', 'dotted']
		NUM_STYLES = len(LINE_STYLES)

		sns.reset_orig()  # get default matplotlib styles back
		clrs = sns.color_palette("bright", n_colors=num_config)  # a list of RGB tuples
		fig, ax = plt.subplots(1,figsize=(15,7),linewidth=3.0)
		for i in range(num_config):
			lines = ax.plot(sim_data[i][sim_date_col_name][pre_trim:post_trim].values, sim_data[i][sim_output_variable][pre_trim:post_trim].values)
			lines[0].set_color(clrs[i])
			lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# add x, y label
		ax.set_xlabel('Date', fontsize=15)
		ax.set_ylabel(y_axis, fontsize=15)
		# show up the legend
		ax.tick_params(labelsize=15)
		ax.grid('on')
		fig.legend(labels=name_list, bbox_to_anchor=(0.82, 0.82))
		plt.show()
		plt.savefig("figure.png")

	def ensemble_obs_plot(self, sim_data, sim_date_col_name, name_list, num_config, sim_output_variable, obs_data, obs_variable, pre_trim: int=0, post_trim: int=-1):
		LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dashdot', 'dotted']
		NUM_STYLES = len(LINE_STYLES)

		sns.reset_orig()  # get default matplotlib styles back
		clrs = sns.color_palette("bright", n_colors=num_config)  # a list of RGB tuples
		fig, ax = plt.subplots(1,figsize=(15,7),linewidth=3.0)
		for i in range(num_config):
			lines = ax.plot(sim_data[i][sim_date_col_name][pre_trim:post_trim].values, sim_data[i][sim_output_variable][pre_trim:post_trim].values)
			lines[0].set_color(clrs[i])
			lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		ax.scatter(sim_data[i][sim_date_col_name][pre_trim:post_trim].values, obs_data[obs_variable][pre_trim:post_trim-1].values, color='blue', s=10)
		# add x, y label
		ax.set_xlabel('Date', fontsize=15)
		ax.set_ylabel(y_axis, fontsize=15)
		# show up the legend
		ax.tick_params(labelsize=15)
		ax.grid('on')
		fig.legend(labels=name_list, bbox_to_anchor=(0.82, 0.82))
		plt.show()
		plt.savefig("figure.png")