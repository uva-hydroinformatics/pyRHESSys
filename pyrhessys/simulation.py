import os
import copy
import shutil
import json
import pkg_resources
import subprocess
import shlex
from pathlib import Path
from typing import List
from .plotting import Plotting

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

    def __init__(self, executable, path, run_suffix='rhessys_run', initialize=True):
        """Initialize a new simulation object"""
        self.executable = executable
        self.path = path
        self.clim = self.path + 'clim'
        self.defs = self.path + 'defs'
        self.flows = self.path + 'flows'
        self.obs = self.path + 'obs'
        self.output = self.path + 'output'
        self.tecfiles = self.path + 'tecfiles'
        self.worldfiles = self.path + 'worldfiles'
        self.parameters = PARAMETER_META
        self.file_name = FILE_NAME
        self.path = path
        self.plotting = Plotting(self.obs)
        self.status = 'Uninitialized'
        if initialize:
            self.initialize()

    def initialize(self):
        self.status = 'Initialized'

    def apply_config(self, config):
        for k, v in config.get('parameters', {}).items():
            self.parameters[k] = v
     
    def _gen_rhessys_cmd(self, run_suffix, processes=1, progress='m'):
        self.run_suffix = run_suffix
        rhessys_run_cmd = ''.join(['cd {}; ./{} -st {} -ed {}'.format(self.path[1:], self.parameters['version'], self.parameters['start_date'], self.parameters['end_date']),
                           ' -b -newcaprise -capr {} -gwtoriparian -capMax {}'.format(self.parameters['capr'], self.parameters['capMax']),
                           ' -slowDrain -leafDarkRespScalar {}'.format(self.parameters['leafDarkRespScalar']),
                           ' -frootRespScalar {} -StemWoodRespScalar {}'.format(self.parameters['frootRespScalar'],self.parameters['StemWoodRespScalar']),
                           ' -t tecfiles{} -w worldfiles{} -whdr worldfiles{}'.format(self.file_name['tecfiles'],self.file_name['world'],self.file_name['worldhdr']),
                           ' -r flows{} -rtz {}'.format(self.file_name['flows'], self.parameters['rtz']),
                           ' -pre output/{} -s {} {} {} -sv {} {} -gw {} {}'.format(run_suffix, self.parameters['rtz'], self.parameters['s1'], self.parameters['s2'], self.parameters['s3'], self.parameters['sv1'], self.parameters['sv2'], self.parameters['gw1'], self.parameters['gw2'])                          
                          ])
        return rhessys_run_cmd

    def _run_local(self, run_suffix, processes=1, progress=None):
        """Start a local simulation"""
        run_cmd = self._gen_rhessys_cmd(run_suffix, processes, progress)
        process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = process.communicate()[0].decode('utf-8')
        print(output)
        self.status = 'Running'

    def start(self, run_option,  run_suffix='pyrhessys_run', processes=1, progress=None):
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