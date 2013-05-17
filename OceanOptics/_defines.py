
""" File:           defines.py
    Author:         Andreas Poehlmann

    Python Interface for OceanOptics Spectometer USB2000+
    Some definition stuff...
"""

#----------------------------------------------------------

class OceanOpticsError(Exception):
    pass

OceanOpticsVendorId = 0x2457

OceanOpticsModelConfig = {
    'USB2000'       : { 'ProductId' : [], # XXX: Couldn't find productid
                        'EPout' : 0x02,
                        'EPin0' : 0x87, 'EPin0_size' : 64,
                        'EPin1' : 0x07, 'EPin1_size' : 64, },
    'USB-LS450'     : { 'ProductId' : [], # XXX: Couldn't find productid
                        'EPout' : 0x02,
                        'EPin0' : 0x87, 'EPin0_size' : 64,
                        'EPin1' : 0x07, 'EPin1_size' : 64, },
    'USB-ISS-UVVIS' : { 'ProductId' : [], # XXX: Couldn't find productid
                        'EPout' : 0x02,
                        'EPin0' : 0x87, 'EPin0_size' : 64,
                        'EPin1' : 0x07, 'EPin1_size' : 64, },
    'HR2000'        : { 'ProductId' : [0x100A, 0x1009],
                        'EPout' : 0x02,
                        'EPin0' : 0x87, 'EPin0_size' : 64,
                        'EPin1' : 0x07, 'EPin1_size' : 64, },
    'NIR'           : { 'ProductId' : [0x1010, 0x100C],
                        'EPout' : 0x02,
                        'EPin0' : 0x87, 'EPin0_size' : 64,
                        'EPin1' : 0x07, 'EPin1_size' : 64, },
    'USB2000+'      : { 'ProductId' : [0x101E],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'Torus'         : { 'ProductId' : [0x1040],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'NIRQUEST'      : { 'ProductId' : [0x1026, 0x1028],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 512,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'USB4000'       : { 'ProductId' : [0x1022],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'HR2000+'       : { 'ProductId' : [0x1012],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'HR4000'        : { 'ProductId' : [0x1012, 0x1011],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'Apex'          : { 'ProductId' : [0x1044],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'Maya'          : { 'ProductId' : [0x102A],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'Maya2000pro'   : { 'ProductId' : [0x102A],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'QE65pro'       : { 'ProductId' : [0x1018],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'QE65000'       : { 'ProductId' : [0x1018],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    'Jaz'           : { 'ProductId' : [0x2000],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 512,
                        'EPin1' : 0x82, 'EPin1_size' : 512, },
    # This one has a slightly different interface, but I think we
    # can just communicate everything through EP 0x01 and 0x81,
    # so we can keep most of the abstraction layer intact
    'STS'           : { 'ProductId' : [0x4000],
                        'EPout' : 0x01,
                        'EPin0' : 0x81, 'EPin0_size' : 64,
                        'EPin1' : 0x81, 'EPin1_size' : 64, }, 
        }


USB2000_TRIGGER_MODES = {
        'normal' : 0,
        'software' : 1,
        'external_HW_lvl' : 2,
        'external_sync' : 3,
        'external_HW_edge' : 4 
        }




