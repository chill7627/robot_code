from adafruit_lis3mdl import LIS3MDL
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from board import I2C
from vpython import vector


class RobotIMU:
    def __init__(self, gyro_offsets=None):
        self._i2c = I2C()
        self._accl_gyro = LSM6DSOX(self._i2c)
        self._mag = LIS3MDL(self._i2c)
        self.gyro_offsets = gyro_offsets or vector(0, 0, 0)

    def read_magnetometer(self):
        """returns mag_x, mag_y, mag_z"""
        x, y, z = self._mag.magnetic
        return vector(x, y, z)
        
    def read_acclerometer(self):
        """returns accl_x, accl_y, accl_z"""
        x, y, z = self._accl_gyro.acceleration
        return vector(x, y, z)

    def read_gyroscope(self):
        """returns gyro_x, gyro_y, gyro_z"""
        x, y, z = self._accl_gyro.gyro
        return vector(x, y, z) - self.gyro_offsets