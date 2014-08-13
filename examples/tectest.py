import oceanoptics
import time

spec = oceanoptics.QE65000

spec.integration_time(0.1)
sp = spec.spectrum()

time.sleep(10)

setpoints = [-1,-3,-5,-8,-10,-12,-15,-18]
temps = []

for s in setpoints:
    spec.set_TEC_temperature(s)
    time.sleep(10)
    temps.append(spec.get_TEC_temperature())

print(setpoints)
print(temps)

