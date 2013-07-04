# XXX: untested
#----------------------------------------------------------
from .._base import OceanOpticsBase as _OOBase
#----------------------------------------------------------


class QE65000(_OOBase):

    def __init__(self):
        super(QE65000, self).__init__('QE6500')


