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
          'numpy',
          'xarray>0.10.9',
          'matplotlib',
          'geopandas',
          'shapely',
          'seaborn',
          'pandas',
          'hs_restclient==1.3.4',
          'distributed',
          'fiona',
          'geoviews',
          'holoviews'
          ],
      include_package_data=True,
      test_suite='pyRHESSys.tests')
