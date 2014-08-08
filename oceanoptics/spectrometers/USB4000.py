# -*- coding: utf-8 -*-
""" File:           USB4000.py
    Author:         Ian Ross Williams
    Last change:    2014/08/08

    Python Interface for USB4000 OceanOptics Spectometers.
    Current device classes:
        * USB4000
"""

#----------------------------------------------------------
import struct
import usb.core
import numpy as np
import time
import md5
import warnings
from itertools import chain 

from oceanoptics.defines import OceanOpticsError as _OOError
from oceanoptics.defines import OceanOpticsModelConfig as _OOModelConfig
from oceanoptics.defines import OceanOpticsSpectrumConfig as _OOSpecConfig
from oceanoptics.base    import OceanOpticsSpectrometer as _OOSpec
from oceanoptics.base    import OceanOpticsSpectrometer as _OOSpec
from oceanoptics.base    import OceanOpticsUSBComm as _OOUSBComm
from oceanoptics.defines import OceanOpticsValidPixels as _OOValidPixels
#----------------------------------------------------------

class USB4000(_OOSpec, _OOUSBComm):

    def __init__(self):
        super(USB4000, self).__init__('USB4000')

        self._EPout = _OOModelConfig['USB4000']['EPout']
        self._EPin0 = _OOModelConfig['USB4000']['EPin0']
        self._EPin1 = _OOModelConfig['USB4000']['EPin1']
        self._EPin2 = _OOModelConfig['USB4000']['EPin2']
        self._EPin6 = _OOModelConfig['USB4000']['EPin6']
        self._EPin0_size = _OOModelConfig['USB4000']['EPin0_size']
        self._EPin1_size = _OOModelConfig['USB4000']['EPin1_size']
        self._EPin2_size = _OOModelConfig['USB4000']['EPin2_size']
        self._EPin6_size = _OOModelConfig['USB4000']['EPin6_size']

        self._initialize()

        status = self._init_robust_status()
        self._usb_speed = status['usb_speed']
        self._integration_time = status['integration_time']
        self._pixels = status['pixels']
        self._packet_N, self._packet_size, self._packet_func = (
                _OOSpecConfig['USB4000'][self._usb_speed] )

        self._init_robust_spectrum()

        # XXX: differs for some spectrometers...
        #self._sat_factor = 65535.0/float(
        #      stuct.unpack('<h', self._query_information(17, raw=True)[6:8])[0])
        self._wl_factors = [float(self._query_information(i)) for i in range(1,5)]
        self._nl_factors = [float(self._query_information(i)) for i in range(6,14)]
        self._wl = sum( self._wl_factors[i] *
              np.arange(self._pixels, dtype=np.float64)**i for i in range(4) )
        self._valid_pixels = _OOValidPixels['USB4000']

    def __repr__(self):
        rtn  = "USB4000 status:\n"
        rtn += "  USB speed = %d\n" % (self._usb_speed)
        rtn += "  Integration time = %dus\n" % (self._integration_time)
        rtn += "  Pixels = %d\n" % (self._pixels)
        rtn += "  End points = 1:%x 2:%x 6:%x\n" % (self._EPin1, self._EPin2, self._EPin6)
        rtn += "  Number of packets per scan = %d" % (self._packet_N)
        rtn += "  Packet size = %d\n" % (self._packet_size)
        return rtn

    #---------------------
    # High level functions
    #---------------------

    def wavelengths(self, only_valid_pixels=True):
        """returns array of wavelengths

        Parameters
        ----------
        only_valid_pixels : bool, optional
            only optical active pixels are returned.

        Returns
        -------
        wavelengths : ndarray
            wavelengths of spectrometer
        """
        if only_valid_pixels:
            return self._wl[self._valid_pixels]
        else:
            return self._wl

    def intensities(self, raw=False, only_valid_pixels=True,
            correct_nonlinearity=True, correct_darkcounts=True,
            correct_saturation=True ):
        """returns array of intensities

        Parameters
        ----------
        raw : bool, optional
            does nothing yet.
        only_valid_pixels : bool, optional
            only optical active pixels are returned.
        correct_nonlinearity : bool, optional
            does nothing yet.
        correct_darkcounts : bool, optional
            does nothing yet.
        correct_saturation : bool, optional
            does nothing yet.

        Returns
        -------
        intensities : ndarray
            intensities of spectrometer.
        """
        if only_valid_pixels:
            data = np.array(self._request_spectrum()[self._valid_pixels], dtype=np.float64)
        else:
            data = np.array(self._request_spectrum(), dtype=np.float64)
        return data

    def spectrum(self, raw=False, only_valid_pixels=True,
            correct_nonlinearity=True, correct_darkcounts=True,
            correct_saturation=True):
        """returns array of wavelength and intensities

        Parameters
        ----------
        raw : bool, optional
            does nothing yet.
        only_valid_pixels : bool, optional
            only optical active pixels are returned.
        correct_nonlinearity : bool, optional
            does nothing yet.
        correct_darkcounts : bool, optional
            does nothing yet.
        correct_saturation : bool, optional
            does nothing yet.

        Returns
        -------
        spectrum : ndarray
            wavelengths and intensities of spectrometer.
        """
        return np.vstack((self.wavelengths(only_valid_pixels=only_valid_pixels),
                          self.intensities(raw=raw,
                                only_valid_pixels=only_valid_pixels,
                                correct_nonlinearity=correct_nonlinearity,
                                correct_darkcounts=correct_darkcounts,
                                correct_saturation=correct_saturation)))

    def integration_time(self, time_sec=None):
        """get or set integration_time in seconds
        """
        if not (time is None):
            time_us = time_sec * 1000000
            self._set_integration_time(time_us)
        self._integration_time = self._query_status()['integration_time']*1e-6
        return self._integration_time


    #---------------------
    # helper functions.
    #---------------------

    def _init_robust_status(self):
        for i in range(10):
            try:
                status = self._query_status()
                break
            except usb.core.USBError: pass
        else: raise _OOError('Initialization USBCOM')
        return status

    def _init_robust_spectrum(self):
        self.integration_time(1000)
        for i in range(10):
            try:
                self._request_spectrum()
                break
            except: raise
        else: raise _OOError('Initialization SPECTRUM')


    #---------------------
    # Low level functions.
    #---------------------

    def _initialize(self):
        """ send command 0x01 """
        self._usb_send(struct.pack('<B', 0x01))

    def _set_integration_time(self, time_us):
        """ send command 0x02 """
        self._usb_send(struct.pack('<BI', 0x02, int(time_us)))

    def _query_information(self, address, raw=False):
        """ send command 0x05 """
        ret = self._usb_query(struct.pack('<BB', 0x05, int(address)))
        if bool(raw): return ret
        if ret[0] != 0x05 or ret[1] != int(address)%0xFF:
            raise _OOError('query_information: Wrong answer')
        return ret[2:ret[2:].index(0)+2].tostring()

    def _write_information(self):
        raise NotImplementedError

    def _request_spectrum(self):
        self._usb_send(struct.pack('<B', 0x09))
        time.sleep(max(self._integration_time - self._USBTIMEOUT, 0))
        ret = []
        for _ in range(4):
            ret += self._usb_read(epi=self._EPin6, epi_size=self._packet_size)
        for _ in range(self._packet_N - 4):
            ret += self._usb_read(epi=self._EPin2, epi_size=self._packet_size)
        ret = struct.pack('<'+'B'*(self._pixels*2), *ret)
        
        sync = self._usb_read(epi=self._EPin2, epi_size=1)
        if sync[0] != 0x69:
            raise _OOError('request_spectrum: Wrong sync byte')

        spectrum = struct.unpack('<'+'H'*self._pixels, ret)
        spectrum = map(self._packet_func, spectrum)
        return spectrum

    def _query_status(self):
        """ 0xFE query status """
        ret = self._usb_query(struct.pack('<B', 0xFE))
        data = struct.unpack('<HLBBBBBBBBBB', ret[:])
        ret = { 'pixels' : data[0],
                'integration_time' : data[1],
                'lamp_enable' : data[2],
                'trigger_mode' : data[3],
                'acquisition_status' : data[4],
                'packets_in_spectrum' : data[5],
                'power_down' : data[6],
                'packets_in_endpoint' : data[7],
                'usb_speed' : data[10] }
        return ret


