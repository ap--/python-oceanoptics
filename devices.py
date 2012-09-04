
import usb
import struct

spectrometers = []
for bus in usb.busses():
    for dev in bus.devices:
        if dev.idVendor == 0x2457 and dev.idProduct == 0x101E:
            spectrometers.append(dev)

if spectrometers:
    print 'Using the first spectrometer'
    oos = spectrometers[0]
else:
    print 'No spectrometers found'
    exit()

# oos
#-------------

#handle = oos.open()

# EP1_out 0x01
# EP2_in  0x82
# EP6_in  0x86
# EP1_in  0x81

class scratch_OOS(object):

    def __init__(self, usbdevice):
        self.d = usbdevice
        endpoints = oos.configurations[0].interfaces[0][0].endpoints
        endpoints = dict( (ep.address, ep) for ep in endpoints )
        self.EP1_out = endpoints[0x01]
        self.EP2_in = endpoints[0x82]
        self.EP6_in = endpoints[0x86]
        self.EP1_in = endpoints[0x81]
        self.handle = self.d.open()

        self.handle.setConfiguration(0)
        self.handle.claimInterface(0)
    
        self._write = self.handle.bulkWrite
        self._read = self.handle.bulkRead
#cmds

    def initialize(self):
        """ 0x01 initialize """
        self._write(self.EP1_out, struct.pack('<B', 0x01))

    def set_integration_time(self, time):
        """ 0x02 set integration time """
        self._write(self.EP1_out, struct.pack('<BI', 0x02, int(time)))

# 0x03 set strobe enable status
# 0x04 set shutdown mode

    def query_information(self, address):
        """ 0x05 query info """
        self._write(self.EP1_out, struct.pack('<BB', 0x05, int(address)%256))
        ret = self._read(self.EP1_in, self.EP1_in.maxPacketSize)
        return ret

# 0x06 write info

# 0x09 request spectra
# 0x0A set trigger mode
# 0x0B query number of plugin accessories
# 0x0C query plugin identifiers
# 0x0D detect plugins

# 0x60 I2C read
# 0x61 I2C write
# 0x62 spi io
# 0x6A write register info
# 0x6B read register info
# 0x6C read pcb temperature
# 0x6D read irradiance calib factors
# 0x6E write irradiance calib factors

# 0xFE query info
