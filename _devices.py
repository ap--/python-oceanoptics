
""" File:           devices.py
    Author:         Andreas Poehlmann
    Last change:    2012/09/04

    Python Interface for OceanOptics Spectometers.
    Current device classes: 
        * USB2000+
"""

#----------------------------------------------------------
import usb.core
import struct
from _defines import OceanOpticsError as _OOError
import numpy as np
import time
#----------------------------------------------------------


class USB2000(object):
    """ class USB2000:
        
            Serial --> serial_number
            acquire_spectrum() --> np.array
            device_temperature() --> float celcius
            integration_time(time_us=None) --> returns / sets the ~
    """
    
    def __init__(self):
        
        self._dev = usb.core.find(idVendor=0x2457, idProduct=0x101E)
        if self._dev is None:
            raise _OOError('No OceanOptics USB2000+ spectrometer found!')
        else:
            print ('*NOTE*: Currently the first device matching the '
                   'Vendor/Product id is used')
        
        # This information comes from the OEM-Datasheet
        # "http://www.oceanoptics.com/technical"
        #       "/engineering/OEM%20Data%20Sheet%20--%20USB2000+.pdf"
        self._EP1_out = 0x01
        self._EP1_in = 0x81
        self._EP2_in = 0x82
        self._EP6_in = 0x86
        self._EP1_in_size = 64
        self._EP2_in_size = 512
        self._EP6_in_size = 512

        # This part makes the initialization a little bit more robust
        self._dev.set_configuration()
        self._initialize()
        #<robust>#
        for i in range(10):
            try:
                self._usbcomm = self._query_status()['usb_speed']
                break
            except usb.core.USBError: pass
        else: raise _OOError('Initialization USBCOM')
        self.integration_time(1000) # sets self._it
        for i in range(10):
            try:
                self._request_spectrum()
                break
            except: pass
        else: raise _OOError('Initialization SPECTRUM')
        #</robust>#

        self._wl = self._get_wavelength_calibration()
        self._nl = self._get_nonlinearity_calibration()
        self._st = self._get_saturation_calibration()
        self.Serial = self._get_serial()


    def integration_time(self, time_us=None):
        if not (time_us is None):
            self._set_integration_time(time_us)
        self._it = self._query_status()['integration_time']
        return self._it

    def device_temperature(self):
        return self._read_pcb_temperature()

    def acquire_spectrum(self):
        raw_intensity = np.array(self._request_spectrum(), dtype=np.float)[20:]
        wavelength = sum( self._wl[i] * np.arange(20,2048)**i for i in range(4) )
        # fixed linearization, see documentation at:
        # --> http://www.oceanoptics.com/technical/OOINLCorrect%20Linearity%20Coeff%20Proc.pdf
        intensity =  raw_intensity / sum( self._nl[i] * raw_intensity**i for i in range(8) ) * self._st
        return np.vstack([wavelength, intensity])


    #-----------------------------
    # The user doesn't need to see this
    #-----------------------------
    def _initialize(self):
        """ 0x01 initialize """
        self._dev.write(self._EP1_out, struct.pack('<B', 0x01))

    def _set_integration_time(self, time_us):
        """ 0x02 set integration time """
        self._dev.write(self._EP1_out, struct.pack('<BI', 0x02, int(time_us)))

    def _query_information(self, address, raw=False):
        """ 0x05 query info """
        self._dev.write(self._EP1_out, struct.pack('<BB', 0x05, int(address)%0xFF))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)
        if bool(raw): return ret
        if ret[0] != 0x05 or ret[1] != int(address)%0xFF:
            raise Exception('query_information: Wrong answer')
        return ret[2:ret[2:].index(0)+2].tostring()

    def _read_register_information(self, address):
        """ 0x6B read register info """
        self._dev.write(self._EP1_out, struct.pack('<BB', 0x6B, int(address)%0xFF))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)
        if ret[0] != int(address)%0xFF:
            raise Exception('read_register_information: Wrong answer')
        return struct.unpack('<h', ret[1:])[0]

    def _read_pcb_temperature(self):
        """ 0x6C read pcb temperature """
        self._dev.write(self._EP1_out, struct.pack('<B', 0x6C))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)
        if ret[0] != 0x08:
            raise Exception('read_pcb_temperature: Wrong answer')
        adc, = struct.unpack('<h', ret[1:])
        return 0.003906*adc

    def _query_status(self):
        """ 0xFE query status """
        self._dev.write(self._EP1_out, struct.pack('<B', 0xFE))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)
        data = struct.unpack('<HLBBBBBBBBBB', ret[:])
        ret = { 'pixels'              : data[0],
                'integration_time'    : data[1],
                'lamp_enable'         : data[2],
                'trigger_mode'        : data[3],
                'acquisition_status'  : data[4],
                'packets_in_spectrum' : data[5],
                'power_down'          : data[6],
                'packets_in_endpoint' : data[7],
                'usb_speed'           : data[10] }
        return ret

    def _request_spectrum(self):
        """ 0x09 request spectra """
        # XXX: 100000 was an arbitary choice. Should probably be a little less than the USB timeout
        self._dev.write(self._EP1_out, struct.pack('<B', 0x09))
        time.sleep( max(self._it - 100000, 0) * 1e-6 )
        if self._usbcomm == 0x80: #HIGHSPEED
            ret = [self._dev.read(self._EP2_in, 512) for _ in range(8)]
        else: # _usbcomm == 0x00  #FULLSPEED
            ret = [self._dev.read(self._EP2_in, 64) for _ in range(64)]
        ret = sum(ret[1:], ret[0])
        spectrum = struct.unpack('<'+'h'*2048, ret)
        sync = self._dev.read(self._EP2_in, 1)
        if sync[0] != 0x69:
            raise _OOError('request_spectrum: Wrong answer')
        return spectrum

    def _get_serial(self):
        return self._query_information(0)

    def _get_wavelength_calibration(self):
        return [float(self._query_information(i)) for i in range(1,5)]

    def _get_nonlinearity_calibration(self):
        if int(self._query_information(14)) != 7:
            # Don't care about this right now
            raise _OOError('This spectrometer has less correction factors')
        return [float(self._query_information(i)) for i in range(6,14)]

    def _get_saturation_calibration(self):
        ret = self._query_information(0x11, raw=True)
        return 65535.0/float(struct.unpack('<h',ret[6:8])[0])



    #-------------------------------------------
    # This stuff is not implemented yet.
    # Don't really need it ...
    #-------------------------------------------
    def _set_strobe_enable_status(self):
        """ 0x03 set strobe enable status """
        raise NotImplementedError

    def _set_shutdown_mode(self):
        """ 0x04 set shutdown mode """
        raise NotImplementedError
    
    def _write_information(self, address):
        """ 0x06 write info """
        raise NotImplementedError

    def _set_trigger_mode(self, mode):
        """ 0x0A set trigger mode """
        raise NotImplementedError
        
    def _query_plugin_num(self):
        """ 0x0B query number of plugin accessories """
        raise NotImplementedError
    
    def _query_plugin_ident(self):
        """ 0x0C query plugin identifiers """
        raise NotImplementedError
    
    def _detect_plugins(self):
        """ 0x0D detect plugins """
        raise NotImplementedError
    
    def _i2c_read(self):
        """ 0x60 I2C read """
        raise NotImplementedError
    
    def _i2c_write(self, data):
        """ 0x61 I2C write """
        raise NotImplementedError

    def _spi_io(self):
        """ 0x62 spi io """
        raise NotImplementedError

    def _write_register_info(self):
        """ 0x6A write register info """
        raise NotImplementedError
    
    def _read_irradiance_calibration(self):
        """ 0x6D read irradiance calib factors """
        raise NotImplementedError
    
    

