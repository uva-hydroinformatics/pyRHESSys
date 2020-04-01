from setuptools import setup, find_packages

setup(name='pyRHESSys',
      version='1.0.0',
      description='an Object-Oriented Python wrapper for the RHESSys model',
      url='https://github.com/DavidChoi76/pyRHESSys.git',
      author='YoungDon Choi',
      author_email='choiyd1115@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy>=1.11.2',  
          'xarray>0.10.9',
          'pandas',
          'netcdf4>=1.2.5',
          'numba',          
          'scipy>=0.18.1',          
          'matplotlib',
          'hs_restclient',
          'dask==2.12.0',
          'distributed==1.21.8',
          'toolz',
          'dask-jobqueue',
          'geopandas',
          'hydroeval',
          'imageio'
          ],
      include_package_data=True,
      test_suite='pyRHESSys.tests')
