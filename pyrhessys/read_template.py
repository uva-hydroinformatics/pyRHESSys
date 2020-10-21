import os
import shutil
import pkg_resources

DELINEATION_1 = pkg_resources.resource_filename(
        __name__, 'shell_R/grass_delineation_1.sh')
BASIN_DETERMINE = pkg_resources.resource_filename(
        __name__, 'shell_R/basin_determine.R')
DELINEATION_2 = pkg_resources.resource_filename(
        __name__, 'shell_R/grass_delineation_2.sh')
ZONE_CLUSTER = pkg_resources.resource_filename(
        __name__, 'shell_R/zone_cluster.R')
SSURGO_FULLEXTRACTION_STEP1 = pkg_resources.resource_filename(
        __name__, 'shell_R/ssurgo_fullextraction_step1.R')
SSURGO_FULLEXTRACTION_STEP2 = pkg_resources.resource_filename(
        __name__, 'shell_R/ssurgo_fullextraction_step2.R')  
SSURGO_FULLEXTRACTION_STEP3 = pkg_resources.resource_filename(
        __name__, 'shell_R/ssurgo_fullextraction_step3.R')
AGGREGATE_LULCFRAC = pkg_resources.resource_filename(
        __name__, 'shell_R/aggregate_lulcFrac.R')  
AGGREGATE_LULCFRAC_WRITE2GIS = pkg_resources.resource_filename(
        __name__, 'shell_R/aggregate_lulcFrac_write2GIS.R')    
G2W_CF_RHESSYSEC_SOIL_FULLEXTRACTION = pkg_resources.resource_filename(
        __name__, 'shell_R/g2w_cf_RHESSysEC_soil_fullextraction.R')
LIB_RHESSYS_WRITETABLE2WORLD_SOIL_FULLEXTRACTION = pkg_resources.resource_filename(
        __name__, 'shell_R/LIB_RHESSys_writeTable2World_soil_fullextraction.R')
LULC_NLCD_REMOTE_FOREST_CATCHMENT = pkg_resources.resource_filename(
        __name__, 'shell_R/lulc_30m_NLCD_remote_forest_catchment.csv')       
FOREST_COMMUNITY = pkg_resources.resource_filename(
        __name__, 'shell_R/forest_community.sh')     
G2W_TEMPLATE = pkg_resources.resource_filename(
        __name__, 'shell_R/g2w_template.txt')   
LULC_NLCD_URBAN_CATCHMENT = pkg_resources.resource_filename(
        __name__, 'lulc_30m_NLCD_urban_catchment.csv') 
G2W_TEMPLATE1 = pkg_resources.resource_filename(
        __name__, 'shell_R/g2w_template1.txt') 
LANDUSE = pkg_resources.resource_filename(
        __name__, 'shell_R/landuse.sh') 	
LULC_NLCD_DIFFICULT_RUN_CATCHMENT = pkg_resources.resource_filename(
        __name__, 'shell_R/lulc_30m_NLCD_difficult_run_catchment.csv')  		
G2W_TEMPLATE_DIFFICULT_RUN = pkg_resources.resource_filename(
        __name__, 'shell_R/g2w_template_difficult_run.txt') 
LUFRAC_DIFFICULT_RUN = pkg_resources.resource_filename(
        __name__, 'shell_R/landuse_fractions_difficult_run.sh')
LULC_NLCD_MEADOW_CREEK_CATCHMENT = pkg_resources.resource_filename(
        __name__, 'shell_R/lulc_30m_NLCD_Meadow_Creek_catchment.csv')