import usb.core
from .defines import OceanOpticsSupportedModels as _OOSupMod
from .defines import OceanOpticsModelConfig as _OOModConf
from .defines import OceanOpticsVendorId as _OOVendorId
from .defines import OceanOpticsError as _OOError
from .base import OceanOpticsBase as _OOBase


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

    if mod == 'STS':
        from spectrometers.STS import STS
        return STS()
    elif mod == 'QE65000':
        from spectrometers.QE65000 import QE65000
        return QE65000()
    elif mod == 'USB4000':
        from spectrometers.USB4000 import USB4000
        return USB4000()
    elif mod == 'HR4000':
        from spectrometers.HR4000 import HR4000
        return HR4000()
    return _OOBase(mod)

