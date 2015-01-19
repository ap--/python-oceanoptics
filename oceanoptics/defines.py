"""
File:           defines.py
Author:         Andreas Poehlmann

Python Interface for OceanOptics Spectometer USB2000+
Some definition stuff...
"""


class OceanOpticsError(Exception):
    """OceanOptics specific Exception"""
    pass

OceanOpticsVendorId = 0x2457

OceanOpticsModelConfig = {
    'USB-ISS-UVVIS': {'ProductId': [],  # XXX: Couldn't find productid
                      'EPout': 0x02,
                      'EPin0': 0x87, 'EPin0_size': 64,
                      'EPin1': 0x07, 'EPin1_size': 64, },
    'Maya2000pro': {'ProductId': [0x102A],
                    'EPout': 0x01,
                    'EPin0': 0x81, 'EPin0_size': 64,
                    'EPin1': 0x82, 'EPin1_size': 512, },
    'USB-LS450': {'ProductId': [],  # XXX: Couldn't find productid
                  'EPout': 0x02,
                  'EPin0': 0x87, 'EPin0_size': 64,
                  'EPin1': 0x07, 'EPin1_size': 64, },
    'NIRQUEST': {'ProductId': [0x1026, 0x1028],
                 'EPout': 0x01,
                 'EPin0': 0x81, 'EPin0_size': 512,
                 'EPin1': 0x82, 'EPin1_size': 512, },
    'USB2000+': {'ProductId': [0x101E],
                 'EPout': 0x01,
                 'EPin0': 0x81, 'EPin0_size': 64,
                 'EPin1': 0x82, 'EPin1_size': 512, },
    'HR2000+': {'ProductId': [0x1016],
                'EPout': 0x01,
                'EPin0': 0x81, 'EPin0_size': 64,
                'EPin1': 0x82, 'EPin1_size': 512, },
    'QE65pro': {'ProductId': [0x4004],
                'EPout': 0x01,
                'EPin0': 0x81, 'EPin0_size': 64,
                'EPin1': 0x82, 'EPin1_size': 512, },
    'QE65000': {'ProductId': [0x1018],
                'EPout': 0x01,
                'EPin0': 0x81, 'EPin0_size': 64,
                'EPin1': 0x82, 'EPin1_size': 512, },
    'USB2000': {'ProductId': [0x1002],
                'EPout': 0x02,
                'EPin0': 0x87, 'EPin0_size': 64,
                'EPin1': 0x82, 'EPin1_size': 64, },
    'USB650': {'ProductId': [0x1014],
                'EPout': 0x02,
                'EPin0': 0x87, 'EPin0_size': 64,
                'EPin1': 0x82, 'EPin1_size': 64, },
    # The USB4000 returns spectra split over two end points
    #  EPin6 for first 1024 pixels then EPin2 for the rest
    'USB4000': {'ProductId': [0x1022],
                'EPout': 0x01,
                'EPin0': 0x81, 'EPin0_size': 64,
                'EPin1': 0x81, 'EPin1_size': 64,
                'EPin2': 0x82, 'EPin2_size': 512,
                'EPin6': 0x86, 'EPin6_size': 512 },
    'HR2000': {'ProductId': [0x100A, 0x1009],
               'EPout': 0x02,
               'EPin0': 0x87, 'EPin0_size': 64,
               'EPin1': 0x82, 'EPin1_size': 64, },
    # The HR4000 returns spectra split over two end points
    #  EPin6 for first 1024 pixels then EPin2 for the rest
    'HR4000': {'ProductId': [0x1012, 0x1011],
               'EPout': 0x01,
               'EPin0': 0x81, 'EPin0_size': 64,
               'EPin1': 0x82, 'EPin1_size': 512,
               'EPin2': 0x82, 'EPin2_size': 512,
               'EPin6': 0x86, 'EPin6_size': 512 },
    'Torus': {'ProductId': [0x1040],
              'EPout': 0x01,
              'EPin0': 0x81, 'EPin0_size': 64,
              'EPin1': 0x82, 'EPin1_size': 512, },
    'Apex': {'ProductId': [0x1044],
             'EPout': 0x01,
             'EPin0': 0x81, 'EPin0_size': 64,
             'EPin1': 0x82, 'EPin1_size': 512, },
    'Maya': {'ProductId': [0x102C],
             'EPout': 0x01,
             'EPin0': 0x81, 'EPin0_size': 64,
             'EPin1': 0x82, 'EPin1_size': 512, },
    'Jaz': {'ProductId': [0x2000],
            'EPout': 0x01,
            'EPin0': 0x81, 'EPin0_size': 512,
            'EPin1': 0x82, 'EPin1_size': 512, },
    'NIR': {'ProductId': [0x1010, 0x100C],
            'EPout': 0x02,
            'EPin0': 0x87, 'EPin0_size': 64,
            'EPin1': 0x07, 'EPin1_size': 64, },
    # The STS has a slightly different interface, but I think we
    # can just communicate everything through EP 0x01 and 0x81,
    # so we can keep most of the abstraction layer intact
    'STS': {'ProductId': [0x4000],
            'EPout': 0x01,
            'EPin0': 0x81, 'EPin0_size': 64,
            'EPin1': 0x81, 'EPin1_size': 64, },
    }


OceanOpticsSpectrumConfig = {
    'Apex'          : { 0x80 : [  9, 512, lambda x : x      ],
                        0x00 : [ 66,  64, lambda x : x      ] },
    'HR2000+'       : { 0x80 : [  8, 512, lambda x : x^0x2000 ],
                        0x00 : [ 64,  64, lambda x : x^0x2000 ] },
    'HR4000'        : { 0x80 : [ 15, 512, lambda x : x      ],
                        0x00 : [120,  64, lambda x : x      ] },
    'Maya'          : { 0x80 : [  9, 512, lambda x : x      ],
                        0x00 : [ 66,  64, lambda x : x      ] },
    'Maya2000pro'   : { 0x80 : [  9, 512, lambda x : x      ],
                        0x00 : [ 66,  64, lambda x : x      ] },
    'QE65000'       : { 0x80 : [  5, 512, lambda x : x^0x8000 ],
                        0x00 : [ 40,  64, lambda x : x^0x8000 ] },
    'QE65pro'       : { 0x80 : [  5, 512, lambda x : x^0x8000 ],
                        0x00 : [ 40,  64, lambda x : x^0x8000 ] },
    'Torus'         : { 0x80 : [  8, 512, lambda x : x      ],
                        0x00 : [ 64,  64, lambda x : x      ] },
    'USB2000+'      : { 0x80 : [  8, 512, lambda x : x      ],
                        0x00 : [ 64,  64, lambda x : x      ] },
    'USB4000'       : { 0x80 : [ 15, 512, lambda x : x      ],
                        0x00 : [120,  64, lambda x : x      ] },
    'USB2000'       : { 0x00 : [ 64,  64, lambda x : x      ],
                        0x80 : [ 64,  64, lambda x : x      ] },
    'USB650'        : { 0x00 : [ 64,  64, lambda x : x      ],
                        0x80 : [ 64,  64, lambda x : x      ] },
    'HR2000'        : { 0x00 : [ 64,  64, lambda x : x      ],
                        0x80 : [ 64,  64, lambda x : x      ] },
    }


OceanOpticsValidPixels = {
    'Apex'          : slice(10, 2058),
    'HR2000+'       : slice(20, 2048),
    'HR4000'        : slice(22, 3670),
    'Maya'          : slice(16, 2064),
    'Maya2000pro'   : slice(10, 2058),
    'QE65000'       : slice(10, 1034),
    'QE65pro'       : slice(0, 1024),
    'Torus'         : slice(20, 2048),
    'USB2000+'      : slice(20, 2048),
    'USB4000'       : slice(22, 3670),
    'USB2000'       : slice(26, 2048),
    'USB650'        : slice(26, 2048),
    'HR2000'        : slice(26, 2048),
    }

OceanOpticsMinMaxIntegrationTime = {
    'Apex'          : (0.015, 1600.),
    'HR2000+'       : (0.001, 655.350),
    'HR4000'        : (0.00001, 655.350),
    'Maya'          : (0.015, 1600.),
    'Maya2000pro'   : (0.0072, 65.),
    'QE65000'       : (0.008, 1600.),
    'QE65pro'       : (0.010, 1600.),
    'Torus'         : (0.0, float('inf')),  # TODO: don't know...
    'USB2000+'      : (0.001, 655.350),
    'USB4000'       : (0.00001, 655.350),
    'USB2000'       : (0.003, 655.350),
    'USB650'        : (0.003, 655.350),  # XXX: seems to be a rebranded USB2000
    'HR2000'        : (0.003, 655.350),
    'STS'           : (0.00001, 85.)
    }

OceanOpticsSupportedModels = OceanOpticsSpectrumConfig.keys() + ['STS']

