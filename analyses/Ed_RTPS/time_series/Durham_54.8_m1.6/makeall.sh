#!/bin/bash

# Make The timeseries plots for Durham.

export lat='54.8'
export lon='-1.6'

for var in PRMSL PRATE
do
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=3 --var=$var |spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=3 --var=$var |spice_parallel --time=10 --batch=1
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.1 --var=$var |spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.1 --var=$var |spice_parallel --time=10 --batch=1
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.3 --var=$var |spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.3 --var=$var |spice_parallel --time=10 --batch=1
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.5 --var=$var |spice_parallel --time=10 --batch=3
    ../all_values_at_point.py --lat=$lat --lon=$lon --version=4.6.5 --var=$var |spice_parallel --time=10 --batch=1
done

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=4.6.1 --var=PRMSL --yscale=0.01 --startmonth=2 --endmonth=2
mv PRMSL.png V3vV461_Feb_PRMSL.png

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison=4.6.1 --var=PRATE --yscale=1000 --startmonth=2 --endmonth=2
mv PRATE.png V3vV461_Feb_PRATE.png

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison2=4.6.3 --var=PRMSL --yscale=0.01 --startmonth=2 --endmonth=2
mv PRMSL.png V3vV463_Feb_PRMSL.png

../plot_ts_full.py --lat=$lat --lon=$lon --version=3 --comparison2=4.6.3 --var=PRATE --yscale=1000 --startmonth=2 --endmonth=2
mv PRATE.png V3vV463_Feb_PRATE.png

../plot_ts_3ds.py --lat=$lat --lon=$lon --version=3 --comparison=4.6.1 --var=PRMSL --yscale=0.01 --startmonth=1 --endmonth=9 --ymin=980 --ymax=1040
mv PRMSL_3ds.png V3vV461_3ds_PRMSL.png

../plot_ts_full.py --lat=$lat --lon=$lon --version=4.6.1 --comparison=4.6.5 --comparison2=4.6.3 --var=PRMSL --yscale=0.01 --startmonth=2 --endmonth=2
mv PRMSL.png V461+5+3_Feb_PRMSL.png

../plot_ts_3ds.py --lat=$lat --lon=$lon --version=4.6.1 --comparison=4.6.5 --comparison2=4.6.3 --var=PRMSL --yscale=0.01 --startmonth=1 --endmonth=9 --ymin=980 --ymax=1040
mv PRMSL_3ds.png V461+5+3_3ds_PRMSL.png

../plot_ts_3ds.py --lat=$lat --lon=$lon --version=4.6.1 --comparison2=4.6.3 --var=PRMSL --yscale=0.01 --startmonth=1 --endmonth=9 --ymin=980 --ymax=1040
mv PRMSL_3ds.png V461+3_3ds_PRMSL.png
