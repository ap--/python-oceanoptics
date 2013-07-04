# XXX: untested
#----------------------------------------------------------
from .._base import OceanOpticsBase as _OOBase
#----------------------------------------------------------


class QE65pro(_OOBase):

    def __init__(self):
        super(QE65pro, self).__init__('QE65pro')


