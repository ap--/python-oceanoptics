## Ocean Optics python module ##

This python module provides access to some basic functionality of some [Ocean
Optics](http://www.oceanoptics.com/) spectrometers. This software is not
associated with Ocean Optics. Use it at your own risk.

It is currently working with:

## Ocean Optics python module ##

Currently working with:

* USB2000+
* STS
* QE65000

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


## Quickstart ##

After installing run some of the example programs to test if everything is
working.


## Contributing ##

If you own any of the spectrometers listed below, feel free to contribute.






#### Possible Additions ####

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

#### Not currently planned ####

* HR2000
* Jaz
* NIR 
* NIRQUEST
