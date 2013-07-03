
#----------------------------------------------------------
import struct
import time
import usb.core
import warnings
from _defines import OceanOpticsError as _OOError
from _defines import OceanOpticsModelConfig as _OOModelConfig
from _defines import OceanOpticsVendorId as _OOVendorId
#----------------------------------------------------------

class OceanOpticsUSBComm(object):

    def __init__(self, model):
        self._init_usb_connection(model)

    def _usb_init_connection(self, model):
       
        if model not in _OOModelConfig.keys():
            raise _OOError('Unkown OceanOptics spectrometer model: %s' % model)

        vendorId, productId = _OOVendorId, _OOModelConfig[model]['ProductId']
        self._EPout = _OOModelConfig[model]['EPout']
        self._EPin0 = _OOModelConfig[model]['EPin0']
        self._EPin1 = _OOModelConfig[model]['EPin1']
        self._EPin0_size = _OOModelConfig[model]['EPin0_size']
        self._EPin1_size = _OOModelConfig[model]['EPin1_size']

        devices = usb.core.find(findAll=True, 
                        custom_match=lambda d: (d.idVendor=vendorId and
                                                d.idProduct in productId))
        
        try:
            self._dev = devices.pop(0)
        except IndexError:
            raise _OOError('No OceanOptics %s spectrometer found!' % model)
        else:
            if devices: 
                warnings.warn('Currently the first device matching the '
                              'Vendor/Product id is used')
        
        self._dev.set_configuration()

    def _usb_send(self, data, epo=self._EPout):
        """ helper """
        self._dev.write(epi, data)

    def _usb_read(self, epi=self._EPin0, epi_size=self._EPin0_size):
        """ helper """
        return self._dev.read(epi, epi_size)

    def _usb_query(self, data, epo=self._EPout, 
                epi=self._EPin0, epi_size=self._EPin0_size):
        """ helper """
        self._usb_send(data, epo)
        return self._usb_read(epi, epi_size)



class OceanOpticsBase(OceanOpticsUSBComm):
    """ This class implements functionality that is common
    among all supported spectrometers.

    """

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

    def _request_spectra(self):
        raise NotImplementedError

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
        


class OceanOpticsSerialNum(OceanOpticsUSBComm):

    def _write_serial_number(self,):
        raise NotImplementedError

    def _get_serial_number(self,):
        raise NotImplementedError



class OceanOpticsShutdown(OceanOpticsUSBComm):

    def _set_shutdown_mode(self):
        raise NotImplementedError


class OceanOpticsTrigger(OceanOpticsUSBComm):

    def _set_trigger_mode(self):
        raise NotImplementedError
















