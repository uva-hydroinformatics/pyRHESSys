import os
import copy
import shutil
import json
import pkg_resources
import subprocess
import shlex
import xarray as xr
from pathlib import Path
from typing import List

from .plotting import Plotting
from .input_configure import TimeSeries

PARAMETER = pkg_resources.resource_filename(
        __name__, 'meta/parameter_meta.json')
with open(PARAMETER, 'r') as f:
    PARAMETER_META = json.load(f)
FILE = pkg_resources.resource_filename(
        __name__, 'meta/file_name.json')
with open(FILE, 'r') as f:
    FILE_NAME = json.load(f)

class Simulation():
    """The simulation object provides a wrapper for RHESSys simulations"""

    def __init__(self, executable, project_path, run_suffix='rhessys_run', initialize=True, config_dir='.pyrhessys'):
        """Initialize a new simulation object"""
        self.executable = executable
        self.path = project_path
        self.clim = self.path + '/clim'
        self.defs = self.path + '/defs'
        self.flows = self.path + '/flows'
        self.obs = self.path + '/obs'
        self.output = self.path + '/output'
        self.tecfiles = self.path + '/tecfiles'
        self.worldfiles = self.path + '/worldfiles'
        self.parameters = PARAMETER_META
        self.file_name = FILE_NAME
        self.project_path = Path(os.path.abspath(os.path.realpath(project_path)))
        self.config_path = self.project_path / config_dir
        self.plotting = Plotting(self.obs)
        self.input_ts = TimeSeries(project_path)
        self.status = 'Uninitialized'
        self.stdout = None
        self.stderr = None
        self.process = None
        if initialize:
            self.initialize()

    def initialize(self):
        self.status = 'Initialized'

    def apply_config(self, config):
        for k, v in config.get('parameters', {}).items():
            self.parameters[k] = v
     
    def _gen_rhessys_cmd(self, run_suffix, processes=1, progress='m'):
        self.run_suffix = run_suffix
        rhessys_run_cmd = ''.join(['cd {}; ./{} -st {} -ed {}'.format(os.path.dirname(self.executable), self.parameters['version'], self.parameters['start_date'], self.parameters['end_date']),
                           ' -b -gwtoriparian -t {}{}'.format(self.tecfiles, self.file_name['tecfiles']),
                           ' -w {}{} -whdr {}{}'.format(self.worldfiles, self.file_name['world'], self.worldfiles, self.file_name['world_hdr']),
                           ' -r {}{} {}{}'.format(self.flows, self.file_name['flows_sub'], self.flows, self.file_name['flows_surf']),
                           ' -pre {}/{} -gw {} {} -s {} {} {}'.format(self.output, run_suffix, self.parameters['gw1'], self.parameters['gw2'], self.parameters['s1'], self.parameters['s2'], self.parameters['s3']),     
                           ' -snowEs {} -snowTs {} -sv {} {} -svalt {} {}'.format(self.parameters['snowEs'], self.parameters['snowTs'], self.parameters['sv1'], self.parameters['sv2'], self.parameters['svalt1'], self.parameters['svalt2'])                          
                          ])

        if self.parameters['locationid'] == "0" :
            patch_cmd = ""
        elif self.parameters['locationid'] == "1" :
            patch_cmd = " -p"
        elif self.parameters['locationid'] == "2" :
            patch_cmd = " -p {} {} {} {}".format(self.parameters['basin_id'], self.parameters['hillslope_id'], self.parameters['zone_id'], self.parameters['patch_id'])
        else:
            print(" set locationid: 0-No use location ID, 1-Use every location ID, 2-Use certain ID")
        #print(rhessys_run_cmd + patch_cmd)
        return rhessys_run_cmd + patch_cmd

    def _run_local(self, run_suffix, processes=1, progress=None):
        """Start a local simulation"""
        run_cmd = self._gen_rhessys_cmd(run_suffix, processes, progress)
        self.process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #print(self.process.communicate())
        #output = self.process.communicate()[0].decode('utf-8')
        #print(output)
        self.status = 'Running'

    def _run_docker(self, run_suffix, processes=1, progress=None):
        """Start a docker simulation"""
        #run_cmd = self._gen_rhessys_cmd(run_suffix, processes, progress)
        #run_cmd = run_cmd.replace(self.executable, 'cd /pyrhessys/RHESSysEastCoast; ./rhessysEC.7.2')

        rhessys_run_cmd = ''.join(['cd /pyrhessys/RHESSysEastCoast; ./rhessysEC.7.2 -st {} -ed {}'.format(self.parameters['start_date'], self.parameters['end_date']),
                           ' -b -gwtoriparian -t {}{}'.format(self.tecfiles, self.file_name['tecfiles']),
                           ' -w {}{} -whdr {}{}'.format(self.worldfiles, self.file_name['world'], self.worldfiles, self.file_name['world_hdr']),
                           ' -r {}{} {}{}'.format(self.flows, self.file_name['flows_sub'], self.flows, self.file_name['flows_surf']),
                           ' -pre {}/{} -gw {} {} -s {} {} {}'.format(self.output, run_suffix, self.parameters['gw1'], self.parameters['gw2'], self.parameters['s1'], self.parameters['s2'], self.parameters['s3']),     
                           ' -snowEs {} -snowTs {} -sv {} {} -svalt {} {}'.format(self.parameters['snowEs'], self.parameters['snowTs'], self.parameters['sv1'], self.parameters['sv2'], self.parameters['svalt1'], self.parameters['svalt2'])                          
                          ])

        if self.parameters['locationid'] == "0" :
            patch_cmd = ""
        elif self.parameters['locationid'] == "1" :
            patch_cmd = " -p"
        elif self.parameters['locationid'] == "2" :
            patch_cmd = " -p {} {} {} {}".format(self.parameters['basin_id'], self.parameters['hillslope_id'], self.parameters['zone_id'], self.parameters['patch_id'])
        else:
            print(" set locationid: 0-No use location ID, 1-Use every location ID, 2-Use certain ID")
        
        self.rhessys_run = rhessys_run_cmd + patch_cmd

        cmd = ''.join(['docker run -v {}:{}'.format(self.path, self.path),
                       " --entrypoint '/bin/bash' ",
                       self.executable,
                       '  -c "',
                       self.rhessys_run, '"'])
        print(cmd)
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.status = 'Running'

    def start(self, run_option,  run_suffix='rhessys_run', processes=1, progress=None):
        """Run a RHESSys simulation"""
        self.run_suffix = run_suffix
        if run_option == 'local':
            self._run_local(run_suffix, processes, progress)
        elif run_option == 'docker':
            self._run_docker(run_suffix, processes, progress)
        else:
            raise NotImplementedError('Invalid runtime given! '
                                      'Valid options: local, docker')

    def run(self, run_option,  run_suffix='rhessys_run', processes=1, progress=None):
        self.start(run_option, run_suffix, processes, progress)
        self.monitor()

    def monitor(self):
        # Simulation already run
        if self.status in ['Error', 'Success']:
            return self.status

        if self.process is None:
            raise RuntimeError('No simulation started! Use simulation.start '
                               'or simulation.execute to begin a simulation!')

        self.stdout, self.stderr = self.process.communicate()
        if isinstance(self.stdout, bytes):
            self.stderr = self.stderr.decode('utf-8', 'ignore')
            self.stdout = self.stdout.decode('utf-8', 'ignore')

        SUCCESS_MSG = 'Constructing basins'
        print(self.stdout)
        if SUCCESS_MSG not in self.stdout:
            self.status = 'Error'
        else:
            self.status = 'Success'

        try:
            self._output = [xr.open_dataset(f) for f in self.get_output()]
            if len(self._output) == 1:
                self._output = self._output[0]
        except Exception:
            self._output = None

        return self.status

    def get_output(self) -> List[str]:
        new_file_text = 'Created output file:'
        out_files = []
        for l in self.stdout.split('\n'):
            if new_file_text in l:
                out_files.append(
                    l.split(';')[0].replace(new_file_text, '').strip())
        return out_files

    def parallel_job(self, executable, start_date, end_date, config, path):

        list_keys = [k for k in config]
        p = list_keys[0].split("++")[1:len(list_keys[0].split("++")) - 1]

        parameter = []
        name = []

        for i in list_keys:
            name.append(i)

        for i, value in enumerate(list_keys):
            parameter.append(list_keys[i].split("++")[1:len(list_keys[i].split("++")) - 1])

        parallel_run_cmd1 = []
        for i, k in enumerate(list_keys):
            rhessys_run_cmd = ''.join(['cd {}; ./{} -st {} -ed {}'.format(os.path.dirname(self.executable), self.parameters['version'], self.parameters['start_date'], self.parameters['end_date']),
                           ' -b -gwtoriparian -t {}{}'.format(self.tecfiles, self.file_name['tecfiles']),
                           ' -w {}{} -whdr {}{}'.format(self.worldfiles, self.file_name['world'], self.worldfiles, self.file_name['world_hdr']),
                           ' -r {}{} {}{}'.format(self.flows, self.file_name['flows_sub'], self.flows, self.file_name['flows_surf']),
                           ' -pre {}/{}'.format(self.output, name[i])  
                          ])
            parallel_run_cmd1.append(rhessys_run_cmd)
        parallel_run_cmd2 = []
        my_dict = {'gw1': self.parameters['gw1'], 'gw2': self.parameters['gw2'], 's1': self.parameters['s1'], 's2': self.parameters['s2'], 
                's3': self.parameters['s3'], 'snowEs': self.parameters['snowEs'], 'snowTs': self.parameters['snowTs'], 
                'sv1': self.parameters['sv1'], 'sv2': self.parameters['sv2'], 'svalt1': self.parameters['svalt1'], 'svalt2': self.parameters['svalt2']}

        for i, k in enumerate(parameter):
            for j in parameter[i]:
                keys = j.split("=")[0]
                values = j.split("=")[1]
                my_dict[keys] = values

            par = ' -gw ' + str(my_dict['gw1']) + ' ' + str(my_dict['gw2']) + ' ' + ' -s ' + str(my_dict['s1']) + ' ' + str(my_dict['s2']) + ' ' + str(my_dict['s3'])  \
                + ' ' +' -snowEs ' + str(my_dict['snowEs']) + ' ' +' -snowTs '+ str(my_dict['snowTs']) + ' ' + ' -sv ' \
                + str(my_dict['sv1']) + ' ' + str(my_dict['sv2']) + ' -svalt ' + str(my_dict['svalt1']) + ' ' + str(my_dict['svalt2'])
                                                                                  
            parallel_run_cmd2.append(par)  

            if self.parameters['locationid'] == "0" :
                patch_cmd = ""
            elif self.parameters['locationid'] == "1" :
                patch_cmd = " -p"
            elif self.parameters['locationid'] == "2" :
                patch_cmd = " -p {} {} {} {}".format(self.parameters['basin_id'], self.parameters['hillslope_id'], self.parameters['zone_id'], self.parameters['patch_id'])
            else:
                print(" set locationid: 0-No use location ID, 1-Use every location ID, 2-Use certain ID")

        for i, k in enumerate(list_keys):
            cmd = parallel_run_cmd1[i] + ' ' + parallel_run_cmd2[i] + ' ' + patch_cmd 
            print(cmd)

            file_name = path + "/" + "input_"+str(i)+".txt"
            parallel_cmd = open(file_name, "w") 
            parallel_cmd.write(cmd)
            parallel_cmd.close()
        
        return name