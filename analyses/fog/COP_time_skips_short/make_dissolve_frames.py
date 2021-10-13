#!/usr/bin/env python

# Fill in the gaps in the frame list with dissolve transitions.

import os
import glob

files = sorted(
    glob.glob("%s/images/COP_time_skips_short/[0-9]*.png" % (os.getenv("SCRATCH")))
)

for idx in range(len(files) - 1):
    f1 = os.path.basename(files[idx])
    f2 = os.path.basename(files[idx + 1])
    if f1[0:4] != f2[0:4]:
        print(
            ("./make_dissolve_transition.py --startfile=%s " + "--endfile=%s")
            % (f1, f2)
        )
