import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

file0readinput = np.loadtxt("Calibration Data", delimiter = ',') #The file is comma separated
file0read = np.transpose(file0readinput)
Trtd = file0read[0] #Temperature read by RTD
Rt = file0read[2] #Resistance reading of the thermister

R = list(map(float,Rt))
T = list(map(float,Trtd))


#Fit function for parameters
def fitfxn(T, R0, alpha, beta): #find constants for R(T)
    T0 = 22.720
    return R0*np.exp(alpha*(T-T0) + beta*((T-T0)**2))

param, paramcov = curve_fit(fitfxn, T, R, [16.310,-0.048,0.00001])  #fitfxn, x, y; R(T)
xdata = np.linspace(25,65,1000)
ydata = fitfxn(xdata, param[0],param[1],param[2])

#Plot
plt.plot(T, R, marker = '.', c = 'yellowgreen', label = 'Data')
plt.plot(xdata,ydata, label = 'Fit')

plt.xlabel("Temperature (Celcius)")
plt.ylabel("Resistance (Kilo-Ohms)")

plt.legend()
plt.show()
