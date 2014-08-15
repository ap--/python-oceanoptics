# tested 
#----------------------------------------------------------
from oceanoptics.base import OceanOpticsBase as _OOBase
#----------------------------------------------------------


class USB2000plus(_OOBase):

    def __init__(self):
        super(USB2000plus, self).__init__('USB2000+')


class HR2000plus(_OOBase):

    def __init__(self):
        super(HR2000plus, self).__init__('HR2000+')


