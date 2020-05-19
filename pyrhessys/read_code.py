import os
import shutil
import pkg_resources

DELINEATION_1 = pkg_resources.resource_filename(
        __name__, 'shell_R/grass_delineation_1.sh')
with open(DELINEATION_1, 'r') as f:
    DELINEATION_1 = f.read()