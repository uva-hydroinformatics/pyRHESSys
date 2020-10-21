import os
import shutil
import pkg_resources

delineation_d8 = pkg_resources.resource_filename(
        __name__, 'sh_code/grass_delineation_d8.sh')
delineation_dinf = pkg_resources.resource_filename(
        __name__, 'sh_code/grass_delineation_dinf.R')
spatial_hierarchy = pkg_resources.resource_filename(
        __name__, 'sh_code/grass_spatial_hierarchy.sh')
lulc_fraction = pkg_resources.resource_filename(
        __name__, 'sh_code/lulc_fraction.sh')