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


setV(dac0, 0)
time.sleep(3)
setV(dac0, 3.3)

v23 = adc.readADCDifferential23(4096, 128)*0.001  # returns float


#Graph data:


indata = np.zeros(nsamples,'float')
print('Initializing ADC...')


adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)

t0 = time.perf_counter()
for i in range(nsamples):
   st = time.perf_counter()
   indata[i] = 0.001*adc.getLastConversionResults()
   while (time.perf_counter() - st) <= sinterval:
      pass
t = time.perf_counter() - t0
adc.stopContinuousConversion()

xpoints = np.arange(0, ACQTIME, sinterval)

f1, ax1 = plt.subplots()
ax1.plot(xpoints, indata)
f1.show()


#Fit data to find time constant
x = xpoints
y = indata
def fitfxn(x, v0, tau):
    return v0 * np.exp(-x/tau)

param, param_cov = curve_fit(fitfxn, x, y)

input("\nPress <Enter> to exit...\n")



