import vpython as vp
import logging
import time
from robot_imu import RobotIMU

logging.basicConfig(level=logging.INFO)
imu = RobotIMU()

vp.graph(xmin=0, xmax=60, scroll=True)
graph_x = vp.gcurve(color=vp.color.red)
graph_y = vp.gcurve(color=vp.color.green)
graph_z = vp.gcurve(color=vp.color.blue)

start = time.time()
while True:
    vp.rate(100)
    elapsed = time.time() - start
    gyro = imu.read_gyroscope()
    graph_x.plot(elapsed, gyro.x)
    graph_y.plot(elapsed, gyro.y)
    graph_z.plot(elapsed, gyro.z)