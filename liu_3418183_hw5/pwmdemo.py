#!/usr/bin/env python3

#
# pwmdemo.py - Demonstrate hardware PWM
#
# 02Mar19  Improved printout and comments, added loop for slow ramp
# 28Feb18  Added printout of duty cycle during slow ramp
# 17Feb18  Everett Lipman
#

import os
import sys
from wpdir import wiringpi

DELAY = 5   # delay in ms between duty cycle changes during ramp
STEPS = 100 # number of duty cycle steps in ramp

#
# constants
#
PWM_OUTPUT = 2  # pin mode
PWM_MODE_MS = 0 # standard mark-space PWM

PWMPIN = 18  # Broadcom pin numbering

#
# The PWM clock base frequency is 19.2 MHz.  The counter
# is incremented at the base frequency divided by PWM_DIVISOR.
# When it reaches PWM_RANGE counts, it begins a new cycle.
# The output in mark-space mode is held high until the
# counter reaches the value set by pwmWrite().
#
# RANGE:  300; DIVISOR: 2 -> 32 kHz PWM with a resolution of 300 steps
# RANGE: 4000; DIVISOR: 2 -> 2.4 kHz PWM with a resolution of 4000 steps
#
PWM_RANGE = 300  # must be less than 4096
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

print()
print('Slow ramp...')
for duty in (0.0, 0.2, 0.4, 0.6, 1.0):
    duty_counts = int(duty*PWM_RANGE)
    duty_pct = 100.0*float(duty_counts)/PWM_RANGE
    print('Setting PWM duty cycle to %.0f %%  (%d/%d)' % (duty_pct, duty_counts,
                                                      PWM_RANGE))
    wiringpi.pwmWrite(PWMPIN, duty_counts)  # Allowabl values: 0 to PWM_RANGE
    wiringpi.delay(2000)
wiringpi.delay(1000)
print()
###############################################################################

print('Fast ramp...')
print()
print('^C to stop.')
while True:
   for i in range(STEPS):
      on = int(PWM_RANGE*i/STEPS)
      wiringpi.pwmWrite(PWMPIN, on)
      wiringpi.delay(DELAY)
   for i in range(STEPS, 0, -1):
      on = int(PWM_RANGE*i/STEPS)
      wiringpi.pwmWrite(PWMPIN, on)
      wiringpi.delay(DELAY)