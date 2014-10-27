**This software is not associated with Ocean Optics. Use it at your own risk.**

**Info:** If this is not working for you, checkout [python-seabreeze](https://github.com/ap--/python-seabreeze).


## Ocean Optics python module ##

This python module provides access to some basic functionality of some [Ocean
Optics](http://www.oceanoptics.com/) spectrometers. The lack of availability of
a python interface for their spectrometers lead to the development of this
module. The specifications of the USB communication layer used in their
spectrometers are freely available in the OEM manuals on their website.

This software is a community effort to get platform independent python support
for these spectrometers. If you are not 100% sure what you are doing, stick with
the - also platform independent - SpectraSuite and OceanView software.

**Currently working with:**

* USB2000+
* USB4000
* QE65000
* STS (Note: The rewritten class supports protocol version _0x1100_)
* USB2000
* USB650

**Might work, untested:**

* HR4000
* QE65pro
* HR2000+
* HR2000
* apex
* maya
* maya2000pro
* Torus

**Not yet supported:**

* Jaz
* NIR 
* NIRQUEST

Contributions are welcome.


## Installing ##

### Requirements ###

I'm using python 2.7.x, so this is not tested on Python 3.x.

The core libraries require:
- pyusb-1.0.0b1 (this is available on pypi. Newer versions break parts of the API...)
- numpy

For the example you'll need:
- gtk3 python bindings
- matplotlib

### Linux ###

To install the python module download this repository and run:

```
python setup.py install
```

You should also install the udev rules:

```
sudo cp misc/10-oceanoptics.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

make sure that your user is in the _plugdev_ group.

### Windows and OSX ###

If anyone wants to volunteer to write instructions how to use this library on Windows and Mac, feel free to contact me.


## Quickstart ##

After installing test if it's working by:

```
import oceanoptics
spec = oceanoptics.get_a_random_spectrometer()
print spec.spectrum()
```

or run the example program _liveview.py_


## Contributing ##

If you own any of the spectrometers listed below, feel free to contribute.


## License ##

Python files in this repository are released under the [MIT license](LICENSE.md).
