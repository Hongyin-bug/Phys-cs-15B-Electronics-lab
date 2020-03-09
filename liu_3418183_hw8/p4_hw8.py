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
temp = 45 #Set point for block temperature
period = 180 #Record data for 3 minutes, in seconds

#Store temperature measurements
file0write=open("Temperature Data",'w')
file0write.write("0 \n")
file0write.close()
Tlist = []
T0rtd0lst = []

#Controller portion
alpha = -0.048
beta = 0.0001
R0 = 16.310
T0 = 22.720

for i in range(period+1):
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    T = (2*beta*T0 - alpha - np.sqrt((alpha - 2*beta*T0)**2 - 4*beta*(beta*(T0**2)-alpha*T0-np.log(Rt/R0))))/(2*beta)
    Tlist.append(T)  #stores temperature data in a list and a textfile
    file0append = open("Temperature Data",'a')
    file0append.write(str(T) + "\r\n")
    file0write.close()
    Trtd = rtd_sensor.temperature
    T0rtd0lst.append(Trtd)
    for i in range(5): #Stores temperature every 0.5 seconds
        v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
        v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
        Vt = v01 - v23 #voltage across thermistor
        I = v23/(10^5) #current
        Rt = Vt/I #resistance of thermistor
        T = (2*beta*T0 - alpha - np.sqrt((alpha - 2*beta*T0)**2 - 4*beta*(beta*(T0**2)-alpha*T0-np.log(Rt/R0))))/(2*beta)
        if T < temp: 
            DEFDUTY = 5
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts) 
        elif T > temp:
            DEFDUTY = 0    #set pwm cycle to 0%
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts) #set pwm cycle here 
        time.sleep(0.1)


# Plot 
x = np.arange(0, period + 1, 1)
ybang = Tlist
yrtd = T0rtd0lst

plt.scatter(x, ybang, s = 6, marker = '.', c = 'yellowgreen', label = 'Thermister')
plt.scatter(x, yrtd, s = 6, marker = '>', c = 'b', label = 'RTD')

plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celcius)")

axes = plt.gca()
axes.set_ylim([0,60])

plt.legend()
plt.show()

