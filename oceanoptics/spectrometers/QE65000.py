# XXX: untested
#----------------------------------------------------------
from __future__ import print_function
import struct
from oceanoptics.base import OceanOpticsBase as _OOBase
import time
#----------------------------------------------------------


class QE65000(_OOBase):

    def __init__(self):
        super(QE65000, self).__init__('QE65000')
        print('TEC temperature: ' + str(self._set_TEC_temperature(-18)))


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
