# XXX: untested
#----------------------------------------------------------
from oceanoptics.base import OceanOpticsBase as _OOBase
from oceanoptics.defines import OceanOpticsModelConfig as _OOModelConfig
from oceanoptics.spectrometers.USB4000 import USB4000 as _USB4000
#----------------------------------------------------------


class HR4000(_OOBase):

    def __init__(self):
        self._EPin2 = _OOModelConfig['HR4000']['EPin2']
        self._EPin6 = _OOModelConfig['HR4000']['EPin6']
        self._EPin2_size = _OOModelConfig['HR4000']['EPin2_size']
        self._EPin6_size = _OOModelConfig['HR4000']['EPin6_size']
        super(HR4000, self).__init__('HR4000')

    # XXX: the HR4000 uses the same two EndPoint Spectrum function as the USB4000
    _request_spectrum = _USB4000.__dict__['_request_spectrum']

