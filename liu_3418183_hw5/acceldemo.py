#!/usr/bin/env python3

#
# acceldemo.py - Demonstrate accelerometer measurement
#
# 10Feb19  Vectorized g
# 20Feb18  Everett Lipman
#

import os
import sys
import time
import numpy as np
import smbus

#
# constants
#
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
###############################################################################

if __name__ == '__main__':

   acc = Lis3dh()
   while True:
      accel = acc.read_accel()
      print('ax: %7.3f    ay: %7.3f    az: %7.3f' % tuple(accel), end='')
      a = np.sqrt(accel.dot(accel))
      angv = accel - gv
      ang = np.sqrt(angv.dot(angv))
      print('    |a|: %6.3f' % a, end='')
      print('    |a-g|: %7.3f' % ang)