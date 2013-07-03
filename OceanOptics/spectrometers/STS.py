# -*- coding: utf-8 -*-
""" File:           STS.py
    Author:        Jose A. Jimenez-Berni
    Last change:    2013/05/20

    Python Interface for STS OceanOptics Spectometers.
    Current device classes:
        * STS
"""

#----------------------------------------------------------
import usb.core
import struct
from .._defines import OceanOpticsError as _OOError
import numpy as np
import time
#----------------------------------------------------------

class STS(object):
    """ class STS:

            Serial --> serial_number
            acquire_spectrum() --> np.array
            get_device_temperature() --> float Celcius
            set_integration_time(time_us=None) --> sets the ~
            get_integration_time() --> returns  the ~ in us
            set_scan_averages(scan_averages=None) --> sets the ~
            get_scan_averages() --> returns  the ~
            get_irradiance_calibraiton() --> returns float[1024] coef for radiometriometric calibration
    """

    def __init__(self):

        self._dev = usb.core.find(idVendor=0x2457, idProduct=0x4000)
        if self._dev is None:
            raise _OOError('No OceanOptics STS spectrometer found!')
        else:
            print ('*NOTE*: Currently the first device matching the '
                   'Vendor/Product id is used')

        # This information comes from the OEM-Datasheet
        # "http://www.oceanoptics.com/technical"
        #       "/engineering/OEM%20Data%20Sheet%20--%20USB2000+.pdf"
        self._EP1_out = 0x01
        self._EP1_in = 0x81
        self._EP2_in = 0x82
        self._EP2_out = 0x02
        self._EP3_interrupt = 0x83
        self._EP1_in_size = 64
        self._EP2_in_size = 64
        self._EP1_out_size = 64
        self._EP2_out_size = 64


        self._START_BYTES = 0xC0C1
        self._END_BYTES = 0xC2C3C4C5
        self._PROTOCOL_VERSION = 0x0100

        self._MSG_GET_SERIAL = 0x00000100
        self._MSG_GET_SERIAL_LENGHT = 0x00000101

        self._MSG_GET_CORRECTED_SPECTRUM = 0x00101000
        self._MSG_SET_INTEGRATION_TIME = 0x00110010

        self._MSG_GET_HW_VERSION=0x00000080
        self._MSG_GET_SW_VERSION=0x00000090

        self._MSG_GET_AVG_SCANS=0x00110510
        self._MSG_SET_AVG_SCANS=0x00120010

        self._MSG_GET_TEMPERATURE=0x00400001
        self._MSG_GET_ALL_TEMPERATURE=0x00400002

        self._MSG_GET_WAVELENGTH_COEFF_COUNT = 0x00180100
        self._MSG_GET_WAVELENGTH_COEFF = 0x00180101

        self._MSG_GET_NONLINEAR_COEFF_COUNT = 0x00181100
        self._MSG_GET_NONLINEAR_COEFF = 0x00181101

        self._MSG_GET_STRAYLIGHT_COEFF_COUNT = 0x00183100
        self._MSG_GET_STRAYLIGHT_COEFF = 0x00183101


        self._MSG_GET_IRRADIANCE_COEFF = 0x00182001


        self._scan_averages = 0


        # This part makes the initialization a little bit more robust
        self._dev.set_configuration()


        # This empties the USB buffer
        self._initialize()

        print "HW Version: %i" % self._get_hw_version()
        print "SW Version: %i" % self._get_sw_version()
        self.Serial = self._get_serial()
        print "Serial: %s" % self.Serial
        self.set_integration_time(10000) # sets self._it
        self.set_scan_averages(10)
        self._request_spectrum()
        self._wl = self._get_wavelength_calibration()
        self._nl = self._get_nonlinearity_calibration()
        self._sl = self._get_stray_light_calibration()


        # Make sure everything is working
        for i in range(10):
            try:
                self._request_spectrum()
                break
            except: pass
        else: raise _OOError('Initialization SPECTRUM')

    def set_integration_time(self, time_us):
        if not (time_us is None):
            self._set_integration_time(time_us)

    def get_integration_time(self):
        return self._it

    def set_scan_averages(self, scan_averages):
        if not (scan_averages is None):
            self._set_scan_averages(scan_averages)

    def get_scan_averages(self):
        return self._scan_averages

    def get_device_temperature(self):
        """Returns the temperature of the detector"""
        temperatures = self._read_temperatures()
        return temperatures[0]

    def get_irradiance_calibration(self):
        return self._read_irradiance_calibration()

    def acquire_spectrum(self):
        raw_intensity = np.array(self._request_spectrum(), dtype=np.float)
        nl_coeffs = len(self._nl)
        wavelength = sum( self._wl[i] * np.arange(1024)**i for i in range(4) )
        # fixed linearization, see documentation at:
        # --> http://www.oceanoptics.com/technical/OOINLCorrect%20Linearity%20Coeff%20Proc.pdf
        intensity =  raw_intensity / sum( self._nl[i] * raw_intensity**i for i in range(nl_coeffs) )
        return np.vstack([wavelength, intensity])


    def acquire_radiance_spectrum(self):
        raise NotImplementedError


    #-----------------------------
    # The user doesn't need to see this
    #-----------------------------
    def _initialize(self):
        """ Empty USB buffer """
        print "Initilizing"
        while(True):
            try:
                self._dev.read(self._EP1_in, self._EP1_in_size)
            except:
                break
        #self._dev.write(self._EP1_out, struct.pack('<B', 0x01))


    def _get_serial(self):

        serial_leght = int(self._query_coefficient_count(self._MSG_GET_SERIAL_LENGHT))
        print "Serial length: %i" % serial_leght

        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_SERIAL,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)
        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBB16sL16sL', ret)
            if ack[3] == 0:
                return str(ack[9]).replace('\0','')
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1


        return "Not Yet!"

    def _get_hw_version(self):
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_HW_VERSION,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBBB15sL16sL', ret)
            if ack[3] == 0:
                return ack[9]
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1

    def _get_sw_version(self):
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_SW_VERSION,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBBB15sL16sL', ret)
            if ack[3] == 0:
                return ack[9]
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1


    def _set_integration_time(self, time_us):
        """
        Sets the integration time in us.

        :param time_us: Integration time in us.
        :returns: The actual integration time returned by the spectrometer or -1 in case of error

        """


        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBBL12sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_SET_INTEGRATION_TIME,0x00000000,0x00000000,0x0000,0x00,0x04,time_us,'',\
        0x14,'',self._END_BYTES))

        try:
            ret = self._dev.read(self._EP1_in, self._EP1_in_size)
            if len(ret) == 64:
                ack = struct.unpack('<HHHHLL6sBBL12sL16sL', ret)
                if ack[3] == 0:
                    time_us = ack[9]
                    print "Error setting integration time"
                    return -1
                else:
                    print "Error code: %i" % ack[3]
                    return -1
            else:
                print "Unexpected msg lenght: %i vs 64" % len(ret)
                return -1
        except Exception:
            #No error message
            self._it = time_us

    def _set_scan_averages(self, scan_averages):
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBBH14sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_SET_AVG_SCANS,0x00000000,0x00000000,0x0000,0x00,0x02,scan_averages,'',\
        0x14,'',self._END_BYTES))

        try:
            ret = self._dev.read(self._EP1_in, self._EP1_in_size)
            if len(ret) == 64:
                ack = struct.unpack('<HHHHLL6sBBH14sL16sL', ret)
                if ack[3] == 0:
                    print ack[9]
                    print "Error setting integration time"
                    return -1
                else:
                    print "Error code: %i" % ack[3]
                    return -1
            else:
                print "Unexpected msg lenght: %i vs 64" % len(ret)
                return -1
        except Exception:
            #No error message
            self._scan_averages = scan_averages


    def _get_scan_averages(self):
        #TODO: Not working as expected, returns error
        """
        Gets the coefficient count for a given command.

        :param command: E.g. Wavelength calibration, stray light...
        :returns: The value of the coefficient count stored in EEPROM.

        """
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_AVG_SCANS,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBBH14sL16sL', ret)
            if ack[3] == 0:
                return ack[9]
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1


    def _request_spectrum(self):
        """
        Return the spectrum array.

        :returns: An array with 1024 unsigned short elements and the spectral intensity.
        """
        # XXX: 100000 was an arbitary choice. Should probably be a little less than the USB timeout
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_CORRECTED_SPECTRUM,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))

        time.sleep( max((self._it+100000)*self._scan_averages , 0) * 1e-6 )
        ret = [self._dev.read(self._EP1_in, self._EP1_in_size) for _ in range(33)]
        ret = sum(ret[1:], ret[0])

        spectrum = struct.unpack('<HHHHLLLHBB16sL1024H16sL', ret)

        return spectrum[12:1036]


    def _get_wavelength_calibration(self):
        return [float(self._query_coefficient(i,self._MSG_GET_WAVELENGTH_COEFF)) for i in range(4)]

    def _get_nonlinearity_calibration(self):
        nl_coef = int(self._query_coefficient_count(self._MSG_GET_NONLINEAR_COEFF_COUNT))
        if nl_coef != 8:
            # Don't care about this right now
            raise _OOError('This spectrometer has less correction factors')
        return [float(self._query_coefficient(i,self._MSG_GET_NONLINEAR_COEFF)) for i in range(nl_coef)]

    def _get_stray_light_calibration(self):
        sl_coef = int(self._query_coefficient_count(self._MSG_GET_STRAYLIGHT_COEFF_COUNT))

        return [float(self._query_coefficient(i,self._MSG_GET_STRAYLIGHT_COEFF)) for i in range(sl_coef)]


    def _read_irradiance_calibration(self):
        """"
        Return the irradiance calibration stores in the STS.

        :returns: An array with 1024 floating elements.
        """

        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_IRRADIANCE_COEFF,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))

        ret = [self._dev.read(self._EP1_in, self._EP1_in_size) for _ in range(65)]
        ret = sum(ret[1:], ret[0])
        #print "".join('%02x' % i for i in ret)
        spectrum = struct.unpack('<HHHHLLLHBB16sL1024f16sL', ret)
        #print(spectrum[12:1036])
        return spectrum[12:1036]


    def _query_coefficient_count(self, command):
        """
        Gets the coefficient count for a given command.

        :param command: E.g. Wavelength calibration, stray light...
        :returns: The value of the coefficient count stored in EEPROM.

        """
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        command,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBBB15sL16sL', ret)
            if ack[3] == 0:
                return ack[9]
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1


    def _query_coefficient(self, index, command):
        """
        Sets the integration time in us.

        :param index: Index of the coefficient to retrieve.

        :param command: E.g. Wavelength calibration, stray light...
        :returns: The value of the coefficient stored in EEPROM.

        """
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBBB15sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        command,0x00000000,0x00000000,0x0000,0x00,0x01,index,'',\
        0x14,'',self._END_BYTES))
        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        if len(ret) == 64:
            ack = struct.unpack('<HHHHLL6sBBf12sL16sL', ret)
            if ack[3] == 0:
                return ack[9]
            else:
                print "Error code: %i" % ack[3]
                return -1
        else:
            print "Unexpected msg lenght: %i vs 64" % len(ret)
            return -1

    def _read_temperatures(self):
        """
        Reads the sensor temperatures and returns an float array with the.
        [0] is the temperature of the detector
        [1] is the temperature of the controller

        :returns: a float array with two elements.

        """
        self._dev.write(self._EP1_out, struct.pack('<HHHHLLLHBB16sL16sL', \
        self._START_BYTES,self._PROTOCOL_VERSION,0x0000,0x0000,\
        self._MSG_GET_ALL_TEMPERATURE,0x00000000,0x00000000,0x0000,0x00,0x00,'',\
        0x14,'',self._END_BYTES))

        ret = self._dev.read(self._EP1_in, self._EP1_in_size)

        ack = struct.unpack('<HHHHLLLHBB3f4sL16sL', ret)

        return [ack[10],ack[12]]
