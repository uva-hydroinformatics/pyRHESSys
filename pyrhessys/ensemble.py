from copy import deepcopy
from distributed import Client, get_client
import os
import pandas as pd
import time
import xarray as xr
import json
import pkg_resources

from .simulation import Simulation
from .utils import ChainDict, product_dict

OMP_NUM_THREADS = int(os.environ.get('OMP_NUM_THREADS', 1))

PARAMETER = pkg_resources.resource_filename(
        __name__, 'meta/parameter_meta.json')
with open(PARAMETER, 'r') as f:
    PARAMETER_META = json.load(f)

sim_output = []

class Ensemble(object):
    '''
    Ensembles represent an multiple SUMMA configurations based on
    changing the decisions or parameters of a given run.
    '''

    def __init__(self, executable: str,configuration: dict,
                 path: str=None, num_workers: int=1,
                 threads_per_worker: int=OMP_NUM_THREADS,
                 scheduler: str=None):
        """
        Create a new Ensemble object. The API mirrors that of the
        Simulation object.
        """
        self._status = 'Initialized'
        self.executable: str = executable
        self.path: str = path
        self.configuration: dict = configuration
        self.num_workers: int = num_workers
        self.simulations: dict = {}
        self.submissions: list = []
        #self.start_date = PARAMETER_META['start_date']
        #self.end_date = PARAMETER_META['end_date']
        self.parameters = PARAMETER_META

        # Try to get a client, and if none exists then start a new one
        try:
            self._client = get_client()
            # Start more workers if necessary:
            workers = len(self._client.get_worker_logs())
            if workers <= self.num_workers:
                self._client.cluster.scale(workers)
        except ValueError:
            self._client = Client(n_workers=self.num_workers,
                                  threads_per_worker=threads_per_worker)
        self._generate_simulation_objects()

    def _generate_simulation_objects(self):
        """
        Create a mapping of configurations to the simulation objects.
        """
        self.name_list = []
        if self.path:
            for name, config in self.configuration.items():
                self.name = name
                self.name_list.append(self.name)
                self.simulations[name] = Simulation(
                    self.executable, self.path, run_suffix=self.name)
        else:
            for name, config in self.configuration.items():
                assert config['file_manager'] is not None, \
                    "No filemanager found in configuration or Ensemble!"
                self.simulations[name] = Simulation(
                    self.executable, config['file_manager'], run_suffix=self.name)

    def _generate_coords(self):
        """
        Generate the coordinates that can be used to merge the output
        of the ensemble runs into a single dataset.
        """
        parameter_dims = ChainDict()
        for name, conf in self.configuration.items():
            for k, v in conf.get('parameters', {}).items():
                parameter_dims[k] = v
        return {'parameters': parameter_dims}

    def merge_output(self):
        """
        Open and merge all of the output datasets from the ensemble
        run into a single dataset.
        """
        for name_list in self.name_list:
            plot_data = pd.read_csv(self.path + 'output/'+ name_list +'_basin.daily', delimiter=" ")
            date_index = pd.date_range(self.parameters['start_date'][0:10], self.parameters['end_date'][0:10], freq='1D')
            plot_data.insert(loc=0, column='Date', value=date_index[:-1].values)
            plot_data.set_index('Date')
            sim_output.append(plot_data)
        return sim_output

    def start(self, run_option: str):
        """
        Start running the ensemble members.

        Parameters
        ----------
        run_option:
            The run type. Should be either 'local' or 'docker'
        prerun_cmds:
            A list of preprocessing commands to run
        """
        for n, s in self.simulations.items():
            # Sleep calls are to ensure writeout happens
            config = self.configuration[n]
            self.submissions.append(self._client.submit(
                _submit, s, n, run_option, config))

    def run(self, run_option: str, monitor: bool=True):
        """
        Run the ensemble

        Parameters
        ----------
        run_option:
            Where to run the simulation. Can be ``local`` or ``docker``
        prerun_cmds:
            A list of shell commands to run before running SUMMA
        monitor:
            Whether to halt operation until runs are complete
        """
        self.start(run_option)
        if monitor:
            return self.monitor()
        else:
            return True

    def monitor(self):
        """
        Halt computation until submitted simulations are complete
        """
        simulations = self._client.gather(self.submissions)
        
        for s in simulations:
            self.simulations[s.run_suffix] = s

    def summary(self):
        """
        Show the user information about ensemble status
        """
        success, error, other = [], [], []
        for n, s in self.simulations.items():
            if s.status == 'Success':
                success.append(n)
            elif s.status == 'Error':
                error.append(n)
            else:
                other.append(n)
        return {'success': success, 'error': error, 'other': other}

    def rerun_failed(self, run_option: str, monitor: bool=True):
        """
        Try to re-run failed simulations.

        Parameters
        ----------
        run_option:
            Where to run the simulation. Can be ``local`` or ``docker``
        prerun_cmds:
            A list of shell commands to run before running SUMMA
        monitor:
            Whether to halt operation until runs are complete
        """
        run_summary = self.summary()
        self.submissions = []
        for n in run_summary['error']:
            config = self.configuration[n]
            s = self.simulations[n]
            self.submissions.append(self._client.submit(
                _submit, s, n, run_option, config))
            time.sleep(2.0)
        if monitor:
            return self.monitor()
        else:
            return True


def _submit(s: Simulation, name: str, run_option: str, config):
    s.initialize()
    s.apply_config(config)
    s.run(run_option, run_suffix=name)
    s.process = None
    return s

def parameter_product(list_config):
    return {'++'+'++'.join('{}={}'.format(k, v) for k, v in d.items())+'++':
            {'parameters': d} for d in product_dict(**list_config)}
