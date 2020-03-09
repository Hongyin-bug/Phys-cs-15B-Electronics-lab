import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import sys
import time
from Adafruit import ADS1x15

adc = ADS1x15()

import os
import sys
from wpdir import wiringpi

DELAY = 5   # delay in ms between duty cycle changes during ramp
STEPS = 100 # number of duty cycle steps in ramp

PWM_OUTPUT = 2  # pin mode
PWM_MODE_MS = 0 # standard mark-space PWM

PWMPIN = 18  # Broadcom pin numbering
PWM_RANGE = 4000 # must be less than 4096
PWM_DIVISOR = 2  # must be between 2 and 4095
###############################################################################
#
# Check user ID - must be running with root privileges
#
euid = os.geteuid()
if euid != 0:
   print('\nThis program must be run as root.  Try using sudo.',
          file=sys.stderr)
   print('Exiting.\n', file=sys.stderr)
   exit(1)

retval = wiringpi.wiringPiSetupGpio()  # use Broadcom pin numbering
if retval != 0:
   print('wiringpi setup error.  Exiting.', file=sys.stderr)
   exit(1)

wiringpi.pinMode(PWMPIN, PWM_OUTPUT)
wiringpi.pwmSetMode(PWM_MODE_MS)
wiringpi.pwmSetClock(PWM_DIVISOR)
wiringpi.pwmSetRange(PWM_RANGE)
###############################################################################
temp = 35 #Set point for block temperature
period = 600 #Record data for 10 minutes, in seconds

#Store temperature measurements
file0write=open("Temperature Data",'w')
file0write.write("0 \n")
file0write.close()
Tlist = []

#Controller portion
for i in range(period+1):
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    T = 263.84 - 5000*np.sqrt(0.002304 + 0.0004*np.log(Rt/15.73))
    Tlist.append(T)  #stores temperature data in a list and a textfile
    file0append = open("Temperature Data",'a')
    file0append.write(str(T) + "\r\n")
    file0write.close()
    for i in range(10):
        v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
        v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
        Vt = v01 - v23 #voltage across thermistor
        I = v23/(10^5) #current
        Rt = Vt/I #resistance of thermistor
        T = 263.84 - 5000*np.sqrt(0.002304 + 0.0004*np.log(Rt/15.73))
        if T < temp - 3:  #Sometimes the temperature measurement is no exact, so allow one degree of error
            DEFDUTY = 100
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts) #set pwm cycle here = 100  #set pwm cycle to 100% 
        elif T > temp - 2:
            DEFDUTY = 0    #set pwm cycle to 0%
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts) #set pwm cycle here 
        time.sleep(0.1)


# Plot of temperature over the 10 minutes
x = np.arange(0, period + 1, 1)
y = Tlist

plt.scatter(x, y, s = 5, c = 'yellowgreen')

plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celcius)")

axes = plt.gca()
axes.set_ylim([0,50])

plt.show()

