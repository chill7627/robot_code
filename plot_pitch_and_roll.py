import vpython as vp
from delta_timer import DeltaTimer
from robot_imu import RobotIMU, ImuFusion
import imu_settings


imu = RobotIMU(gyro_offsets=imu_settings.gyro_offsets)
fusion = ImuFusion(imu)
timer = DeltaTimer()
vp.graph(xmin=0, xmax=60, scroll=True)
graph_pitch = vp.gcurve(color=vp.color.red)
graph_roll = vp.gcurve(color=vp.color.green)

while True:
    vp.rate(100)
    dt, elapsed = timer.update()
    fusion.update(dt)
    graph_pitch.plot(elapsed, fusion.pitch)
    graph_roll.plot(elapsed, fusion.roll)