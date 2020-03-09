import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import sys
import time
from Adafruit import ADS1x15
adc = ADS1x15()

 #Ask user for signal frequency
while True:
    try:
        period = int(input("How long do you want to record the temperature for? (in seconds) "))
        if period <=0 or period > 1000000000:
            period = int(input("Time out of range, pls choose one that is positive and not too large!!! "))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break


################
file0write=open("Temperature Data",'w')
file0write.write("0 \n")
file0write.close()
Tlist = []

for i in range (0, period+1):
    v23 = adc.readADCDifferential23(4096, 128)*0.001 #voltage across resistance
    v01 = adc.readADCDifferential01(4096, 128)*0.001 #volage across thermistor
    Vt = v01 - v23 #voltage across thermistor
    I = v23/(10^5) #current
    Rt = Vt/I #resistance of thermistor
    T = 263.84 - 5000*np.sqrt(0.002304 + 0.0004*np.log(Rt/15.73))
    Tlist.append(T)
    file0append = open("Temperature Data",'a')
    file0append.write(str(T) + "\r\n")
    file0write.close()
    time.sleep(1)


#plot
x = np.arange(0, period + 1, 1)
y = Tlist

plt.scatter(x, y, s = 5, c = 'yellowgreen')


plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celcius)")
plt.show()

#Determine time constant
def fitfxn(x, tau, T0, T00):
    return T0 * np.exp(-x/tau) + T00

param, param_cov = curve_fit(fitfxn, x, y)
print(param, param_cov)