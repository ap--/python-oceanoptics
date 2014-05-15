# XXX: untested
#----------------------------------------------------------
from __future__ import print_function
import struct
import usb.core
from ..defines import OceanOpticsError as _OOError
from ..base import OceanOpticsBase as _OOBase
import numpy as np
import time
#----------------------------------------------------------


class QE65000(_OOBase):

    def __init__(self):
        super(QE65000, self).__init__('QE65000')
        print('TEC temperature: ' + str(self._set_TEC_temperature(-18)))


    def _request_spectrum(self):
        self._usb_send(struct.pack('<B', 0x09))
        time.sleep(max(self._integration_time - self._USBTIMEOUT, 0))
        ret = [self._usb_read(epi=self._EPspec, epi_size=self._packet_size)
               for _ in range(self._packet_N)]
        sync = self._usb_read(epi=self._EPspec, epi_size=1)
        ret = ret[0] + ret[1] + ret[2] + ret[3] + ret[4]
        if sync[0] != 0x69:
            raise _OOError('request_spectrum: Wrong sync byte')
        spectrum = struct.unpack('<' + 'H' * self._pixels, ret)
        spectrum = map(self._packet_func, spectrum)
        spectrum = np.array(spectrum, dtype=np.uint16)
        spectrum ^= 0b1000000000000000
        return spectrum

    def intensities(self, raw=False, only_valid_pixels=True,
                    correct_nonlinearity=True, correct_darkcounts=True,
                    correct_saturation=True):
        if only_valid_pixels:
            data = np.array(self._request_spectrum(), dtype=np.float)[10:1034]
        else:
            data = np.array(self._request_spectrum(), dtype=np.float)
        if not raw:
            data = data / sum(self._nl_factors[i] * data ** i for i in range(8))
            # XXX: differs for some spectrometers
            #data *= self._sat_factor
        return data

    def wavelengths(self, only_valid_pixels=True):
        if only_valid_pixels:
            return sum(self._wl_factors[i] * np.arange(1024) ** i for i in range(4))
        else:
            return sum(self._wl_factors[i] * np.arange(self._pixels) ** i for i in range(4))


    def _read_temperatures(self):
        """ 0x6C read pcb temperature """
        self._usb_send(struct.pack('<B', 0x6C))
        ret = self._usb_read()
        if (ret[0] != 0x08) | (ret[0] != 0x08):
            raise Exception('read_temperatures: Wrong answer')
        pcb = struct.unpack('<h', ret[1:3])[0] * 0.003906
        heatsink = struct.unpack('<h', ret[4:6])[0] * 0.003906
        ret = (pcb, heatsink)
        return ret

    def _read_pcb_temperature(self):
        """ just for compatibility with parent class """
        ret = self._read_temperatures()
        return ret[0]

    def _read_TEC_temperature(self):
        """ 072x read TEC temperature """
        self._usb_send(struct.pack('<B', 0x72))
        ret = self._usb_read()
        temp = struct.unpack('<h', ret)[0] / 10  #decode TEC temperature
        return temp

    def _get_TEC_settings(self):
        ret = self._query_information(17, raw=True)
        ret = ret[2:6]  # only use usefull information
        setpoint = struct.unpack('<h', ret[2:4])[0] / 10  # decode TEC setpoint
        ret = (ret[0], ret[1], setpoint)  # (TEC enable, FAN enable, TEC setpoint)
        return ret

    def _set_TEC_temperature(self, temperature):
        print('Initializing TEC')
        self._read_TEC_temperature()  # Read Temp
        self._usb_send(struct.pack('<BBB', 0x71, 0x00, 0x00))
        time.sleep(0.3)  # wait 200ms
        message = struct.pack('>Bh', 0x73, (temperature * 10))
        self._usb_send(message)
        time.sleep(0.3)  # wait 200ms
        self._usb_send(struct.pack('<BBB', 0x70, 0x01, 0x00))
        time.sleep(0.3)  # wait 200ms
        self._usb_send(struct.pack('<BBB', 0x71, 0x01, 0x00))
        print('...')
        time.sleep(2)
        print('TEC initialized')
        return self._read_TEC_temperature()
