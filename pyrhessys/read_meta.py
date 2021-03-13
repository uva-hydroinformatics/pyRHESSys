import os
import shutil
import pkg_resources

lulc_forest_fraction = pkg_resources.resource_filename(
        __name__, 'meta/lulc_forest_fraction.csv')
lulc_urban_fraction = pkg_resources.resource_filename(
        __name__, 'meta/lulc_urban_fraction.csv')
lulc_difficult_run_fraction = pkg_resources.resource_filename(
        __name__, 'meta/lulc_difficult_run_fraction.csv')
lulc_meadow_creek_fraction = pkg_resources.resource_filename(
        __name__, 'meta/lulc_meadow_creek_fraction.csv')
vegCollection = pkg_resources.resource_filename(
        __name__, 'meta/vegCollection.csv')
soilCollection = pkg_resources.resource_filename(
        __name__, 'meta/soilCollection.csv')
lulcCollectionEC = pkg_resources.resource_filename(
        __name__, 'meta/lulcCollectionEC.csv')
zoneCollection = pkg_resources.resource_filename(
        __name__, 'meta/zoneCollection.csv')
hillCollection = pkg_resources.resource_filename(
        __name__, 'meta/hillCollection.csv')
lulc_1m_va = pkg_resources.resource_filename(
        __name__, 'meta/lulc_1m_va.csv')
lulc_1m_chesapeake = pkg_resources.resource_filename(
        __name__, 'meta/lulc_1m_Chesapeake_Conservancy.csv')
ssurgo_soil_map = pkg_resources.resource_filename(
        __name__, 'meta/ssurgo_download_link.csv')