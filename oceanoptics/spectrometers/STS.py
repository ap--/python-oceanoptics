# -*- coding: utf-8 -*-
#
# STS spectrometer
# ================
#
# To implement further functionality you basically just need to look at
# the two communication layer functions:
#  self._send_command and self._query_data
#
# based on those you can implement other commands.
# call them with the right message constant in self._const.MSG_...
# and the payload data packed in a string.
#
""" File:           STS.py
    Author:         Jose A. Jimenez-Berni, Andreas Poehlmann
    Last change:    2014/08/15

    Python Interface for STS OceanOptics Spectometers.
    Current device classes:
        * STS
"""

#----------------------------------------------------------
import struct
from oceanoptics.defines import OceanOpticsError as _OOError
from oceanoptics.base import OceanOpticsSpectrometer as _OOSpec
from oceanoptics.base import OceanOpticsUSBComm as _OOUSBComm
import numpy as np
import time
import hashlib
import warnings
#----------------------------------------------------------

class _STSCONSTANTS(object):
    """All relevant constants are stored here"""

    HEADER_START_BYTES = 0xC0C1
    HEADER_PROTOCOL_VERSION = 0x1100  # XXX: this seems to be the newest protocol version!!!

    FLAG_RESPONSE_TO_REQUEST = 0x0001
    FLAG_ACK = 0x0002
    FLAG_REQUEST_ACK = 0x0004
    FLAG_NACK = 0x0008
    FLAG_HW_EXCEPTION = 0x0010
    FLAG_PROTOCOL_DEPRECATED = 0x0020

    ERROR_CODES = {  0: 'Success (no detectable errors)',
                     1: 'Invalid/unsupported protocol',
                     2: 'Unknown message type',
                     3: 'Bad checksum',
                     4: 'Message too large',
                     5: 'Payload length does not match message type',
                     6: 'Payload data invalid',
                     7: 'Device not ready for given message type',
                     8: 'Unknown checksum type',
                     9: 'Device reset unexpectedly',
                    10: 'Too many buses (Commands have come from too many bus interfaces)',
                    11: 'Out of memory. Failed to allocate enough space to complete request.',
                    12: 'Command is valid, but desired information does not exist.',
                    13: 'Int Device Error. May be unrecoverable.',
                   100: 'Could not decrypt properly',
                   101: 'Firmware layout invalid',
                   102: 'Data packet was wrong size',
                   103: 'hardware revision not compatible with firmware',
                   104: 'Existing flash map not compatible with firmware',
                   255: 'Operation/Response Deferred. Operation will take some time to complete. Do not ACK or NACK yet.',
                  }

    NO_ERROR = 0x0000

    RESERVED = ""

    CHECKSUM_TYPE_NONE = 0x00
    CHECKSUM_TYPE_MD5 = 0x01

    NO_CHECKSUM = ""

    FOOTER = 0xC2C3C4C5  # the datasheet specifies it in this order...

    # Generic Device Commands
    MSG_RESET = 0x00000000
    MSG_RESET_DEFAULTS = 0x00000001
    MSG_GET_HARDWARE_REVISION = 0x00000080
    MSG_GET_FIRMWARE_REVISION = 0x00000090
    MSG_GET_SERIAL_NUMBER = 0x00000100
    MSG_GET_DEVICE_ALIAS = 0x00000200
    MSG_GET_DEVICE_ALIAS_LENGTH = 0x00000201
    MSG_SET_DEVICE_ALIAS = 0x00000210
    MSG_GET_NUMBER_USER_STRINGS = 0x00000300
    MSG_GET_USER_STRING_LENGTH = 0x00000301
    MSG_GET_USER_STRING = 0x00000302
    MSG_SET_USER_STRING = 0x00000310
    MSG_GET_RS232_BAUDRATE = 0x00000800
    MSG_GET_RS232_FLOW_CONTROL_MODE = 0x00000804
    MSG_SET_RS232_BAUDRATE = 0x00000810
    MSG_SET_RS232_FLOW_CONTROL_MODE = 0x00000814
    MSG_SAVE_RS232_SETTINGS = 0x000008F0
    MSG_CONFIGURE_STATUS_LED = 0x00001010
    MSG_REPROGRAMMING_MODE = 0x000FFF00

    # Spectrometer Commands
    MSG_GET_AND_SEND_CORRECTED_SPECTRUM = 0x00101000
    MSG_GET_AND_SEND_RAW_SPECTRUM = 0x00101100
    MSG_GET_PARTIAL_SPECTRUM_MODE = 0x00102000
    MSG_GET_AND_SEND_PARTIAL_CORRECTED_SPECTRUM = 0x00102080
    MSG_SET_INTEGRATION_TIME = 0x00110010
    MSG_SET_TRIGGER_MODE = 0x00110110
    MSG_SIMULATE_TRIGGER_PULSE = 0x00110120
    MSG_GET_PIXEL_BINNING_FACTOR = 0x00110280
    MSG_GET_MAXIMUM_BINNING_FACTOR = 0x00110281
    MSG_SET_BINNING_FACTOR = 0x00110290
    MSG_SET_DEFAULT_BINNING_FACTOR = 0x00110295
    MSG_SET_LAMP_ENABLE = 0x00110410
    MSG_SET_TRIGGER_DELAY = 0x00110510
    MSG_GET_SCANS_TO_AVERAGE = 0x00120000
    MSG_SET_SCANS_TO_AVERAGE = 0x00120010
    MSG_GET_BOXCAR_WIDTH = 0x00121000
    MSG_SET_BOXCAR_WIDTH = 0x00121010
    MSG_GET_WAVELENGTH_COEFFICIENT_COUNT = 0x00180100
    MSG_GET_WAVELENGTH_COEFFICIENT = 0x00180101
    MSG_SET_WAVELENGTH_COEFFICIENT = 0x00180111
    MSG_GET_NONLINEARITY_COEFFICIENT_COUNT = 0x00181100
    MSG_GET_NONLINEARITY_COEFFICIENT = 0x00181101
    MSG_SET_NONLINEARITY_COEFFICIENT = 0x00181111
    MSG_GET_IRRADIANCE_CALIBRATION = 0x00182001
    MSG_GET_IRRADIANCE_CALIBRATION_COUNT = 0x00182002
    MSG_GET_IRRADIANCE_CALIBRATION_COLLECTION_AREA = 0x00182003
    MSG_SET_IRRADIANCE_CALIBRATION = 0x00182011
    MSG_SET_IRRADIANCE_CALIBRATION_COLLECTION_AREA = 0x00182013
    MSG_GET_NUMBER_STRAY_LIGHT_COEFFICIENTS = 0x00183100
    MSG_GET_STRAY_LIGHT_COEFFICIENT = 0x00183101
    MSG_SET_STRAY_LIGHT_COEFFICIENT = 0x00183111
    MSG_GET_HOT_PIXEL_INDICES = 0x00186000
    MSG_SET_HOT_PIXEL_INDICES = 0x00186010
    MSG_GET_BENCH_ID = 0x001B0000
    MSG_GET_BENCH_SERIAL_NUMBER = 0x001B0100
    MSG_GET_SLIT_WIDTH_MICRONS = 0x001B0200
    MSG_GET_FIBER_DIAMETER_MICRONS = 0x001B0300
    MSG_GET_FILTER = 0x001B0500
    MSG_GET_COATING = 0x001B0600

    # GPIO commands
    MSG_GET_NUMBER_GPIO_PINS = 0x00200000
    MSG_GET_OUTPUT_ENABLE_VECTOR = 0x00200100
    MSG_SET_OUTPUT_ENABLE_VECTOR = 0x00200110
    MSG_GET_VALUE_VECTOR = 0x00200300
    MSG_SET_VALUE_VECTOR = 0x00200310

    # Strobe commands
    MSG_SET_SINGLE_STROBE_PULSE_DELAY = 0x00300010
    MSG_SET_SINGLE_STROBE_PULSE_WIDTH = 0x00300011
    MSG_SET_SINGLE_STROBE_ENABLE = 0x00300012
    MSG_SET_CONTINUOUS_STROBE_PERIOD = 0x00310010
    MSG_SET_CONTINUOUS_STROBE_ENABLE = 0x00310011

    # Temperature Commands
    MSG_GET_TEMPERATURE_SENSOR_COUNT = 0x00400000
    MSG_READ_TEMPERATURE_SENSOR = 0x00400001
    MSG_READ_ALL_TEMPERATURE_SENSORS = 0x00400002

    HEADER_FMT = ("<H"    # start_bytes
                   "H"    # protocol_version
                   "H"    # flags
                   "H"    # error number
                   "L"    # message type
                   "L"    # regarding
                   "6s"   # reserved
                   "B"    # checksum type
                   "B"    # immediate length
                   "16s"  # immediate data
                   "L"    # bytes remaining
                 )

    FOOTER_FMT = ("16s"  # checksum
                  "L"    # footer
                 )

class STS(_OOSpec, _OOUSBComm):
    """Rewrite of STS class"""

    def __init__(self, integration_time=0.001):
        super(STS, self).__init__('STS')

        self._const = _STSCONSTANTS

        # we can't query this info:
        self._pixels = 1024

        # get wavelengths
        self._wl = self._get_wavelengths()

        # set the integration time
        self._integration_time = self._set_integration_time(integration_time)


    #------------------------------------
    # Implement High level functionality
    #------------------------------------

    def integration_time(self, time_sec=None):
        """get or set the integration_time in seconds

        """
        if time_sec is not None:
            self._integration_time = self._set_integration_time(time_sec)
        return self._integration_time

    def wavelengths(self, *args, **kwargs):
        # TODO: add function paramters
        return self._wl

    def intensities(self, *args, **kwargs):
        # TODO: add function paramters
        return self._request_spectrum()

    def spectrum(self, *args, **kwargs):
        # TODO: add function paramters
        return np.vstack((self._wl, self._request_spectrum()))

    #-----------------
    # low level layer
    #-----------------

    def _set_integration_time(self, time_sec):
        """Sets the integration time in seconds

        """
        integration_time_us = int(time_sec * 1000000)
        self._send_command(self._const.MSG_SET_INTEGRATION_TIME, struct.pack("<L", integration_time_us))
        return integration_time_us * 1e-6


    def _get_wavelengths(self):
        """returns an array of wavelengths for the STS spectrometer

        """
        # Get the numer of wavelength coefficients first
        data = self._query_data(self._const.MSG_GET_WAVELENGTH_COEFFICIENT_COUNT, "")
        N_wlcoeff = struct.unpack("<B", data)[0]

        # Then query the coefficients
        wlcoefficients = []
        for i in range(N_wlcoeff):
            data = self._query_data(self._const.MSG_GET_WAVELENGTH_COEFFICIENT, struct.pack("<B", i))
            wlcoefficients.append(struct.unpack("<f", data)[0])

        # Now, generate the wavelength array
        return sum( wlcoefficients[i] * np.arange(self._pixels, dtype=np.float64)**i for i in range(N_wlcoeff) )

    def _request_spectrum(self):
        """returns the spectrum array.

        """
        # Get all data
        msg = self._construct_outgoing_message(self._const.MSG_GET_AND_SEND_RAW_SPECTRUM, "")
        self._usb_send(msg)
        time.sleep(max(self._integration_time - self._USBTIMEOUT, 0))
        ret = self._usb_read()

        remaining_bytes, checksumtype = self._check_incoming_message_header(ret[:44])
        length_payload_footer = remaining_bytes

        remaining_bytes -= len(ret[44:])

        while True:
            if remaining_bytes <= 0:
                break
            N_bytes = min(remaining_bytes, self._EPin0_size)
            ret += self._usb_read(epi_size=N_bytes)
            remaining_bytes -= N_bytes

        if length_payload_footer != len(ret[44:]):
            raise _OOError("There is a remaining packet length error: %d vs %d" % (remaining_bytes, len(ret[44:])))

        checksum = self._check_incoming_message_footer(ret[-20:])
        if (checksumtype == self._const.CHECKSUM_TYPE_MD5) and (checksum != hashlib.md5(ret[:-20]).digest()):
            # TODO: raise Error
            warnings.warn("The checksums differ, but we ignore this for now.")
        data = self._extract_message_data(ret)

        spectrum = struct.unpack("<%dH" % self._pixels, data)
        return np.array(spectrum, dtype=np.float64)

    #-----------------------------
    # communication functionality
    #-----------------------------

    def _query_data(self, msgtype, payload):
        """recommended query function"""
        msg = self._construct_outgoing_message(msgtype, payload, request_ACK=False)
        ret = self._usb_query(msg)

        remaining_bytes, checksumtype = self._check_incoming_message_header(ret[:44])
        if remaining_bytes != len(ret[44:]):
            raise _OOError("There is a remaining packet length error: %d vs %d" % (remaining_bytes, len(ret[44:])))

        checksum = self._check_incoming_message_footer(ret[-20:])
        if (checksumtype == self._const.CHECKSUM_TYPE_MD5) and (checksum != hashlib.md5(ret[:-20]).digest()):
            # TODO: raise Error
            warnings.warn("The checksums differ, but we ignore this for now.")
        data = self._extract_message_data(ret)
        return data

    def _send_command(self, msgtype, payload):
        """recommended command function"""
        msg = self._construct_outgoing_message(msgtype, payload, request_ACK=True)
        ret = self._usb_query(msg)
        _, checksumtype = self._check_incoming_message_header(ret[:44])
        checksum = self._check_incoming_message_footer(ret[-20:])
        if (checksumtype == self._const.CHECKSUM_TYPE_MD5) and (checksum != hashlib.md5(ret[:-20]).digest()):
            # TODO: raise Error
            warnings.warn("The checksums differ, but we ignore this for now.")
        return

    def _construct_outgoing_message(self, msgtype, payload, request_ACK=False, regarding=None):
        """message layout, see STS datasheet

        """
        if request_ACK == True:
            flags = self._const.FLAG_REQUEST_ACK
        else:
            flags = 0

        if regarding is None:
            regarding = 0

        if len(payload) <= 16:
            payload_fmt = "0s"
            immediate_length = len(payload)
            immediate_data = payload
            payload = ""
            bytes_remaining = 20  # Checksum + footer
        else:
            payload_fmt = "%ds" % len(payload)
            immediate_length = 0
            immediate_data = ""
            bytes_remaining = 20 + len(payload)

        FMT = self._const.HEADER_FMT + payload_fmt + self._const.FOOTER_FMT

        msg = struct.pack(FMT, self._const.HEADER_START_BYTES,
                               self._const.HEADER_PROTOCOL_VERSION,
                               flags,
                               self._const.NO_ERROR,
                               msgtype,
                               regarding,
                               self._const.RESERVED,
                               self._const.CHECKSUM_TYPE_NONE,
                               immediate_length,
                               immediate_data,
                               bytes_remaining,
                               payload,
                               self._const.NO_CHECKSUM,
                               self._const.FOOTER)
        return msg

    def _check_incoming_message_header(self, header):
        """message layout, see STS datasheet

        """
        assert len(header) == 44, "header has wrong length! len(header): %d" % len(header)

        data = struct.unpack(self._const.HEADER_FMT, header)

        assert data[0] == self._const.HEADER_START_BYTES, 'header start_bytes wrong: %d' % data[0]
        assert data[1] == self._const.HEADER_PROTOCOL_VERSION, 'header protocol version wrong: %d' % data[1]

        flags = data[2]
        if flags == 0:
            pass
        if flags & self._const.FLAG_RESPONSE_TO_REQUEST:
            pass  # TODO: propagate?
        if flags & self._const.FLAG_ACK:
            pass  # TODO: propagate?
        if flags & self._const.FLAG_REQUEST_ACK:
            pass  # TODO: only the host should be able to set this?
        if (flags & self._const.FLAG_NACK) or (flags & self._const.FLAG_HW_EXCEPTION):
            error = data[3]
            if error != 0:  # != SUCCESS
                raise _OOError(self._const.ERROR_CODES[error])
            else:
                pass  # TODO: should we do simething here?
        if flags & self._const.FLAG_PROTOCOL_DEPRECATED:
            raise _OOError("Protocol deprecated?!?")

        # msgtype = data[4]
        # regarding = data[5]

        checksumtype = data[7]  # TODO: implement checksums.
        assert checksumtype in [self._const.CHECKSUM_TYPE_NONE, self._const.CHECKSUM_TYPE_MD5], 'the checksum type is unkown: %d' % checksumtype

        # immediate_length = data[8]
        # immediate_data = data[9]
        bytes_remaining = data[10]

        return bytes_remaining, checksumtype

    def _check_incoming_message_footer(self, footer):
        """message layout, see STS datasheet

        """
        assert len(footer) == 20, "footer has wrong length! len(footer): %d" % len(footer)

        data = struct.unpack("<" + self._const.FOOTER_FMT, footer)

        checksum = data[0]
        assert data[1] == self._const.FOOTER, "the device returned a wrong footer: %d" % data[1]

        return checksum

    def _extract_message_data(self, msg):
        """message layout, see STS datasheet

        """
        payload_length = len(msg) - 44 - 20  # - HeaderLength - FooterLength
        assert payload_length >= 0, "the received message was shorter than 64 bytes: %d" % payload_length
        payload_fmt = "%ds" % payload_length
        FMT = self._const.HEADER_FMT + payload_fmt + self._const.FOOTER_FMT

        data = struct.unpack(FMT, msg)

        msgtype = data[4]

        immediate_length = data[8]
        immediate_data = data[9]
        payload = data[11]

        if (immediate_length > 0) and len(payload) > 0:
            raise _OOError("the device returned immediate data and payload data? cmd: %d" % msgtype)
        elif immediate_length > 0:
            return immediate_data[:immediate_length]
        elif payload_length > 0:
            return payload
        else:
            return ""
