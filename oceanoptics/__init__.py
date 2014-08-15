
__version__ = '0.2.9'

from oceanoptics.spectrometers.XXX2000 import USB2000, HR2000
from oceanoptics.spectrometers.XXX2000plus import USB2000plus, HR2000plus
from oceanoptics.spectrometers.XXX4000 import USB4000, HR4000
from oceanoptics.spectrometers.MAYA import MAYA
from oceanoptics.spectrometers.MAYA2000pro import MAYA2000pro
from oceanoptics.spectrometers.APEX import APEX
from oceanoptics.spectrometers.QE65xxx import QE65000, QE65pro
from oceanoptics.spectrometers.TORUS import TORUS
from oceanoptics.spectrometers.STS import STS

from oceanoptics.defines import OceanOpticsError

from oceanoptics.utils import get_a_random_spectrometer
