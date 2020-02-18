# pyRHESSys

The pyRHESSys is an Object-Oriented Python wrapper for the model input creation and manipulation, model execution, model output visualization and analysis of RHESSys model (The Regional Hydro-Ecologic Simulation System).

* [RHESSys Website at GitHub ](https://github.com/RHESSys)
* [RHESSys Website - Naomi Tague ](http://fiesta.bren.ucsb.edu/~rhessys/)

## The pyRHESSys is intended to provide

 - Get and set model input
 - Run RHESsys Model on local and Cloud 
 - Visualize RHESSys outputs
 - Use pyRHESSYS with jupyter notebook environment 
 - Interact Hydorshare to download RHESSys TestCases and upload the output of RHESSys 
 - Create model input using GRASS GIS (in progress)
 - Automate model calibration or sensitivity analysis (Future work)
 
## Installation and Usage

#### pyRHESSys requires Python 3.6 and following packages :

 - xarray 0.10.0 : N-D labeled arrays and datasets in python
 - numpy 1.13.3 : the fundamental package for scientific computing with Python
 - matplotlib 2.1.1 : a Python 2D plotting library 
 - seaborn 0.8.1 : statistical data visualization 
 - jupyterthemes 0.18.3 : select and install a Jupyter notebook theme
 - hs-restclient 1.2.12 : HydroShare REST API python client library
 - ipyleaflet 0.7.1 : A jupyter widget for dynamic Leaflet maps 
 - Linux Environment (VirtualBox 5.2.8)
     
## Download and Install pyRHESSys:

**1.)**  Download pyRHESSys
```python
~/Downloads$ git clone https://github.com/uva-hydroinformatics/pysumma.git
```
        
**2.)**  change directory into pysumma folder same level with setup.py.
```python
~/Downloads/pysumma$ pip install .
```

## Examples of unit test :

**a unit test using unittest library**  

```python
~/Downloads/pysumma$ python setup.py test
```
## Examples of manipulating and running pyRHESSys :

Refereed paper : RHESSys: Regional Hydro-Ecologic Simulation System—An ObjectOriented Approach to Spatially Distributed Modeling of Carbon, Water, and Nutrient Cycling(http://fiesta.bren.ucsb.edu/~rhessys/setup/downloads/files/RHESSysTagueEA2004.pdf.

**(Test Case-1)** [Modeling the Impact of Stomatal Resistance Parameterizations on Total Evapotranspiration 
         in the Reynolds Mountain East catchment using pySUMMA](notebooks/pySUMMA_Test_Case_1.ipynb) 
         
## Bugs
  Our issue tracker is at https://github.com/DavidChoi76/pyRHESSys/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

## License
  Distributed with a MIT license; see LICENSE.txt::

  Copyright (C) 2020 pyRHESSys Developers
  YoungDon Choi <yc5ef@virginia.edu>
 
