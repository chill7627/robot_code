from Raspi_MotorHAT import Raspi_MotorHAT as rmh
from gpiozero import DistanceSensor
import atexit

class Robot:
    def __init__(self, motorhat_addr=0x60):
        # Setup the motorhat with the passed address
        self._mh = rmh(addr=motorhat_addr)
        # get local variable for each motorhat
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)
        # set up the distance sensors
        self.left_distance_sensor = DistanceSensor(echo=5, trigger=6, queue_len=2)
        self.right_distance_sensor = DistanceSensor(echo=17, trigger=27, queue_len=2)
        # ensure the motors get stopped when the code exits
        atexit.register(self.stop_motors)

    def convert_speed(self, speed):
        # Choose the running mode
        mode = rmh.RELEASE
        if speed > 0:
            mode = rmh.FORWARD
        elif speed < 0:
            mode = rmh.BACKWARD
        # Scale the speed
        output_speed = abs((speed*255)) // 100
        return mode, int(output_speed)

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)

    def stop_motors(self):
        self.left_motor.run(rmh.RELEASE)
        self.right_motor.run(rmh.RELEASE)
