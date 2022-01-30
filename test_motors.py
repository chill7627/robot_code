from Raspi_MotorHAT import Raspi_MotorHAT as RMH
import time
import atexit

mh = RMH(addr=0x60)
lm = mh.getMotor(1)
rm = mh.getMotor(2)

def turn_off_motors():
    lm.run(RMH.RELEASE)
    rm.run(RMH.RELEASE)

atexit.register(turn_off_motors)
lm.setSpeed(100)
rm.setSpeed(150)
lm.run(RMH.FORWARD)
rm.run(RMH.FORWARD)
time.sleep(1)
