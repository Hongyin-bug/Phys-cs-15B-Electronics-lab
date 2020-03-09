from __future__ import print_function
import sys
import time
import numpy as np

from Adafruit import ADS1x15
adc = ADS1x15()

import os
from wpdir import wiringpi

DELAY = 5   # delay in ms between duty cycle changes during ramp
STEPS = 100 # number of duty cycle steps in ramp

PWM_OUTPUT = 2  # pin mode
PWM_MODE_MS = 0 # standard mark-space PWM

PWMPIN = 18  # Broadcom pin numbering
PWM_RANGE = 4000  # must be less than 4096
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
#Ask for desired temperature
while True:
    try:
        temp = int(input("What is the temperature you want to set to? (in Celcius)"))
        if temp <30 or temp > 60:
            temp = int(input("Temperature out of range, pls choose one in the range of 30 to 60"))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break

#Controller portion
while True:
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    T = 263.84 - 5000*np.sqrt(0.002304 + 0.0004*np.log(Rt/15.73))
    if T < temp - 1:  #Sometimes the temperature measurement is no exact, so allow one degree of error
        DEFDUTY = 100
        duty_counts = int(DEFDUTY*PWM_RANGE)
        wiringpi.pwmWrite(PWMPIN, duty_counts) #set pwm cycle here = 100  #set pwm cycle to 100% 
    elif T > temp - 0.5:
        DEFDUTY = 0    #set pwm cycle to 0%
        duty_counts = int(DEFDUTY*PWM_RANGE)
        wiringpi.pwmWrite(PWMPIN, duty_counts) #set pwm cycle here 
    time.sleep(0.001)


