Stripes plotting code
=====================

Parallise the calculation by extracting the data sample for each year independently:

.. literalinclude:: ../../../../analyses/stripes/TMP2m/ensemble_mean/get_slice.py

And then running that script for each year as a separate task:

.. literalinclude:: ../../../../analyses/stripes/TMP2m/ensemble_mean/make_all_slices.py

Then assemble the slices to make the figure:

.. literalinclude:: ../../../../analyses/stripes/TMP2m/ensemble_mean/stripes.py

