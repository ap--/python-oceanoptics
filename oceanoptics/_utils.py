
import usb.core
from _defines import OceanOpticsSupportedModels as _OOSupMod
from _defines import OceanOpticsModelConfig as _OOModConf
from _defines import OceanOpticsVendorId as _OOVendorId
from _defines import OceanOpticsError as _OOError
from _base import OceanOpticsBase


def get_a_random_spectrometer():
    
    ProductId = {}
    for model in _OOSupMod:
        pid = _OOModConf[model]['ProductId']
        ProductId.update(zip(pid,[model]*len(pid)))

    devices = usb.core.find(find_all=True,
                    custom_match=lambda d: (d.idVendor==_OOVendorId and
                                            d.idProduct in ProductId.keys()))
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
    return OceanOpticsBase(mod)


