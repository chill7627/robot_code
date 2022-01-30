import robot
from Raspi_MotorHAT import Raspi_MotorHAT as rmh
from time import sleep

r = robot.Robot()
r.set_left(80)
r.set_right(80)
sleep(1)
