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
SHELL_R = pkg_resources.resource_listdir(
        __name__, 'shell_R/')
code =[]
for file in SHELL_R:
    with open(os.getcwd()+"/shell_R/"+file, 'r') as f:
        code.append(f.read())

class Simulation():
    """The simulation object provides a wrapper for RHESSys simulations"""

    def __init__(self, executable, path, run_suffix='rhessys_run', initialize=True):
        """Initialize a new simulation object"""
        self.executable = executable
        self.path = path
        self.clim = self.path + '/clim'
        self.defs = self.path + '/defs'
        self.flows = self.path + '/flows'
        self.obs = self.path + '/obs'
        self.output = self.path + '/output'
        self.tecfiles = self.path + '/tecfiles'
        self.worldfiles = self.path + '/worldfiles'
        self.parameters = PARAMETER_META
        self.code = SHELL_R
        self.file_name = FILE_NAME
        self.path = path
        self.plotting = Plotting(self.obs)
        self.input_ts = TimeSeries(path)
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
        print(rhessys_run_cmd + patch_cmd)
        return rhessys_run_cmd + patch_cmd

    def _run_local(self, run_suffix, processes=1, progress=None):
        """Start a local simulation"""
        run_cmd = self._gen_rhessys_cmd(run_suffix, processes, progress)
        self.process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        #print(self.process.communicate())
        #output = self.process.communicate()[0].decode('utf-8')
        #print(output)
        self.status = 'Running'

    def start(self, run_option,  run_suffix='rhessys_run', processes=1, progress=None):
        """Run a RHESSys simulation"""
        #TODO: Implement running on hydroshare here
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