# -*- coding: utf-8 -*-
"""
Basic spectral logger test for storing spectra into HDF5 file using pandas

Created on Sat May 18 10:48:48 2013

@author: jim006
"""

import OceanOptics
import sys, time
import pandas
from datetime import datetime
import atexit
import numpy as np


class spectral_logger(object):

    def __init__(self,  interval_seconds=60):
        self.hd5_store = None
        self.spectrometer = None
        self.acquiring = False
        self.interval_seconds = interval_seconds
        self.wl = None
        self.hdf_filename = None
        self.integration_time = 1e6
        self.scan_averages = 5
        self._init_spectrometer()
        self.setup_spectrometer()

    def _init_spectrometer(self):
        try:
            self.spectrometer = OceanOptics.STS()
            sp = self.spectrometer.acquire_spectrum()
            self.wl = sp[0]
            serial = self.spectrometer.Serial
            self.hdf_filename = serial+'.h5'
        except:
            print "Error opening spectrometer. Exiting..."
            sys.exit(1)

    def setup_spectrometer(self):
        self.spectrometer.set_scan_averages(self.scan_averages)
        self.spectrometer.set_integration_time(self.integration_time)

    def set_integration_time(self, integration_time):
        self.spectrometer.set_integration_time(integration_time)
        self.integration_time = integration_time

    def set_scan_averages(self, scan_averages):
        self.spectrometer.set_scan_averages(scan_averages)
        self.scan_averages = scan_averages

    def measure_spectrum(self):
        self.acquiring = True
        store = pandas.HDFStore(self.hdf_filename)
        intensities = {}
        current_datetime = datetime.utcnow()
        ts = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        ts_index = current_datetime.strftime("D%Y_%m_%dT%H_%M_%SZ")
        sp = self.spectrometer.acquire_spectrum()
        print "Aquiring: %s" % ts_index
        detector_temperature = self.spectrometer.get_device_temperature()
        intensities[ts_index] = sp[1]
        spectrum_df = pandas.DataFrame(intensities, index=self.wl)
        store[ts_index] = spectrum_df
        index_item = {'spectrum_datestamp' : ts, 'spectrum_id' : ts_index, 'detector_temperature' : detector_temperature, 'integration_time_us' : self.integration_time, 'scan_averages' : self.scan_averages}
        df_index = pandas.DataFrame(index_item, index = [0])
        #import pdb; pdb.set_trace()
        if 'spectrum_index' in store:
            df_in_store = store['spectrum_index']
            df_in_store = df_in_store.append(index_item, ignore_index=True)
            store['spectrum_index'] = df_in_store
        else:
            store['spectrum_index'] = df_index
        store.close()
        self.acquiring = False

def clean(logger=None):
    print "clean me"
    if (logger is not None):
        for i in range(10):
            if not logger.acquiring:
                sys.exit(0)
            else:
                time.sleep(1)

def cycle_dc_calibration():
    logger.set_scan_averages(10)
    for integration_time in np.arange(1e5, 5e6, 1e5):
        print "Integrating spectrum for IT: %ims" % (integration_time*1e-3)
        logger.set_integration_time(integration_time)
        logger.measure_spectrum()


if __name__ == "__main__":
    logger = spectral_logger()
    atexit.register(clean, logger)
    while(True):
        cycle_dc_calibration()
        #logger.measure_spectrum()
        time.sleep(logger.interval_seconds)

