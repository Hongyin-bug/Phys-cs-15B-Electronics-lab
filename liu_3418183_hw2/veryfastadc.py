#!/usr/bin/env python3
#
# fastadc.py - ADC demo with ADS1015 continuous conversion
#
# 14May18  Changed time.sleep(1.0e-7) to pass in acquisition loop
#             Added units to elapsed time printout
# 27Feb18  Added comments about plotting style options
# 16Feb18  Modified plotting to use steps instead of linear interpolation
# 30Jan18  Changed full-scale range to 4096,
#          changed plotting to use object-oriented interface
# 27May16  Adapted from adcdemo.py by Everett Lipman
#

ACQTIME = 2.  # seconds of data acquisition

#    samples per second
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
SPS = 3300

#    full-scale range in mV
#    options: 256, 512, 1024, 2048, 4096, 6144.
VRANGE = 4096

nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

import sys
import time
import numpy as np
import matplotlib.pyplot as plt

#
# Adafruit libraries modified by Ben Laroque for Python 3 and ADS1015
#
from Adafruit import ADS1x15
###############################################################################

indata = np.zeros(nsamples,'float')

print()
print('Initializing ADC...')
print()

#
# Default ADC IC is ADS1015
# Default address is 0x48 on the default I2C bus
#
adc = ADS1x15()

# First two arguments are the channels
# Third argument is the full-scale range in mV (default +/- 6144).
#    options: 256, 512, 1024, 2048, 4096, 6144.
#    Note: input should not exceed VDD + 0.3
# Fourth argument is samples per second (default 250).
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
#
adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()

for i in range(nsamples):
   st = time.perf_counter()
   indata[i] = 0.001*adc.getLastConversionResults()
   while (time.perf_counter() - st) <= sinterval:
      pass

t = time.perf_counter() - t0

adc.stopContinuousConversion()

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t)
print()

f1, ax1 = plt.subplots()

#
# Default plotting style connects points with lines
#
ax1.plot(xpoints, indata)

#
# Plotting with steps is better for visualizing sampling
#
# ax1.plot(xpoints, indata,'-',drawstyle='steps-post')

f1.show()

input("\nPress <Enter> to exit...\n")
