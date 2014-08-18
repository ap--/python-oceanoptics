## USB Command interface

Most of the OceanOptics spectrometer share a relatively similar usb-interface. The following tables show the supported commandset for each model.

* The STS spectrometer is not listed here, because it has a special commandset.

#### mapping for the cmdset table

| id| Spectrometer |
|:--|--------------|
| A | USB2000
| B | USB-LS450
| C | USB-ISS-UVVIS
| D | USB2000+
| E | USB4000
| F | HR2000
| G | HR2000+
| H | HR4000
| I | Jaz
| J | apex
| K | maya
| L | maya2000pro
| M | QE65pro
| N | QE65000 
| O | NIR 
| P | NIRQUEST
| Q | Torus

#### supported cmdsets


| cmd | function                 | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q |
|:----|:-------------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0x01| initialize USB           | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x02| set integration time     | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x03| set strobe enable status | x | x | x | x | x | x | x | x | x |   | x | x | x | x | x | x | x |
| 0x04| set shutdown mode        |   |   |   | x |   |   | x | x | x |   |   |   |   |   |   |   | x |
| 0x05| query information        | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x06| write information        | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x07| wirte serial number      | x | x | x |   |   | x |   |   |   |   |   |   |   |   | x | x |   |
| 0x08| get serial number        | x | x | x |   |   | x |   |   |   |   |   |   |   |   | x | x |   |
| 0x09| request spectra          | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x0A| set trigger mode         | x | x | x | x | x | x | x | x |   |   | x | x | x | x | x | x | x |
| 0x0B| query number od plugin   | x | x | x | x | x | x | x | x |   |   | x | x | x | x |x\*|   | x |
| 0x0C| query plugin id          | x | x | x | x | x | x | x | x |   |   | x | x | x | x |x\*|x\*| x |
| 0x0D| detect plugins           | x | x | x | x | x | x | x | x |   |   | x | x | x | x |x\*|   | x |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x1E| stop spectral acquisition|   |   |   |   |   |   |   |   |   |   |   |   |   |   | x |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x20| read temperature         |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x21| set led mode             |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x23| query calib constant     |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x24| send calib constant      |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x25| set analog output        |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x26| load all calib < eeprom  |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x27| write all calib > eeprom |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x3E| tec controller write     |   |   |   |   |   |   |   |   |   |   |   |   |   |   | x |   |   |
| 0x3F| tec controller read      |   |   |   |   |   |   |   |   |   |   |   |   |   |   | x |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x40| set digital poti         |   |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x41| set powerup potu val     |   |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x42| read poti val            |   |   | x |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x60| i2c read                 |   |   |   | x | x |   | x | x |   |   | x | x | x | x |   |   | x |
| 0x61| i2c write                |   |   |   | x | x |   | x | x |   |   | x | x | x | x |   |   | x |
| 0x62| spi io                   |   |   |   | x | x |   | x | x |   |   |   |   | x | x |   |   | x |
| 0x68| psoc read                |   |   |   |   | x |   | x | x |   |   |   |   | x | x |   |   | x |
| 0x69| psoc write               |   |   |   |   | x |   | x | x |   |   |   |   | x | x |   |   | x |
| 0x6A| write register info      |   |   |   | x | x |   | x | x |   | x | x | x | x | x |   |   | x |
| 0x6B| read register indo       |   |   |   | x | x |   | x | x |   | x | x | x | x | x |   |   | x |
| 0x6C| red pcb temperature      |   |   |   | x | x |   | x | x |   |   |   |   | x | x |   | x | x |
| 0x6D| read irradiance calib    |   |   |   | x | x |   | x | x |   | x | x | x | x | x |   |   | x |
| 0x6E| write irradiance calib   |   |   |   | x | x |   | x | x |   | x | x | x | x | x |   |   | x |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x70| set fan state            |   |   |   |   |   |   |   |   |   |   |   |   | x | x |   | x |   |
| 0x71| set tec controller state |   |   |   |   |   |   |   |   |   |   |   |   | x | x |   | x |   |
| 0x72| tec controller read      |   |   |   |   |   |   |   |   |   |   |   |   | x | x |   | x |   |
| 0x73| tec controller write     |   |   |   |   |   |   |   |   |   |   |   |   | x | x |   | x |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0xC0| get # of spectrometers   |   |   |   |   |   |   |   |   | x |   |   |   |   |   |   |   |   |
| 0xC1| set current channel      |   |   |   |   |   |   |   |   | x |   |   |   |   |   |   |   |   |
| 0xC6| get jaz info             |   |   |   |   |   |   |   |   | x |   |   |   |   |   |   |   |   |
| 0xC7| set jaz info             |   |   |   |   |   |   |   |   | x |   |   |   |   |   |   |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0xFE| query status             | x | x | x | x | x |   | x | x |   | x | x | x | x | x | x | x | x |
 

\*) Theese commands mean something different for the specific spectrometer



### near term planned support

To keep everything simple we'll exclude the following models at the beginning:

* HR2000, Jaz because they don't support the query status cmd
* NIR, NIRQUEST because they differ in some commands


| cmd | function                 | A | B | C | D | E | G | H | J | K | L | M | N | Q |
|:----|:-------------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0x01| initialize USB           | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x02| set integration time     | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x05| query information        | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x06| write information        | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0xFE| query status             | x | x | x | x | x | x | x | x | x | x | x | x | x |
| 0x09| request spectra          | x | x | x | x | x | x | x | x | x | x | x | x | x |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x03| set strobe enable status | x | x | x | x | x | x | x |   | x | x | x | x | x |
| 0x0A| set trigger mode         | x | x | x | x | x | x | x |   | x | x | x | x | x |
| 0x0C| query plugin id          | x | x | x | x | x | x | x |   | x | x | x | x | x |
| 0x0B| query number od plugin   | x | x | x | x | x | x | x |   | x | x | x | x | x |
| 0x0D| detect plugins           | x | x | x | x | x | x | x |   | x | x | x | x | x |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x6A| write register info      |   |   |   | x | x | x | x | x | x | x | x | x | x |
| 0x6B| read register indo       |   |   |   | x | x | x | x | x | x | x | x | x | x |
| 0x6D| read irradiance calib    |   |   |   | x | x | x | x | x | x | x | x | x | x |
| 0x6E| write irradiance calib   |   |   |   | x | x | x | x | x | x | x | x | x | x |
| 0x60| i2c read                 |   |   |   | x | x | x | x |   | x | x | x | x | x |
| 0x61| i2c write                |   |   |   | x | x | x | x |   | x | x | x | x | x |
| 0x62| spi io                   |   |   |   | x | x | x | x |   |   |   | x | x | x |
| 0x6C| red pcb temperature      |   |   |   | x | x | x | x |   |   |   | x | x | x |
| 0x68| psoc read                |   |   |   |   | x | x | x |   |   |   | x | x | x |
| 0x69| psoc write               |   |   |   |   | x | x | x |   |   |   | x | x | x |
| 0x04| set shutdown mode        |   |   |   | x |   | x | x |   |   |   |   |   | x |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x07| wirte serial number      | x | x | x |   |   |   |   |   |   |   |   |   |   |
| 0x08| get serial number        | x | x | x |   |   |   |   |   |   |   |   |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x70| set fan state            |   |   |   |   |   |   |   |   |   |   | x | x |   |
| 0x71| set tec controller state |   |   |   |   |   |   |   |   |   |   | x | x |   |
| 0x72| tec controller read      |   |   |   |   |   |   |   |   |   |   | x | x |   |
| 0x73| tec controller write     |   |   |   |   |   |   |   |   |   |   | x | x |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x20| read temperature         |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x21| set led mode             |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x23| query calib constant     |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x24| send calib constant      |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x25| set analog output        |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x26| load all calib < eeprom  |   | x |   |   |   |   |   |   |   |   |   |   |   |
| 0x27| write all calib > eeprom |   | x |   |   |   |   |   |   |   |   |   |   |   |
|     |                          |   |   |   |   |   |   |   |   |   |   |   |   |   |
| 0x40| set digital poti         |   |   | x |   |   |   |   |   |   |   |   |   |   |
| 0x41| set powerup potu val     |   |   | x |   |   |   |   |   |   |   |   |   |   |
| 0x42| read poti val            |   |   | x |   |   |   |   |   |   |   |   |   |   |
