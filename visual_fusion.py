import vpython as vp
from robot_imu import RobotIMU, ImuFusion
from delta_timer import DeltaTimer
import imu_settings
import virtual_robot

imu = RobotIMU(gyro_offsets=imu_settings.gyro_offsets,
               mag_offsets=imu_settings.mag_offsets)
fusion = ImuFusion(imu)

# make a robot vpython canvas
robot_view = vp.canvas(align="left")
model = virtual_robot.make_robot()
virtual_robot.robot_view()
# make a compass vpython canvas
compass = vp.canvas(width=400, height=400)
vp.cylinder(radius=1, axis=vp.vector(0, 0, 1),
            pos=vp.vector(0, 0, -1))
needle = vp.arrow(axis=vp.vector(1, 0, 0),
                  color=vp.color.red)

# set up graphs for pitch, roll, and yaw
vp.graph(xmin=0, xmax=60, scroll=True)
graph_roll = vp.gcurve(color=vp.color.red)
graph_pitch = vp.gcurve(color=vp.color.green)
graph_yaw = vp.gcurve(color=vp.color.blue)

# create a delta timer
timer = DeltaTimer()
while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    # update fusion with time
    fusion.update(dt)
    # reset the virtual model before we rotate it
    model.up = vp.vector(0, 1, 0)
    model.axis = vp.vector(1, 0, 0)
    # perform three rotations: roll, pitch, yaw
    model.rotate(angle=vp.radians(fusion.roll), axis=vp.vector(1, 0, 0))
    model.rotate(angle=vp.radians(fusion.pitch), axis=vp.vector(0, 1, 0))
    model.rotate(angle=vp.radians(fusion.yaw), axis=vp.vector(0, 0, 1))
    # position the compass needle, yaw is in degrees so convert it
    needle = vp.vector(vp.sin(vp.radians(fusion.yaw)),
                       vp.cos(vp.radians(fusion.yaw)),
                       0)
    # plot the the three-graphs axes
    graph_roll.plot(elapsed, fusion.roll)
    graph_pitch.plot(elapsed, fusion.pitch)
    graph_yaw.plot(elapsed, fusion.yaw)