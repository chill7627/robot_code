import vpython as vp
from robot_imu import RobotIMU
from delta_timer import DeltaTimer
import imu_settings

imu = RobotIMU(mag_offsets=imu_settings.mag_offsets)
# dial and needle for compass
vp.cylinder(radius=1, axis=vp.vector(0, 0, 1),
            pos=vp.vector(0, 0, -1))
needle = vp.arrow(axis=vp.vector(1, 0, 0),
                  color=vp.color.red)
# make a graph to show the heading
vp.graph(xmin=0, xmax=60, scroll=True)
graph_yaw = vp.gcurve(color=vp.color.blue)
timer = DeltaTimer()

# main loop
while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    mag = imu.read_magnetometer()
    # find the heading from atan of xy plane and plot it
    yaw = -vp.atan2(mag.y, mag.x)
    graph_yaw.plot(elapsed, vp.degrees(yaw))
    # set the needle axis to our direction, using sin/cos to convert it back into a unit direction
    needle.axis = vp.vector(vp.sin(yaw), vp.cos(yaw), 0)