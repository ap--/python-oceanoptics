**This software is not associated with Ocean Optics. Use it at your own risk.**

## Ocean Optics python module ##

This python module provides access to some basic functionality of some [Ocean
Optics](http://www.oceanoptics.com/) spectrometers. 

**Currently working with:**

* USB2000+
* USB4000
* QE65000
* STS (Note: The rewritten class supports protocol version _0x1100_)

Those should work, but are untested:
* HR4000
* QE65pro
* HR2000+
* USB2000
* HR2000
* apex
* maya
* maya2000pro
* Torus

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

or run some the example program _liveview.py_


## Contributing ##

If you own any of the spectrometers listed below, feel free to contribute.


#### Not yet supported ####

* Jaz
* NIR 
* NIRQUEST
