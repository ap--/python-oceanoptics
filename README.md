## Ocean Optics python module ##

This python module provides access to some basic functionality of some [Ocean
Optics](http://www.oceanoptics.com/) spectrometers. This software is not
associated with Ocean Optics. Use it at your own risk.

**Currently working with:**

* USB2000+
* QE65000
* STS (Note: The rewritten class supports protocol version _0x1100_)

Those should work, but are untested:

* USB4000
* HR2000+
* HR4000
* apex
* maya
* maya2000pro
* QE65pro
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


#### Possible Additions ####

These might actually already work.

* USB2000
* USB-LS450
* USB-ISS-UVVIS
* USB4000
* HR2000+
* HR4000
* apex
* maya
* maya2000pro
* QE65pro
* Torus

#### Not supported ####

* HR2000
* Jaz
* NIR 
* NIRQUEST
