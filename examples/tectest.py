import oceanoptics
import time

spec = oceanoptics.QE65000()

spec.integration_time(0.1)
sp = spec.spectrum()

spec.set_TEC_temperature(0)
time.sleep(30)

setpoints = [-1,-3,-5,-8,-10,-12,-15,-18]
temps = []

for s in setpoints:
    spec.set_TEC_temperature(s)
    print(s)
    time.sleep(30)
    temps.append(spec.get_TEC_temperature())

print(setpoints)
print(temps)

# >Bh
# [-1, -3, -5, -8, -10, -12, -15, -18]
#[-20, -22, -22, -22, -21, -20, -22, -22]

# <Bh
# [-1, -3, -5, -8, -10, -12, -15, -18]
#[-13, -5, -6, -6, -9, -10, -13, -16]

# <Bh longer coldown time
#[-1, -3, -5, -8, -10, -12, -15, -18]
#[-13, -5, -5, -6, -9, -11, -13, -16]

# +1
#[-1, -3, -5, -8, -10, -12, -15, -18]
#[-4, -4, -5, -6, -8, -11, -13, -16]