
import usb.core
import usb.util
import struct


# oos
#-------------
# handle = oos.open()
# EP1_out 0x01
# EP2_in  0x82
# EP6_in  0x86
# EP1_in  0x81



class scratch_OOS(object):

    def __init__(self):
        
        self.d = usb.core.find(idVendor=0x2457, idProduct=0x101E)
        if self.d is None:
            raise Exception('No OceanOptics USB2000+ spectrometer found!')
        else:
            print ('*NOTE*: Currently the first device matching the '
                   'Vendor/Product id is used')
        
        self.d.set_configuration()
        
        self.EP1_out = 0x01
        self.EP1_in = 0x81
        self.EP2_in = 0x82
        self.EP6_in = 0x86
        self.EP1_in_size = 64
        self.EP2_in_size = 64
        self.EP6_in_size = 64

    def initialize(self):
        """ 0x01 initialize """
        self.d.write(self.EP1_out, struct.pack('<B', 0x01))

    def set_integration_time(self, time):
        """ 0x02 set integration time """
        self.d.write(self.EP1_out, struct.pack('<BI', 0x02, int(time)))

    def _set_strobe_enable_status(self):
        """ 0x03 set strobe enable status """
        raise NotImplementedError

    def _set_shutdown_mode(self):
        """ 0x04 set shutdown mode """
        raise NotImplementedError

    def query_information(self, address):
        """ 0x05 query info """
        self.d.write(self.EP1_out, struct.pack('<BB', 0x05, int(address)%0xF))
        ret = self.d.read(self.EP1_in, self.EP1_in_size)
        if a[0] != 0x05 or a[1] != int(address)%0xFF:
            raise Exception('query_information: Wrong answer')
        return ret[2:ret.index(0)].tostring()

    def _write_information(self, address):
        """ 0x06 write info """
        raise NotImplementedError

    def _request_spectrum(self):
        """ 0x09 request spectra """
        raise NotImplementedError

    # 0x0A set trigger mode
    # 0x0B query number of plugin accessories
    # 0x0C query plugin identifiers
    # 0x0D detect plugins

    # 0x60 I2C read
    # 0x61 I2C write
    # 0x62 spi io
    # 0x6A write register info
    # 0x6B read register info
    def read_pcb_temperature(self):
        """ 0x6C read pcb temperature """
        self.d.write(self.EP1_out, struct.pack('<B', 0x6C))
        ret = self.d.read(self.EP1_in, self.EP1_in_size)
        return ret
    
    # 0x6D read irradiance calib factors
    # 0x6E write irradiance calib factors

    # 0xFE query info



