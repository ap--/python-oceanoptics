

from oceanoptics.base import OceanOpticsBase as _OOBase
import numpy as np
import time
#----------------------------------------------------------


class Dummy(_OOBase):

    def __init__(self):
        self._integration_time = 1000
        print 'Dummy class initialized'

    def _request_spectrum(self):
        spectrum = np.random.random_integers(2400, 2600, (1024))
        spectrum = np.array(spectrum, dtype=np.uint16)
        time.sleep(float(self._integration_time)/1000)
        return spectrum

    def intensities(self, raw=False, only_valid_pixels=True,
                    correct_nonlinearity=True, correct_darkcounts=True,
                    correct_saturation=True):
        data = np.random.random_integers(2400, 2600, (1024))
        data = np.array(data, dtype=np.float)
        time.sleep(float(self._integration_time)/1000)
        return data

    def wavelengths(self, only_valid_pixels=True):
        return np.linspace(200, 900, num=1024)

    def integration_time(self, time_us=None):
        self._integration_time = time_us
        return self._integration_time
