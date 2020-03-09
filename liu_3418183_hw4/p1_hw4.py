ACQTIME = 2
SPS = 128
VRANGE = 4096

nsamples= ACQTIME*SPS
sinterval = 1.0/SPS

import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

VDD = 3.3
MAXN = 4095
NSTEPS = 4
DELAY = 3

from Adafruit.MCP4725 import MCP4725 as mcp4725
from Adafruit import ADS1x15
###############################################################################
##############################################################################

def setV(thedac, V):
   """Set output voltage of specified DAC to V

      thedac is the mcp4725 class instance
      V is the voltage.  V will be clipped if out of range.
   """
   if V > VDD:
      V = VDD
   if V < 0:
      V = 0

   vnum = int(MAXN*V/VDD)

   thedac.set_voltage(vnum)
##############################################################################

dac0 = mcp4725()
adc = ADS1x15()

#(b) This is the code for part (b)

'''volt = 0
v01 = [0]
v23 = [0]
current = [0]
print('Initializing ADC...')

for i in range(34):
    if volt <= 3.3:
        time.sleep(0.1)
        volt = 0.1 * i
        setV(dac0, volt)
        v23.append(adc.readADCDifferential23(4096, 128)*0.001)
        v01.append(adc.readADCDifferential01(4096, 128)*0.001)
        current.append((adc.readADCDifferential01(4096, 128)*0.001 - adc.readADCDifferential23(4096, 128)*0.001)/100)
    else:
        setV(dac0, 0)'''
        
#Graph data:

'''indata = np.zeros(nsamples,'float')
print('Initializing ADC...')

xpoints = v23
ypoints = current


plt.plot(xpoints,ypoints,'go')
plt.xlabel("Voltage at LED (V)")
plt.ylabel("Current (Amps)")

plt.show()'''



#(d) This is the code for part (d)
while True:
    try:
        volt = float(input("What is the voltage you want to set to? "))
        if volt <=0 or volt > 3.6:
            volt = float(input("voltage out of range, pls choose one that is positive and below 3.6V!!! "))
    except ValueError:
        print("Not a number, please try again.")
    else:
        setV(dac0, volt)
        time.sleep(0.1)
        v23 = adc.readADCDifferential23(4096, 128)*0.001
        v01 = adc.readADCDifferential01(4096, 128)*0.001
        current = (v01 - v23)/100
        print("Voltage drop across LED is: ", v23)
        print("Current through LED is ", current)

input("\nPress <Enter> to exit...\n")





