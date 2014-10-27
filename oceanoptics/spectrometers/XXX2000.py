# XXX: USB2000 tested, HR2000 untested
#----------------------------------------------------------
from oceanoptics.base import OceanOpticsBase as _OOBase
from oceanoptics.defines import OceanOpticsError as _OOError
import time
import struct
#----------------------------------------------------------


class _XXX2000(_OOBase):

    def _request_spectrum(self):
        self._usb_send(struct.pack('<B', 0x09))
        time.sleep(max(self._integration_time - self._USBTIMEOUT, 0))
        ret = [ self._usb_read(epi=self._EPspec, epi_size=self._packet_size)
                            for _ in range(self._packet_N) ]
        ret = sum( ret[1:], ret[0] )

        # XXX: This sorts the the packets in the right order
        sorted_ret = []
        for j in range(0, self._packet_N, 2):
            for i in range(self._packet_size):
                sorted_ret.append(chr(ret[j*self._packet_size + i]))
                sorted_ret.append(chr(ret[(j+1)*self._packet_size + i]))
        ret = "".join(sorted_ret)

        sync = self._usb_read(epi=self._EPspec, epi_size=1)
        if sync[0] != 0x69:
            raise _OOError('request_spectrum: Wrong sync byte')
        spectrum = struct.unpack('<'+'H'*self._pixels, ret)
        spectrum = map(self._packet_func, spectrum)
        return spectrum




class USB2000(_XXX2000):

    def __init__(self):
        super(USB2000, self).__init__('USB2000')

    def _set_integration_time(self, time_us):
        """ send command 0x02 """
        # XXX: The USB2000 requires the time set in Milliseconds!
        #      This overides the provided function of OOBase
        time_ms = int(time_us/1000)
        self._usb_send(struct.pack('<BI', 0x02, time_ms))

    def _query_status(self):
        """ 0xFE query status """
        # XXX: The USB2000 also returns the time in Milliseconds!
        #      This overides the provided function of OOBase
        #      and pretends to return us
        # XXX: query status does not actually return the usb_speed,
        #      but we return 0x00 to use the abstraction in OOBase

        ret = self._usb_query(struct.pack('<B', 0xFE))
        # XXX: Error in the manual! Byteorder seems to be bigendian
        data = list(struct.unpack('>HHBBBBBBBBBBBB', ret[:]))
        ret = { 'pixels' : data[0],
                'integration_time' : data[1] * 1000,  # ms to us
                'lamp_enable' : data[2],
                'trigger_mode' : data[3],
                'acquisition_status' : data[4],
                'timer_swap' : data[5],
                'spectral_data_density' : data[6],
                'packets_in_endpoint' : 64,
                'usb_speed' : 0x80 # This is a workaround to leave
                                   # OOBase unchanged. This way
                                   # self._EPspec gets set to 0x82 
                                   # TODO: change abstraction layer
              }
        return ret



class HR2000(_XXX2000):

    def __init__(self):
        super(HR2000, self).__init__('HR2000')

    def _set_integration_time(self, time_us):
        """ send command 0x02 """
        # XXX: The HR2000 requires the time set in Milliseconds!
        #      This overides the provided function of OOBase
        # XXX: We also need to save the integration time internally
        #      because it does not support the _qeury_status command
        time_ms = int(time_us/1000)
        self._integration_time = time_ms / 1000.
        self._usb_send(struct.pack('<BI', 0x02, time_ms))

    def _query_status(self):
        """ 0xFE query status """
        # XXX: The HR2000 also returns the time in Milliseconds!
        #      This overides the provided function of OOBase
        #      and pretends to return us
        # XXX: query status does not actually return the usb_speed,
        #      but we return 0x00 to use the abstraction in OOBase
        _integration_time = getattr(self, '_integration_time', None)
        if _integration_time is not None:
            _integration_time *= 1000000
        ret = { 'pixels' : 2048,
                'integration_time' : _integration_time,
                'lamp_enable' : 0,
                'trigger_mode' : 0,
                'acquisition_status' : 0,
                'packets_in_spectrum' : 0,
                'power_down' : 0,
                'packets_in_endpoint' : 0,
                'usb_speed' : 0x80 # This is a workaround to leave
                                   # OOBase unchanged. This way
                                   # self._EPspec gets set to 0x82 
                                   # TODO: change abstraction layer
              }
        return ret
        
        
        
class USB650(_XXX2000):

    def __init__(self):
        super(USB650, self).__init__('USB650')

    def _set_integration_time(self, time_us):
        """ send command 0x02 """
        # XXX: The USB2000 requires the time set in Milliseconds!
        #      This overides the provided function of OOBase
        time_ms = int(time_us/1000)
        self._integration_time = time_ms * 1e3
        self._usb_send(struct.pack('<BI', 0x02, time_ms))

    def _query_status(self):
        """ 0xFE query status """
        # XXX: The USB2000 also returns the time in Milliseconds!
        #      This overides the provided function of OOBase
        #      and pretends to return us
        # XXX: query status does not actually return the usb_speed,
        #      but we return 0x00 to use the abstraction in OOBase

        ret = self._usb_query(struct.pack('<B', 0xFE))
        # XXX: Error in the manual! Byteorder seems to be bigendian
        data = list(struct.unpack('>HHBBBBBBBBBBBB', ret[:]))
        ret = { 'pixels' : data[0],
                'integration_time' : data[1] * 1000,  # ms to us
                'lamp_enable' : data[2],
                'trigger_mode' : data[3],
                'acquisition_status' : data[4],
                'timer_swap' : data[5],
                'spectral_data_density' : data[6],
                'packets_in_endpoint' : 64,
                'usb_speed' : 0x80 # This is a workaround to leave
                                   # OOBase unchanged. This way
                                   # self._EPspec gets set to 0x82 
                                   # TODO: change abstraction layer
              }
        return ret
