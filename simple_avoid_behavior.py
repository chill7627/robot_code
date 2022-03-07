from robot import Robot
from time import sleep

class ObstacleAvoidingBehavior:
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60

    def get_motor_speed(self, distance):
        """This method chooses a speed for a motor based on the distance from a
        sensor"""
        if distance < 0.2:
            return -self.speed
        else:
            return self.speed

    def run(self):
        #self.robot.set_pan(0)
        #self.robot.set_tilt(0)

        while True:
            # get the sensor readings in meters
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            print("Left: {l:.2f}, Right: {r:.2f}".format(l=left_distance, r=right_distance))
            # get speeds for motors from distances
            left_speed = self.get_motor_speed(left_distance)
            self.robot.set_left(left_speed)
            right_speed = self.get_motor_speed(right_distance)
            self.robot.set_right(right_speed)

            # wait a little
            sleep(0.05)
bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()
