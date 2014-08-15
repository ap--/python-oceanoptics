import usb.core
from oceanoptics.defines import OceanOpticsSupportedModels as _OOSupMod
from oceanoptics.defines import OceanOpticsModelConfig as _OOModConf
from oceanoptics.defines import OceanOpticsVendorId as _OOVendorId
from oceanoptics.defines import OceanOpticsError as _OOError

import oceanoptics.spectrometers
from oceanoptics.spectrometers.XXX2000 import USB2000, HR2000
from oceanoptics.spectrometers.XXX2000plus import USB2000plus, HR2000plus
from oceanoptics.spectrometers.XXX4000 import USB4000, HR4000
from oceanoptics.spectrometers.MAYA import MAYA
from oceanoptics.spectrometers.MAYA2000pro import MAYA2000pro
from oceanoptics.spectrometers.APEX import APEX
from oceanoptics.spectrometers.QE65xxx import QE65000, QE65pro
from oceanoptics.spectrometers.TORUS import TORUS
from oceanoptics.spectrometers.STS import STS

_models = {
	"USB2000"	: USB2000,
	"HR2000"	: HR2000,
	"USB2000plus"	: USB2000plus,
	"HR2000plus"	: HR2000plus,
	"USB4000"	: USB4000,
	"HR4000"	: HR4000,
	"MAYA"	: MAYA,
	"MAYA2000pro"	: MAYA2000pro,
	"APEX"	: APEX,
	"QE65000"	: QE65000,
	"QE65pro"	: QE65pro,
	"TORUS"	: TORUS,
	"STS"	: STS,
        }

def get_a_random_spectrometer():
    ProductId = {}
    for model in _OOSupMod:
        pid = _OOModConf[model]['ProductId']
        ProductId.update(zip(pid, [model] * len(pid)))

    devices = usb.core.find(find_all=True,
                            custom_match=lambda d: (d.idVendor == _OOVendorId and
                                                    d.idProduct in ProductId.keys()))
    # TODO: ??? usb.core.find can also return a generator ???
    devices = list(devices)

    if devices:
        print '> found:'
    else:
        raise _OOError('no supported spectrometers found')
    for d in devices:
        print '>  - %s' % ProductId[d.idProduct]

    mod = ProductId[devices[0].idProduct]
    print '>'
    print '> returning first %s as OceanOpticsSpectrometer' % mod

    return _models[mod]
