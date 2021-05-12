#!/usr/bin/env python3.7

import numpy as np
from pprint import pprint
from typing import List, Dict
from misc import params, prep_data, dbnames, writenc_yr

dbnames: List[str] = dbnames()
for dbname in dbnames:
    kw: Dict[str, str] = params(dbname)
    dset = prep_data(**kw)
    # acumulado anual
    da = dset.precip.sel(time=slice('1981', '2016')) \
        .resample(time='Y').sum(skipna=False)
    # média dos anos
    da = da.mean(dim='time', skipna=False)
    # substitui nan por -999.0
    da.values[np.isnan(da.values)] = -999.0
    fname = f'{dbname}.precip.1981-2016.clim_annual.nc'
    writenc_yr(da.values.reshape(1, da.values.shape[0], da.values.shape[1]),
               da.lat.values, da.lon.values, var_name='precip',
               var_lname='Precipitation', var_unit='mm', fname=fname)
    print(f'\n{fname}\n')
