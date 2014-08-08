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
import time

from oceanoptics.defines import OceanOpticsError as _OOError
from oceanoptics.defines import OceanOpticsModelConfig as _OOModelConfig
#----------------------------------------------------------

class USB4000(_OOBase):

    def __init__(self):
        super(USB4000, self).__init__('USB4000')

        self._EPin2 = _OOModelConfig['USB4000']['EPin2']
        self._EPin6 = _OOModelConfig['USB4000']['EPin6']
        self._EPin2_size = _OOModelConfig['USB4000']['EPin2_size']
        self._EPin6_size = _OOModelConfig['USB4000']['EPin6_size']


    def __repr__(self):
        rtn  = "USB4000 status:\n"
        rtn += "  USB speed = %d\n" % (self._usb_speed)
        rtn += "  Integration time = %dus\n" % (self._integration_time)
        rtn += "  Pixels = %d\n" % (self._pixels)
        rtn += "  End points = 1:%x 2:%x 6:%x\n" % (self._EPin1, self._EPin2, self._EPin6)
        rtn += "  Number of packets per scan = %d" % (self._packet_N)
        rtn += "  Packet size = %d\n" % (self._packet_size)
        return rtn


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



