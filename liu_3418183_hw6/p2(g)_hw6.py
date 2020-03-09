import sys
import time
import numpy as np
from Adafruit import ADS1x15
adc = ADS1x15()

################
while True:
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    T = 263.84 - 5000*np.sqrt(0.002304 + 0.0004*np.log(Rt/15.73))
    print('Temperature: T = %.3f' % T, 'Resistance: R = %.3f' % Rt)
    time.sleep(1)




