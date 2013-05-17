
#----------------------------------------------------------
import usb.core
import struct
from _defines import OceanOpticsError as _OOError
from _defines import OceanOpticsModelConfig as _OOModelConfig
from _defines import OceanOpticsVendorId as _OOVendorId
import time
#----------------------------------------------------------


class OOBase(object):
    
    def _init_usb_connection(self, model):
       
        if model not in _OOModelConfig.keys():
            raise _OOError('Unkown OceanOptics spectrometer model: %s' % model)

        vendorId, productId = _OOVendorId, _OOModelConfig[model]['ProductId']
        self._EPout = _OOModelConfig[model]['EPout']
        self._EPin0 = _OOModelConfig[model]['EPin0']
        self._EPin1 = _OOModelConfig[model]['EPin1']
        self._EPin0_size = _OOModelConfig[model]['EPin0_size']
        self._EPin1_size = _OOModelConfig[model]['EPin1_size']

        devices = usb.core.find(findAll=True, idVendor=vendorId, idProduct=productId)
        
        try:
            self._dev = devices.pop(0)
        except IndexError:
            raise _OOError('No OceanOptics %s spectrometer found!' % model)
        else:
            if devices: 
                warnings.warn('Currently the first device matching the Vendor/Product id is used')
        
        self._dev.set_configuration()


    def _initialize(self):
        pass

    def _set_integration_time(self):
        pass

    def _query_information(self):
        pass

    def _write_information(self):
        pass

    def _request_spectra(self):
        pass



