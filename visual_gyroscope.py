import vpython as vp
from robot_imu import RobotIMU
import time
import imu_settings
import virtual_robot


imu = RobotIMU(gyro_offsets=imu_settings.gyro_offsets)
# initialize pitch, roll, yaw, and initial latest time as current time
pitch = 0
roll = 0
yaw = 0
# initialize model and virtual robot
model = virtual_robot.make_robot()
virtual_robot.robot_view()
latest = time.time()

while True:
    vp.rate(100000)
    current = time.time()
    dt = current - latest
    latest = current
    gyro = imu.read_gyroscope()
    # integrate the current rate in degrees per second multiplied by dt
    roll += gyro.x * dt * 50
    pitch += gyro.y * dt * 50
    yaw += gyro.z * dt * 50
    # reset the model's orientation to prepare it for rotation
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # rotate by each axis, convert degrees into radians, and an axis/vector to rotate around
    # vector is (x, y, z)
    model.rotate(angle=vp.radians(roll), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(pitch), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(yaw), axis=vp.vector(0, 0, 1))