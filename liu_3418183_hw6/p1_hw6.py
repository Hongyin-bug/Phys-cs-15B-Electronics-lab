SPS = 920
sinterval = 1.0/SPS

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

 #Ask user for signal frequency
while True:
    try:
        f = float(input("What is the wave frequency you want to set to? "))
        if f <=0 or f > 100000000:
            f = float(input("Frequency out of range, pls choose one that is positive and not too large!!! "))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break

#Graph of signal
xsignals = np.arange(0, 20/f, 1/(f*10000))
ysignals = 0.5*np.sin(2*f*np.pi*xsignals) + 1

plt.scatter(xsignals,ysignals, s = 2, c = 'yellowgreen')

#Graph of sampling dots      
xsamples = np.arange(0, 20/f, 1/(920))
ysamples = 0.5*np.sin(2*f*np.pi*xsamples) + 1

plt.scatter(xsamples,ysamples, s = 20, c = 'teal')

#Fit sine wave to find measured frequency

def fitfxn(xsamples, frequency):
    return 0.5*np.sin(2*frequency*np.pi*xsamples) + 1

param, param_cov = curve_fit(fitfxn, xsamples, ysamples) 

plt.xlabel("Time (s)")
plt.ylabel("Voltage(V)")
plt.show()
