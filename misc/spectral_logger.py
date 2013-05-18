# -*- coding: utf-8 -*-
"""
Basic spectral logger test for storing spectra into HDF5 file using pandas

Created on Sat May 18 10:48:48 2013

@author: jim006
"""

import OceanOptics
import time
import pandas
from datetime import datetime

integration_time = 1e6
scan_averages = 5

time_delay = 10
spectra = 10

wl = []
temperatures = []
intensities = {}

sts = OceanOptics.STS()
sp = sts.acquire_spectrum()
wl = sp[0]

sts.set_scan_averages(scan_averages)
sts.integration_time(integration_time)

for i in range(spectra):
    store = pandas.HDFStore('spectral.h5')
    intensities = {}
    current_datetime = datetime.utcnow()
    ts = current_datetime.strftime("D%y_%m_%dT%H_%M_%SZ")
    sp = sts.acquire_spectrum()
    print "Aquiring: %s" % ts
    detector_temperature = sts.device_temperature()
    temperatures.append(detector_temperature)
    intensities[ts] = sp[1]
    spectrum_df = pandas.DataFrame(intensities, index=wl)
    store[ts] = spectrum_df
    store.close()
    time.sleep(time_delay)






