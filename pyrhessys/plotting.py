import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import pkg_resources
import seaborn as sns
import cartopy
import geoviews as gv
import geopandas as gpd
import holoviews as hv
import pandas as pd
import xarray as xr

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

	def ts_plot_obs(self, sim_data, sim_output_variable, sim_label, obs_data, obs_variable: str="", obs_label: str="", pre_trim: int=0, post_trim: int=-1):
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

	def ensemble_plot(self, sim_data, name_list, num_config, sim_output_variable, pre_trim: int=0, post_trim: int=-1):
		LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dashdot', 'dotted']
		NUM_STYLES = len(LINE_STYLES)

		sns.reset_orig()  # get default matplotlib styles back
		clrs = sns.color_palette("bright", n_colors=num_config)  # a list of RGB tuples
		fig, ax = plt.subplots(1,figsize=(15,7),linewidth=3.0)
		for i in range(num_config):
			lines = ax.plot(sim_data[i]["Date"][pre_trim:post_trim].values, sim_data[i][sim_output_variable][pre_trim:post_trim].values)
			lines[0].set_color(clrs[i])
			lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		# add x, y label
		ax.set_xlabel('Date (day)', fontsize=15)
		ax.set_ylabel(y_axis, fontsize=15)
		# show up the legend
		ax.tick_params(labelsize=15)
		ax.grid('on')
		fig.legend(labels=name_list, bbox_to_anchor=(0.82, 0.82))
		plt.show()

	def ensemble_obs_plot(self, sim_data, name_list, num_config, sim_output_variable, obs_data, obs_variable, pre_trim: int=0, post_trim: int=-1):
		LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dashdot', 'dotted']
		NUM_STYLES = len(LINE_STYLES)

		sns.reset_orig()  # get default matplotlib styles back
		clrs = sns.color_palette("bright", n_colors=num_config)  # a list of RGB tuples
		fig, ax = plt.subplots(1,figsize=(15,7),linewidth=3.0)
		for i in range(num_config):
			lines = ax.plot(sim_data[i]["Date"][pre_trim:post_trim].values, sim_data[i][sim_output_variable][pre_trim:post_trim].values)
			lines[0].set_color(clrs[i])
			lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
		y_axis = OUTPUT_VARIABLE[sim_output_variable]['description']+'('+OUTPUT_VARIABLE[sim_output_variable]['Units']+')'
		ax.scatter(sim_data[i]["Date"][pre_trim:post_trim].values, obs_data[obs_variable][pre_trim:post_trim-1].values, color='blue', s=10)
		# add x, y label
		ax.set_xlabel('Date (day)', fontsize=15)
		ax.set_ylabel(y_axis, fontsize=15)
		# show up the legend
		ax.tick_params(labelsize=15)
		ax.grid('on')
		fig.legend(labels=name_list, bbox_to_anchor=(0.82, 0.82))
		plt.show()

	#def daily_patch_map(netcdf, variable, timestep):
	    """
    	Create a map for a variable at a given timestep
    	Warning: This function is state dependent! 
    
   		Params:
        	var: the variable of interest
        	timestep: the timestep to plot at
    
    	Returns:
        	poly: A geoviews "shape" plot with the desired data
    	"""
    	# Convert the data from an xarray dataset to a pandas dataframe 
    	# This is necessary for geoviews to be able to plot it
	#	out_df = netcdf[variable].sel(time=timestep).to_dataframe()
		# Make sure we have some metadata to join with the shapefile
	#	out_df['gridcode'] = shapes_df['gridcode'].values
    	# Create the shape plot - some keys:
    	#  - shapes.records() provides the geometry from the shapefiles
    	#  - out_df provides the data
    	#  - value=var chooses which column of the dataframe to use as data for coloring
    	#  - index=['gridcode'] will provide a name on mouse hover
   		#  - on='gridcode' is the key to join the `shapes` with `out_df`
	#	poly = gv.Shape.from_records(shapes.records(), out_df, value=variable, index=['gridcode'], on='gridcode')
    	# Add some options to make things a bit nicer
    	#  - width=700, sets the width, as we expect
    	#  - cmap='plasma' sets the colormap to 'plasma'
    	#  - tools=['hover'] provides information on mouse hover over
    	#  - colorbar=True adds a colorbar
    	#  - alpha=0.7 adds a bit of transparency
	#	poly = poly.opts(width=700, height=600, cmap='plasma', tools=['hover'], colorbar=True, alpha=0.7)
	#	return poly	

	#def daily_patch_map_timeseries(netcdf, variable, start, stop, step, patch):
		# Just as before, use the `var_map` function to build our map
	#	poly = hv.HoloMap({t: daily_var_map(variable, t) for t in netcdf.time.values[start:stop:step]}, kdims=['timestep'])
    	# Vlines will give us an indicator of which time slice we are looking at
	#	vlines = hv.HoloMap({t: hv.VLine(t) for t in netcdf.time.values[start:stop:step]}, kdims=['timestep'])
    	# This seems to make the plot appear more often - probably a holo/geoviews bug somewhere 
	#	poly
    
    	# Calculate min, max, and mean over the domain for each time
	#	vmin = netcdf[variable].isel(time=slice(start, stop)).min(dim=patch).rolling(time=step).min().values
	#	vmax = netcdf[variable].isel(time=slice(start, stop)).max(dim=patch).rolling(time=step).max().values
	#	vmean = netcdf[variable].isel(time=slice(start, stop)).mean(patch).rolling(center=True, time=step).mean().dropna('time')
   
    	# Build the complete interactive plot. Layers are as follows
    	#  - gv.tile_sources.EsriTerrain- Add a background with topography
    	#  - * poly - overlay our map onto the background
    	#  - + hv.Area... - add the area plot to the right
    	#  - * hv.Curve... - overlay the mean curve onto the area plot
    	#  - * vlines... - overlay the timestep indicator
	#	return (gv.tile_sources.EsriTerrain
    #        	* poly
    #        	+ (hv
    #          		.Area((cw18.time[start:stop], vmin, vmax), vdims=['vmin', 'vmax'])
    #           		.opts(alpha=0.5, color='gold', line_color=None)
    #           		.redim.label(x='Date', vmin=var.capitalize()))
    #        	* hv.Curve(vmean).opts(color='purple', alpha=0.8)
    #        	* vlines.opts(alpha=0.4, color='red'))