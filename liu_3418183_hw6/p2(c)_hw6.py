import sys
import time

from Adafruit import ADS1x15
adc = ADS1x15()
################
while True:
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    print(Rt)
    print(I)
    time.sleep(1)






