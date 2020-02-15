import itertools
import os
import shutil
from urllib.request import urlretrieve
import subprocess
from hs_restclient import HydroShare


def get_hs_resource(resource_id):
    path = os.getcwd() + '/' + resource_id + '/' + resource_id + '/data/contents/'
    hs = HydroShare()
    hs.getResource(resource_id, destination=os.getcwd(), unzip=True)

    # unpack the simulation archive and remove unncessary files
    hs_resource = os.listdir(path)[0]
    shutil.unpack_archive(path + hs_resource, extract_dir=os.getcwd())
    cmd = "rm -rf " + resource_id
    subprocess.run(cmd, shell=True)
    return hs_resource.split('.')[0]

def product_dict(**kwargs):
    """
    Take a set of dictionary arguments and generate a new set of
    dictionaries that have all combinations of values for each key.
    """
    keys, vals = kwargs.keys(), kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))


class ChainDict(dict):
    """
    A dictionary which instead of overwriting on existing keys,
    will instead store the values in a list.
    """
    def __setitem__(self, key, val):
        newval = [val]
        if key in list(self.keys()):
            oldval = self.__getitem__(key)
            newval = list(set(oldval + newval))
        dict.__setitem__(self, key, newval)
