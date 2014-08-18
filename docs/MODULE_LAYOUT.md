### planned module layout

To turn this thing into a universal python module for oceanoptics spectrometers, I suggest the following approach:

There is one base class for USB-communication shared by all classes:
    OceanOpticsUSBComm
It's init function needs two be called with a specific model-string, that is used two set up the USB-communication.
It also provides three functions called \_usb\_send, \_usb\_read, \_usb\_query .

The OceanOpticsBase class is shared by most spectrometers. It inherits from USBComm and implements the following lowlevel functionality. The lowlevel function names start with a underscore, and they basically implement the stuff thats in the dev-manual provided by OceanOptics.

| cmd | function             |   
|:----|:---------------------|
| 0x01| initialize USB          
| 0x02| set integration time    
| 0x05| query information       
| 0x06| write information       
| 0xFE| query status            
| 0x09| request spectra         


If a class inherits from USBComm and implements lowlevel functions, all highlevel functions in that class should only use the available lowlevel functions and their names should match \[a\-z\]\[a\-z\_\]\*\[a\-z\].

The common high-level interface for all spectrometers will be defined in OceanOpticsSpectrometer. Inherit from this, and implement the functionality.

That way we can assure a common base highlevel interface for all spectrometers, and if some extra functionality is shared among spectrometers it can be easily tested for, by checking if they inherit from the specific class.

The classes could be grouped like that. All will be implemented in \_base.py. Each spectrometer then inherits from the base classes that it supports.

So this is free for discussion. Because some of the classes below are only supported by a single spectrometer model. Maybe those should be put in the Spectrometer class... Also the high-level interface might still change...


**class** OceanOpticsTrigger
* 0x03 set strobe enable status 
* 0x0A set trigger mode         

**class** OceanOpticsPlugin
* 0x0C query plugin id          
* 0x0B query number od plugin   
* 0x0D detect plugins           

**class** OceanOpticsRegister
* 0x6A write register info      
* 0x6B read register indo       

**class** OceanOpticsIrradiance
* 0x6D read irradiance calib    
* 0x6E write irradiance calib   

**class** OceanOpticsI2C
* 0x60 i2c read                 
* 0x61 i2c write                

**class** OceanOpticsSPI
* 0x62 spi io                   

**class** OceanOpticsTemperature
* 0x6C red pcb temperature      

**class** OceanOpticsPSOC
* 0x68 psoc read                
* 0x69 psoc write               

**class** OceanOpticsShutdown
* 0x04 set shutdown mode        

**class** OceanOpticsSerial
* 0x07 wirte serial number      
* 0x08 get serial number        

**class** OceanOpticsTEC
* 0x70 set fan state            
* 0x71 set tec controller state 
* 0x72 tec controller read      
* 0x73 tec controller write     

**class** ???
* 0x20 read temperature         
* 0x21 set led mode             
* 0x23 query calib constant     
* 0x24 send calib constant      
* 0x25 set analog output        
* 0x26 load all calib < eeprom  
* 0x27 write all calib > eeprom 

**class** OceanOpticsPotentiometer
* 0x40 set digital poti         
* 0x41 set powerup potu val     
* 0x42 read poti val            


Feel free to implement any of those.
