
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xsamples = [260, 360, 410, 440, 450, 460, 470, 480, 510, 560, 660]
ysamples = [4,4,4,4,4,4,3.8,3.8,4,4,4]

plt.scatter(xsamples,ysamples, s = 20, c = 'teal')

plt.xlabel("Frequency (s)")
plt.ylabel("AmplitudeV)")
plt.show()
