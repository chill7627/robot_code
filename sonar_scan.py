import time
import math
import matplotlib.pyplot as plt
from robot import Robot

start_scan = 0
lower_bound = -90
upper_bound = 90
scan_step = 5

the_robot = Robot()
the_robot.set_tilt(0)
scan_data = {}

for facing in range(lower_bound, upper_bound, scan_step):
    the_robot.set_pan(-facing)
    time.sleep(0.1)
    
    scan_data[facing] = the_robot.left_distance_sensor.distance*100
    
axis = [math.radians(facing) for facing in scan_data.keys()]

plt.polar(axis, list(scan_data.values()), 'g-')
plt.savefig('scan.png')