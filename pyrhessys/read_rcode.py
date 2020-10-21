import os
import shutil
import pkg_resources

basin_extraction = pkg_resources.resource_filename(
        __name__, 'r_code/basin_extraction.R')
zone_cluster = pkg_resources.resource_filename(
        __name__, 'r_code/zone_cluster.R')
ssurgo_properties_extraction1 = pkg_resources.resource_filename(
        __name__, 'r_code/ssurgo_properties_extraction1.R')
ssurgo_properties_extraction2 = pkg_resources.resource_filename(
        __name__, 'r_code/ssurgo_properties_extraction2.R')
ssurgo_properties_extraction3 = pkg_resources.resource_filename(
        __name__, 'r_code/ssurgo_properties_extraction3.R')
patch_lulc_extraction = pkg_resources.resource_filename(
        __name__, 'r_code/patch_lulc_extraction.R')  
lulcFrac_write2gis = pkg_resources.resource_filename(
        __name__, 'r_code/lulcFrac_write2gis.R')   
g2world_def_flow = pkg_resources.resource_filename(
        __name__, 'shell_R/g2world_def_flow.R')
g2world = pkg_resources.resource_filename(
        __name__, 'shell_R/g2world.R')
