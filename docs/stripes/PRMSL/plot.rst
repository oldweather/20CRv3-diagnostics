Stripes plotting code
=====================

Parallise the calculation by extracting the data sample for each year independently:

.. literalinclude:: ../../../analyses/stripes/PRMSL/ensemble/get_slice.py

And then running that script for each year as a separate task:

.. literalinclude:: ../../../analyses/stripes/PRMSL/ensemble/make_all_slices.py

Then assemble the slices to make the figure:

.. literalinclude:: ../../../analyses/stripes/PRMSL/ensemble/stripes.py

