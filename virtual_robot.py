import vpython as vp
from robot_pose import robot_view
import logging


def make_robot():
    chassis_width = 155
    chassis_thickness = 3
    chassis_length = 200
    wheel_thickness = 26
    wheel_diameter = 70
    axle_x = 30
    axle_z = -20
    castor_position = vp.vector(-80, -6, -30)
    castor_radius = 14
    castor_thickness = 12
    base = vp.box(length=chassis_length, height=chassis_thickness, width=chassis_width)
    # rotate to match body coord sys
    base.rotate(angle=vp.radians(90), axis=vp.vector(1, 0, 0))
    wheel_dist = chassis_width/2
    wheel_l = vp.cylinder(radius=wheel_diameter/2, length=wheel_thickness, pos=vp.vector(axle_x, -wheel_dist, axle_z),
                          axis=vp.vector(0, -1, 0))
    wheel_r = vp.cylinder(radius=wheel_diameter/2,
                          length=wheel_thickness,
                          pos=vp.vector(axle_x, wheel_dist, axle_z),
                          axis=vp.vector(0, 1, 0))
    castor = vp.cylinder(radius=castor_radius,
                         length=castor_thickness,
                         pos=castor_position,
                         axis=vp.vector(0, 1, 0))
    return vp.compound([base, wheel_l, wheel_r, castor])

if __name__ == '__main__':
    # this will only run if py file called directly and won't run if it is imported
    logging.basicConfig(level=logging.INFO)
    robot_view()
    x_arrow = vp.arrow(axis=vp.vector(200, 0, 0), color=vp.color.red)
    y_arrow = vp.arrow(axis=vp.vector(0, 200, 0), color=vp.color.green)
    z_arrow = vp.arrow(axis=vp.vector(0, 0, 200), color=vp.color.blue)
    make_robot()
