P0 = 1
Kp = 0.5

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
#Set point for block temperature
while True:
    try:
        Ts = int(input("What is the temperature you want to set to? (in Celcius)"))
        if Ts<10 or Ts > 70:
            Ts = int(input("Temperature out of range, pls choose one in the range of 30 to 60"))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break
    
#Asks for time interval to record the data
while True:
    try:
        period = int(input("How long do you want to record the temperature for? (in seconds) "))
        if period <=0 or period > 1000000000:
            period = int(input("Time out of range, pls choose one that is positive and not too large!!! "))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break

#Store temperature measurements
file0write=open("Temperature Data",'w')
file0write.write("0 \n")
file0write.close()
Tlist = []
T0rtd0lst = []

#Controller portion
alpha = -0.0767
beta = 7.13145028 * 10**(-4)
R0 = 19.05
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
    for i in range(10): #Update the power every 0.1 second
        v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
        v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
        Vt = v01 - v23 #voltage across thermistor
        I = v23/(10^5) #current
        Rt = Vt/I #resistance of thermistor
        T = (2*beta*T0 - alpha - np.sqrt((alpha - 2*beta*T0)**2 - 4*beta*(beta*(T0**2)-alpha*T0-np.log(Rt/R0))))/(2*beta)
        DEFDUTY = P0 + 0.5*(Ts - T) #Power applied is proportional to the duty cycle and (Ts - T), so duty cycle is proportional to (Ts - T).
        if DEFDUTY >= 0 and DEFDUTY <= 100:
            duty_counts = int(DEFDUTY*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts)
        elif DEFDUTY > 100:
            duty_counts = int(100*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts)
        elif DEFDUTY < 0:
            duty_counts = int(0*PWM_RANGE)
            wiringpi.pwmWrite(PWMPIN, duty_counts)
        time.sleep(0.1)

#In the end, set the duty cycle back to zero to prevent overheating
duty_counts = int(0)
wiringpi.pwmWrite(PWMPIN, duty_counts)

# Plot of temperature over the 10 minutes
x = np.arange(0, period + 1, 1)
y = Tlist


plt.scatter(x, y, s = 10, c = 'yellowgreen',)

plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celcius)")

axes = plt.gca()
axes.set_ylim([0,80])

plt.show()

