# pyrhessys

| pyrhessys Links & Badges              |                                                                             |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pyRHESSys Tutorial      |[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/DavidChoi76/rhessys_binder_test.git/master)
| pyRHESSys Documentation      | [![Documentation Status](http://readthedocs.org/projects/pyrhessys/badge/?version=latest)](http://pyrhessys.readthedocs.io/en/latest/?badge=latest) |

pyRHESSys (Python-the Regional Hydro-Ecologic Simulation System) is an Object-Oriented Python wrapper for the model input creation and manipulation, model execution, model output visualization and analysis.

* [RHESSys Website at GitHub ](https://github.com/RHESSys)
* [RHESSys Website - Naomi Tague ](http://fiesta.bren.ucsb.edu/~rhessys/)

pyrhessys provides methods for:
------------

 - Get and set model input
 - Run the RHESSys Model on local computers and scientific cyberinfrastructures (especially, CyberGIS-Jupyter for water) 
 - Visualize RHESSys outputs (In progress)
 - Be integrated with pyRHESSys with Jupyter Notebook environment 
 - Interact with Hydorshare to download RHESSys test cases and upload RHESSys outputs
 - Create model input using GRASS GIS and R library (in progress)
 - Automate model calibration or sensitivity analysis (Future work)
 
Installation
------------

pyrhessys can be installed from `pip`.

To install via `pip` use:

```pip install pyrhessys```

rhessys can be installed from 'conda'

To install via 'conda' use:

```conda install -c conda-forge rhessysec```

Installing pyrhessys from source
------------------------------

Installing pyrhessys from source can be useful for developing new features. This can be accomplished by
running:

    git clone https://github.com/DavidChoi76/pyrhessys.git
    cd pyrhessys
    conda env create -f environment.yml
    python -m ipykernel install --user --name=pyrhessys
    pip install .

        
## Bugs
  Our issue tracker is at https://github.com/DavidChoi76/pyrhessys/issues.
  Please report any bugs that you find.  Or, even better, fork the repository on
  GitHub and create a pull request.  All changes are welcome, big or small, and we
  will help you make the pull request if you are new to git
  (just ask on the issue).

## License
  Distributed with a MIT license; see LICENSE.txt::

  Copyright (C) 2020 pyrhessys Developers
  YoungDon Choi <choiyd1115@gmail.com or yc5ef@virginia.edu>
 
