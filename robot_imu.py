from adafruit_lis3mdl import LIS3MDL
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from board import I2C
from vpython import vector, degrees, atan2, radians


class ComplementaryFilter:
    # accelerometer values will be used to help filter out the noise from the gyroscope
    def __init__(self, filter_left=0.9):
        # filter left is the gyro input
        self.filter_left = filter_left
        # filter right is the accelerometer input
        self.filter_right = 1.0 - filter_left

    def filter(self, left, right):
        return self.filter_left * left + self.filter_right * right
    

class ImuFusion:
    def __init__(self, imu, filter_value=0.95):
        self.imu = imu
        self.filter = ComplementaryFilter(filter_value).filter
        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def update(self, dt):
        accel_pitch, accel_roll = self.imu.read_accelerometer_pitch_and_roll()
        gyro = self.imu.read_gyroscope()
        mag = self.imu.read_magnetometer()
        self.pitch = self.filter(self.pitch + gyro.y * dt, accel_pitch)
        self.roll = self.filter(self.roll + gyro.x * dt, accel_roll)
        # rotate mag vector using pitch and tilt the level to xy components
        mag = mag.rotate(radians(self.pitch), vector(0, 1, 0))
        mag = mag.rotate(radians(self.roll), vector(1, 0, 0))
        mag_yaw = -degrees(atan2(mag.y, mag.x))
        # use complimentary filter with gyroscope
        self.yaw = self.filter(self.yaw + gyro.z*dt, mag_yaw)


class RobotIMU:
    def __init__(self, gyro_offsets=None, mag_offsets=None):
        self._i2c = I2C()
        self._accl_gyro = LSM6DSOX(self._i2c)
        self._mag = LIS3MDL(self._i2c)
        self.gyro_offsets = gyro_offsets or vector(0, 0, 0)
        self.mag_offsets = mag_offsets or vector(0, 0, 0)

    def read_magnetometer(self):
        """returns mag_x, mag_y, mag_z"""
        x, y, z = self._mag.magnetic
        return vector(x, y, z) - self.mag_offsets
        
    def read_accelerometer(self):
        """returns accl_x, accl_y, accl_z"""
        x, y, z = self._accl_gyro.acceleration
        return vector(x, y, z)
    
    def read_accelerometer_pitch_and_roll(self):
        accel = self.read_accelerometer()
        pitch = degrees(-atan2(accel.x, accel.z))
        roll = degrees(-atan2(accel.y, accel.z))
        return pitch, roll

    def read_gyroscope(self):
        """returns gyro_x, gyro_y, gyro_z"""
        x, y, z = self._accl_gyro.gyro
        return vector(x, y, z) - self.gyro_offsets