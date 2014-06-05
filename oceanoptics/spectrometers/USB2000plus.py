# tested 
#----------------------------------------------------------
from ..base import OceanOpticsBase as _OOBase
#----------------------------------------------------------


class USB2000plus(_OOBase):

    def __init__(self):
        super(USB2000plus, self).__init__('USB2000+')


