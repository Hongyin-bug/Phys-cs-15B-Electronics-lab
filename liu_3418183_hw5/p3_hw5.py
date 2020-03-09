import numpy as np
import os
import sys
import time
import smbus
from wpdir import wiringpi

### Acceldemo
ADR = 0x18  # default I2C address
CTRL_REG1 = 0x20
CTRL_REG4 = 0x23

OUT_X_L = 0x28
OUT_X_H = 0x29
OUT_Y_L = 0x2a
OUT_Y_H = 0x2b
OUT_Z_L = 0x2c
OUT_Z_H = 0x2d

DATARATE = 0b01110000  # 400 Hz
ENABLE   = 0b00000111  # high-power mode, enable x, y, z
CR1BYTE = DATARATE | ENABLE

g = 9.80665
gv = np.array((0.0, 0.0, g))
FSRANGE = 8*g  # +/- 8g
CR4HIGH = 0b10100000  # block data update on, little endian, +/- 8g
CR4LOW  = 0b00001000  # high-res on, self test disabled, spi mode default
CR4BYTE = CR4HIGH | CR4LOW
###############################################################################

class Lis3dh():
   def __init__(self):
      self.i2c = smbus.SMBus(1)
      self.i2c.write_byte_data(ADR, CTRL_REG1, CR1BYTE)
      self.i2c.write_byte_data(ADR, CTRL_REG4, CR4BYTE)
      self.acceldata = np.zeros(3)

      time.sleep(0.010)  # pause for boot-up

   def read_accel(self):
      x_low  = self.i2c.read_byte_data(ADR, OUT_X_L)
      x_high = self.i2c.read_byte_data(ADR, OUT_X_H)
      y_low  = self.i2c.read_byte_data(ADR, OUT_Y_L)
      y_high = self.i2c.read_byte_data(ADR, OUT_Y_H)
      z_low  = self.i2c.read_byte_data(ADR, OUT_Z_L)
      z_high = self.i2c.read_byte_data(ADR, OUT_Z_H)

      xint = int.from_bytes(bytes((x_low, x_high)), byteorder = 'little',
                            signed = True)
      self.acceldata[0] = float(xint)

      yint = int.from_bytes(bytes((y_low, y_high)), byteorder = 'little',
                            signed = True)
      self.acceldata[1] = float(yint)

      zint = int.from_bytes(bytes((z_low, z_high)), byteorder = 'little',
                            signed = True)
      self.acceldata[2] = float(zint)
      self.acceldata = self.acceldata*FSRANGE/32767

      return(self.acceldata)
############################################################

# pwmdemo.py
DELAY = 5
STEPS = 100

PWM_OUTPUT = 2
PWM_MODE_MS = 0 # standard mark-space PWM
PWMPIN = 18  # Broadcom pin numbering
PWM_RANGE = 3000 # must be less than 4096
PWM_DIVISOR = 2

###############################################################################


# Check user ID - must be running with root privileges
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
        
### code to set pwm

## For part (a)
'''
acc = Lis3dh()
while True:
    accel0 = list(acc.read_accel()) #initial acceleration, includes acceleration of gravity
    wiringpi.delay(1)
    accel1 = list(acc.read_accel()) #final acceleration
    accelx = np.sqrt(accel1[0]*accel1[0]) - np.sqrt(accel0[0]*accel0[0]) #the instantaneous acceleration in each direction
    accely = np.sqrt(accel1[1]*accel1[1]) - np.sqrt(accel0[1]*accel0[1])
    accelz = np.sqrt(accel1[2]*accel1[2]) - np.sqrt(accel0[2]*accel0[2])
    a_ins = np.sqrt(accelx*accelx + accely*accely + accelz*accelz)   #computes the net instantaneous accleration
    if a_ins < 0.5:  #To make sure really small fluctuations (no movement) of measurements will not turn on LED
        a_ins = 0
    else:
        a_ins = a_ins
    pwm = int(a_ins* PWM_RANGE/60)
    wiringpi.pwmWrite(PWMPIN, pwm)
    wiringpi.delay(DELAY)
'''

## For part (b)
acc = Lis3dh()
while True:
    try:
        n = int(input("How many acceleration measurements would you like to make? "))
        if n<=0 or n > 100000000:
            n = int(input("Number out of range, please try another one: "))
    except ValueError:
        print("Your input is either not a number or not an integer, please try again.")
    else:
        accel = 0
        for i in range(n):
            accel0 = list(acc.read_accel()) #initial acceleration, includes accelerationof gravity
            accel1 = list(acc.read_accel()) #final acceleration
            accelx = np.sqrt(accel1[0]*accel1[0]) - np.sqrt(accel0[0]*accel0[0]) #the instantaneous acceleration in each direction
            accely = np.sqrt(accel1[1]*accel1[1]) - np.sqrt(accel0[1]*accel0[1])
            accelz = np.sqrt(accel1[2]*accel1[2]) - np.sqrt(accel0[2]*accel0[2])
            a_ins = np.sqrt(accelx*accelx + accely*accely + accelz*accelz)
            if a_ins < 0.5:
                a_ins = 0
            else:
                a_ins = a_ins
            accel += a_ins
        accel_avg = accel/n     #computes the average acceleration of the n measurements.
        print(accel_avg)
        pwm = int(accel_avg* PWM_RANGE/60)
        wiringpi.pwmWrite(PWMPIN, pwm)
        wiringpi.delay(DELAY)
        
            
        





