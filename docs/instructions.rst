How to use this dataset
=======================

This document is hard to reproduce, as it uses on pre-release data, which is not widely available. 

This document is kept under version control in a `git repository <https://en.wikipedia.org/wiki/Git>`_. The repository is hosted on `GitHub <https://github.com/>`_ (and the documentation made with `GitHub Pages <https://pages.github.com/>`_). The repository is `<https://github.com/oldweather/20CRv3-diagnostics>`_. This repository contains everything you need to reproduce or extend this work **except** the 20CRv3 data, which is not yet released.

If you are familiar with GitHub, you already know `what to do <https://github.com/oldweather/20CRv3-diagnostics>`_: If you'd prefer not to bother with that, you can download the whole dataset as `a zip file <https://github.com/oldweather/20CRv3-diagnostics/archive/master.zip>`_.

To re-run the scripts included, first install three packages this depends on:

- `IRData <http://brohan.org/IRData/>`_ which provides access to the reanalysis data used,
- `Meteographica <https://brohan.org/Meteorographica/>`_ for plotting weather maps,
- `The DWR dataset <https://oldweather.github.io/DWR/>`_ containing the newly-digitised British Isles observations.

Then install the libraries included in this package:

.. code-block:: sh

   python setup.py install --user

If you reuse this, please let me know, by `raising an issue <https://github.com/oldweather/20CRv3-diagnostics/issues/new>`_. You are not obliged to do this, but it would help. 

