# tested
# ----------------------------------------------------------
from __future__ import print_function
from ..base import OceanOpticsBase as _OOBase
from ..base import OceanOpticsTEC as _OOTEC
import struct
#----------------------------------------------------------


class QE65000(_OOBase, _OOTEC):
    def __init__(self):
        super(QE65000, self).__init__('QE65000')
        self.initialize_TEC()

    def _set_integration_time(self, time_us):
        """ send command 0x02 """
        # XXX: The QE65000 requires the time set in Milliseconds!
        #      This overides the provided function of OOBase
        time_ms = int(time_us/1000)
        self._usb_send(struct.pack('<BI', 0x02, time_ms))

    def _query_status(self):
        """ 0xFE query status """
        # XXX: The QE65000 also returns the time in Milliseconds!
        #      This overides the provided function of OOBase
        #      and pretends to return us
        ret = self._usb_query(struct.pack('<B', 0xFE))
        data = struct.unpack('<HLBBBBBBBBBB', ret[:])
        ret = { 'pixels' : data[0],
                'integration_time' : data[1] * 1000,  # ms to us
                'lamp_enable' : data[2],
                'trigger_mode' : data[3],
                'acquisition_status' : data[4],
                'packets_in_spectrum' : data[5],
                'power_down' : data[6],
                'packets_in_endpoint' : data[7],
                'usb_speed' : data[10] }
        return ret
