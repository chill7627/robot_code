from robot_imu import RobotIMU
import time
import vpython as vp


# this code is used to calibrate the gyroscope offset by running measurements on a flat surface
imu = RobotIMU()
# hold min and max values of the gyroscope
gyro_min = vp.vector(0, 0, 0)
gyro_max = vp.vector(0, 0, 0)

# run loop for many readings over time
for n in range(500):
    gyro = imu.read_gyroscope()
    # measure for a while to get the min and max values for each axis
    gyro_min.x = min(gyro_min.x, gyro.x)
    gyro_min.y = min(gyro_min.y, gyro.y)
    gyro_min.z = min(gyro_min.z, gyro.z)
    gyro_max.x = max(gyro_max.x, gyro.x)
    gyro_max.y = max(gyro_max.y, gyro.y)
    gyro_max.z = max(gyro_max.z, gyro.z)
    # middle of two vectors is an estimate of how far we are from zero
    offset = (gyro_min + gyro_max) / 2
    # sleep before next loop
    time.sleep(0.01)
    # print offset values for use
    print(f"Zero offset: {offset}.")