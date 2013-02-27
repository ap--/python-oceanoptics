
""" File:           defines.py
    Author:         Andreas Poehlmann
    Last change:    2012/09/04

    Python Interface for OceanOptics Spectometer USB2000+
    Some definition stuff...
"""

#----------------------------------------------------------

class OceanOpticsError(Exception):
    pass

USB2000_TRIGGER_MODES = {
        'normal' : 0,
        'software' : 1,
        'external_HW_lvl' : 2,
        'external_sync' : 3,
        'external_HW_edge' : 4 
        }


