# pyRHESSys

pyRHESSys (Python-the Regional Hydro-Ecologic Simulation System) is an Object-Oriented Python wrapper for the model input creation and manipulation, model execution, model output visualization and analysis.

* [RHESSys Website at GitHub ](https://github.com/RHESSys)
* [RHESSys Website - Naomi Tague ](http://fiesta.bren.ucsb.edu/~rhessys/)

## pyRHESSys is intended to

 - Get and set model input
 - Run the RHESSys Model on local computers and scientific cyberinfrastructures (especially, CUAHSI JupyterHub and CyberGIS for water) 
 - Visualize RHESSys outputs
 - Be integrated with pyRHESSys with Jupyter Notebook environment 
 - Interact with Hydorshare to download RHESSys test cases and upload RHESSys outputs
 - Create model input using GRASS GIS and R library (in progress)
 - Automate model calibration or sensitivity analysis (Future work)
 
## Installation and Usage

#### pyRHESSys requires Python 3.7 and the following packages :

 - xarray : N-D labeled arrays and datasets in python
 - numpy : the fundamental package for scientific computing with Python
 - matplotlib : a Python 2D plotting library 
 - seaborn : statistical data visualization 
 - jupyterthemes : select and install a Jupyter notebook theme
 - hs-restclient : HydroShare REST API python client library
 - pandas
 - geopandas : an open source project to make working with geospatial data in python easier
 - shapely : a BSD-licensed Python package for manipulation and analysis of planar geometric objects
 - distributed :a lightweight library for distributed computing using Dask in Python
 - fiona : Python library to help integrating geographic information systems with other computer systems
 - hydroeval : an open-source evaluator for streamflow time series in Python
     
## Download and Install pyRHESSys (local computers):

**1.)**  Download pyRHESSys
```python
~/Downloads$ git clone https://github.com/DavidChoi76/pyRHESSys.git
```
        
**2.)**  Go to the pyRHESSys directory, where you will see the file setup.py, and use the following command to install pyRHESSys.
```python
~/Downloads/pyRHESSys pip install .
```

## Examples of manipulating and running pyRHESSys :

Refereed document : RHESSys: Regional Hydro-Ecologic Simulation System—An ObjectOriented Approach to Spatially Distributed Modeling of Carbon, Water, and Nutrient Cycling (http://fiesta.bren.ucsb.edu/~rhessys/setup/downloads/files/RHESSysTagueEA2004.pdf.

**(Test Case)** [RHESSys input data of Coweeta subbasin18](https://www.hydroshare.org/resource/6e34c42af35a4f51b1642de70ed6af95/) 

**(Jupyter Notebook)** [Jupyter Notebook for RHESSys to train pyRHESSys, Example: Coweeta subbasin18](https://www.hydroshare.org/resource/9c2c5df86f1a48c0a57c1d142b4dc9a4/)
         
## Bugs
  Our issue tracker is at https://github.com/DavidChoi76/pyRHESSys/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

## License
  Distributed with a MIT license; see LICENSE.txt::

  Copyright (C) 2020 pyRHESSys Developers
  YoungDon Choi <choiyd1115@gmail.com or yc5ef@virginia.edu>
 
