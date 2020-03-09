import time
import math
import numpy as np

VDD = 3.3
MAXN = 4095
NSTEPS = 4
DELAY = 3  # seconds

#
# Adafruit library
#
from Adafruit.MCP4725 import MCP4725 as mcp4725
##############################################################################
dac0 = mcp4725()

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

#(a)(b)        
'''t0 = time.perf_counter()
volt = 0
while volt<= 2:
    t = time.perf_counter() - t0
    volt = math.sin(50*math.pi*t) + 1
    setV(dac0, volt)
    time.sleep(0.001)'''

#(c)
'''volt = [0,]
for i in range(500000):
    volt.append(float(math.sin(50*math.pi*i/10000)+1))
    
print("start")
vnum = int(MAXN*V/VDD)
for i in volt:
      setV(dac0, i)
      time.sleep(0.002)'''

#(d)
volt = [0,]
for i in range(500000):
    volt.append(float(math.sin(50*math.pi*i/10000)+1))
    
print("start")
vnum = int(MAXN*V/VDD)
for i in volt:
      dac0.set_voltage(i)
      time.sleep(0.002)
    
    

input("\nPress <Enter> to exit...\n")
    



