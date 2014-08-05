

from oceanoptics.base import OceanOpticsSpectrometer as _OOSpec
import numpy as np
import time
#----------------------------------------------------------


class Dummy(_OOSpec):

    def __init__(self):
        self._integration_time = 0.01
        print 'Dummy class initialized'

    def wavelengths(self, only_valid_pixels=True):
        """ returns a np.array with wavelenghts in nm """
        return np.linspace(200, 900, num=1024)

    def intensities(self, raw=False, only_valid_pixels=True,
            correct_nonlinearity=True, correct_darkcounts=True,
            correct_saturation=True ):
        """ returns a np.array with all intensities """
        data = np.random.random_integers(2400, 2600, 1024)
        data = np.array(data, dtype=np.float)
        time.sleep(self._integration_time)
        return data

    def spectrum(self, raw=False, only_valid_pixels=True,
            correct_nonlinearity=True, correct_darkcounts=True,
            correct_saturation=True ):
        """ returns a 2d np.array with all wavelengths and intensities """
        return np.vstack((self.wavelengths(only_valid_pixels),
                          self.intensities(raw, only_valid_pixels, correct_nonlinearity, correct_darkcounts, correct_saturation)))

    def integration_time(self, time_sec=None):
        self._integration_time = time_sec
        return self._integration_time

