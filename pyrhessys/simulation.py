import os
import copy
import shutil
import json
import pkg_resources
import subprocess
import shlex
from pathlib import Path
from typing import List

PARAMETER_PATH = pkg_resources.resource_filename(
        __name__, 'meta/parameter_meta.json')
with open(PARAMETER_PATH, 'r') as f:
    PARAMETER_META = json.load(f)
FILE_PATH = pkg_resources.resource_filename(
        __name__, 'meta/file_name.json')
with open(FILE_PATH, 'r') as f:
    FILE_NAME = json.load(f)
P = PARAMETER_META
F = FILE_NAME

class Simulation():
    """The simulation object provides a wrapper for RHESSys simulations"""

    def __init__(self, executable, path, initialize=True):
        """Initialize a new simulation object"""
        self.executable = executable
        self.model_path = Path(os.path.abspath(path))
        self.clim = self.model_path / 'clim'
        self.defs = self.model_path / 'defs'
        self.flows = self.model_path / 'flows'
        self.obs = self.model_path / 'obs'
        self.output = self.model_path / 'output'
        self.tecfiles = self.model_path / 'tecfiles'
        self.worldfiles = self.model_path / 'worldfiles'
        self.config_path = self.model_path.parent / '.rhessys'
        self.status = 'Uninitialized'
        if initialize:
            self.initialize()

    def initialize(self):
        self.status = 'Initialized'

    def _gen_rhessys_cmd(self, run_suffix, processes=1, prerun_cmds=[],
                       startGRU=None, countGRU=None, iHRU=None,
                       freq_restart=None, progress='m'):
        
        rhessys_run_cmd = ''.join(['./{} -st {} -ed {}'.format(P['version'], P['start_date'], P['end_date']),
                           ' -b -newcaprise -capr {} -gwtoriparian -capMax {}'.format(P['capr'], P['capMax']),
                           ' -slowDrain -leafDarkRespScalar {}'.format(P['leafDarkRespScalar']),
                           ' -frootRespScalar {} -StemWoodRespScalar {}'.format(P['frootRespScalar'],P['StemWoodRespScalar']),
                           ' -t tecfiles{} -w worldfiles{} -whdr worldfiles{}'.format(F['tecfiles'],F['worldfiles1'],F['worldfiles2']),
                           ' -r flows{} -rtz {}'.format(F['flows'], P['rtz']),
                           ' -pre output{} -s {} {} {} -sv {} {} -gw {} {}'.format(F['prefix'], P['rtz'], P['s1'], P['s2'], P['s3'], P['sv1'], P['sv2'], P['gw1'], P['gw2'])                          
                          ])
        return rhessys_run_cmd

    def _run_local(self, run_suffix, processes=1, prerun_cmds=None,
                   startGRU=None, countGRU=None, iHRU=None, freq_restart=None,
                   progress=None):
        """Start a local simulation"""
        run_cmd = self._gen_rhessys_cmd(run_suffix, processes, prerun_cmds,
                                      startGRU, countGRU, iHRU, freq_restart,
                                      progress)
        run_cmd = shlex.split(run_cmd)
        process = subprocess.Popen(run_cmd, stdout=subprocess.PIPE)
        output = process.communicate()[0].decode('utf-8')
        self.status = 'Running'

    def start(self, run_option,  run_suffix='pysumma_run', processes=1,
              prerun_cmds=[], startGRU=None, countGRU=None, iHRU=None,
              freq_restart=None, progress=None):
        """Run a RHESSys simulation"""
        #TODO: Implement running on hydroshare here
        if not prerun_cmds:
            prerun_cmds = []
        self.run_suffix = run_suffix
        if run_option == 'local':
            self._run_local(run_suffix, processes, prerun_cmds,
                            startGRU, countGRU, iHRU, freq_restart, progress)
        elif run_option == 'docker':
            self._run_docker(run_suffix, processes, prerun_cmds,
                             startGRU, countGRU, iHRU, freq_restart, progress)
        else:
            raise NotImplementedError('Invalid runtime given! '
                                      'Valid options: local, docker')

    def run(self, run_option,  run_suffix='rhessys_run', processes=1,
            prerun_cmds=None, startGRU=None, countGRU=None, iHRU=None,
            freq_restart=None, progress=None):
        self.start(run_option, run_suffix, processes, prerun_cmds,
                   startGRU, countGRU, iHRU, freq_restart, progress)