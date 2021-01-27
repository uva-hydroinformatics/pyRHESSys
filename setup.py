from setuptools import setup, find_packages
#import versioneer

setup(name='pyrhessys',
      version = '0.0.5',
      description='an Object-Oriented Python wrapper for the RHESSys model',
      url='https://github.com/DavidChoi76/pyrhessys.git',
      author='YoungDon Choi', 
      author_email='choiyd1115@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.11.2',  
          'xarray>=0.15.0',
          'pandas',
          'netcdf4>=1.2.5',
          'numba',          
          'scipy',          
          'matplotlib',
          'hs_restclient',
          'dask',
          'distributed',
          'toolz',
          'pytest',
          'dask-jobqueue',
          'hydroeval',
          'imageio',
          'sklearn',
          'pyDOE',
          'ipyplot',
          'bs4'
          ],
       extras_require={'visualization': [
          'geopandas',
          'fiona',
          'cartopy',
          'shapely',
          'seaborn',
          'geoviews'       
          ],},
      include_package_data=True,
      test_suite='pyrhessys.tests')