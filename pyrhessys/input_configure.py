import pandas as pd
import numpy as np
import os, shutil


class TimeSeries:

	def __init__(self, filepath):
		self.filepath = filepath

	def rainfall(self, name, data, start_date, col_name="rain"):
		np.savetxt(name+'.rain', data[col_name].values, fmt='%2.4f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.rain'):
			os.remove(self.filepath + '/' + name+'.rain')
		shutil.move(name+'.rain', self.filepath)

	def tempmax(self, name, data, start_date, col_name="tmax"):
		np.savetxt(name+'.tmax', data[col_name].values, fmt='%2.1f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.tmax'):
			os.remove(self.filepath + '/' + name+'.tmax')
		shutil.move(name+'.tmax', self.filepath)

	def tempmin(self, name, data, start_date, col_name="tmin"):
		np.savetxt(name+'.tmin', data[col_name].values, fmt='%2.1f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.tmin'):
			os.remove(self.filepath + '/' + name+'.tmin')
		shutil.move(name+'.tmin', self.filepath)

	def vpd(self, name, data, start_date, col_name="vpd"):
		#vpd = pd.to_numeric(data[col_name].values, errors='coerce')
		#np.savetxt(r'cwt.vpd', vpd, fmt='%3.2f', header=start_date, comments='')
		np.savetxt(name+'.vpd', data[col_name].values, fmt='%2.1f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.vpd'):
			os.remove(self.filepath + '/' + name+'.vpd')
		shutil.move(name+'.vpd', self.filepath)

	def rh(self, name, data, start_date, col_name="rh"):
		#rh = pd.to_numeric(data[col_name].values, errors='coerce')
		#np.savetxt(r'cwt.relative_humidity', rh, fmt='%2.1f', header=start_date, comments='')
		np.savetxt(name+'.relative_humidity', data[col_name].values, fmt='%2.1f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.relative_humidity'):
			os.remove(self.filepath + '/' + name+'.relative_humidity')
		shutil.move(name+'.relative_humidity', self.filepath)

	def kdownDirect(self, name, data, start_date, col_name="kdownDirect"):
		#kdownDirect = pd.to_numeric(data[col_name].values, errors='coerce')
		#np.savetxt(r'cwt.Kdown_direct', kdownDirect, fmt='%5.1f', header=start_date, comments='')
		np.savetxt(name+'.Kdown_direct', data[col_name].values, fmt='%2.1f', header=start_date, comments='')
		if os.path.exists(self.filepath + '/' + name+'.Kdown_direct'):
			os.remove(self.filepath + '/' + name+'.Kdown_direct')
		shutil.move(name+'.Kdown_direct', self.filepath)

	def clim_base(self, name, sta_id="101", x="278391.71", y="3882439.5",z="638.0", e_lai="2.0", s_height="22.9"):
		base = open(name+".base", "w")
		contents = ''.join(['{} base_station_id \n'.format(sta_id),
                            '{} x_coordinate \n'.format(x),
                            '{} y_coordinate \n'.format(y),
                            '{} z_coordinate \n'.format(z),
                            '{} effective_lai \n'.format(e_lai),
                            '{} screen_height \n'.format(s_height),
                            '{}/{} daily_climate_prefix \n'.format(self.filepath, name),
                            '0'])
		base.writelines(contents)
		base.close()
		if os.path.exists(self.filepath + '/' + name+'.base'):
			os.remove(self.filepath + '/' + name+'.base')
		shutil.move(name+".base", self.filepath)

	def tecfile(self, start_date):
		tec_daily = open("tec_daily.txt","w") 
		contents = ["{} print_daily_on ".format(start_date)]  
		tec_daily.writelines(contents) 
		tec_daily.close() 
		if os.path.exists(self.filepath + '/tec_daily.txt'):
			os.remove(self.filepath + '/tec_daily.txt')
		shutil.move('tec_daily.txt', self.filepath)