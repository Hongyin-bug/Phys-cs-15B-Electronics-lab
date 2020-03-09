from __future__ import print_function
import sys
import time
import numpy as np
from scipy.optimize import curve_fit

from Adafruit import ADS1x15
adc = ADS1x15()

import os
from wpdir import wiringpi

import board
import digitalio
import busio
import adafruit_max31865 as max3

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
rtd_sensor = max3.MAX31865(spi, cs, wires=3, rtd_nominal=100.0, ref_resistor=430.0)

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

#Controller portion
alpha = -0.048
beta = 0.0001
R0 = 16.310
T0 = 22.720

Trtd_list = []
Tth_list = []
Rth_list = []

file0write=open("Calibration Data",'w')
#file0write.write(" \n")
file0write.close()

for i in range(30, 61, 5):
    for j in range (200): #Pump the temperature up to i
        Tlist1 = []
        for k in range(5):
            v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
            v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
            Vt = v01 - v23 #voltage across thermistor
            I = v23/(10^5) #current
            Rt = Vt/I #resistance of thermistor
            T = (2*beta*T0 - alpha - np.sqrt((alpha - 2*beta*T0)**2 - 4*beta*(beta*(T0**2)-alpha*T0-np.log(Rt/R0))))/(2*beta)
            Tlist1.append(T) # stores temperature in a list
            time.sleep(0.02)
        Tarray = np.array(Tlist1, dtype = np.float16)
        Tavg = np.average(Tarray)
        if Tavg < i:
            DEFDUTY = 5
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts) 
        elif Tavg > i:
            DEFDUTY = 0   
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts)
    Tlist2 = []   #For boxcar averaging
    for j in range(5): #Update temperature measurement every 0.1 seconds
        v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
        v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
        Vt = v01 - v23 #voltage across thermistor
        I = v23/(10^5) #current
        Rt = Vt/I #resistance of thermistor
        T = (2*beta*T0 - alpha - np.sqrt((alpha - 2*beta*T0)**2 - 4*beta*(beta*(T0**2)-alpha*T0-np.log(Rt/R0))))/(2*beta)
        Tlist2.append(T) # stores temperature in a list
        time.sleep(0.02)
    Tarray2 = np.array(Tlist2, dtype = np.float16)
    Tavg2 = np.average(Tarray2) #Compute the first average
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    time.sleep(2) #To account the phase shift of 2 seconds between the thermister and RTD readings
    Trtd = rtd_sensor.temperature #RTD readings
    Trtd_list.append(Trtd)
    Tth_list.append(Tavg2)
    Rth_list.append(Rt)
    file0append = open("Calibration Data",'a')
    file0append.write(str(Trtd) + "," + str(Tavg) + "," + str(Rt) + "\r\n")
    file0write.close()

