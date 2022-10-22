import time
from image_app_core import start_server_process, get_control_instruction, put_output_image
import cv2
import numpy as np
import camera_stream
from pid_controller import PIController
from robot import Robot


class ColorTrackingBehavior:
    def __init__(self, robot):
        self.robot = robot
        # tune these to color mask and object size
        # range of 25 - 80 for hue is 50 to 160 on hue wheel.
        # saturation is 70 to 255 any lower and start to detect washed out or gray colors.
        # light is 25 very dark to 255 fully lit
        self.low_range = (25, 70, 25)
        self.high_range = (80, 255, 255)
        # correct radius sets the size we intend to keep the object at and behaves as a distance setting
        self.correct_radius = 120
        # center should be half the horizontal resolution of the pics we capture
        self.center = 160
        # running used to switch motors and movement on and off
        self.running = False

    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == 'start':
                self.running = True
            if command == 'stop':
                self.running = False
            if command == 'exit':
                print('Stopping')
                exit()

    def find_object(self, original_frame):
        """Find the largest enclosing circle for all contours in a masked image.
           Returns: the masked image, the object coordinates, the object radius"""
        # convert the frame to HSV, create mask of in range pixels
        frame_hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2HSV)
        masked = cv2.inRange(frame_hsv, self.low_range, self.high_range)
        # draw contours around masked objects
        contours, _ = cv2.findContours(masked, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # find all enclosing circles for each contour found with minEnclosing-Circle method
        circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]
        # circles are radii and coordinates
        # now filter for biggest circles
        largest = (0, 0), 0
        for (x, y), radius in circles:
            if radius > largest[1]:
                largest = (int(x), int(y)), int(radius)

        return masked, largest[0], largest[1]

    def make_display(self, frame, processed):
        """Take the original frame and processed frame then turn them into a dual-screen display
           on output queue through to the web app"""
        display_frame = np.concatenate((frame, processed), axis=1) # change axis to 0 to stack frames vertically
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

    def process_frame(self, frame):
        # process frame
        masked, coordinates, radius = self.find_object(frame)
        # changes masked image to 3 channel image
        processed = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
        # draws same circle on original frame for comparsion on web app
        cv2.circle(frame, coordinates, radius, [255, 0, 0])
        self.make_display(frame, processed)
        return coordinates, radius

    def run(self):
        # runs the behavior
        # set servos on pan and tilt camera to 0 position (forward)
        self.robot.set_pan(0)
        self.robot.set_tile(0)
        # setup camera stream
        camera = camera_stream.setup_camera()
        # set up pid controllers
        # pid for speed based on radius
        speed_pid = PIController(proportional_constant=0.8, integral_constant=0.1, windup_limit=100)
        # pid for direction based on distance
        direction_pid = PIController(proportional_constant=0.25, integral_constant=0.05, windup_limit=400)

        # sleep to allow servos and camera to warm up
        time.sleep(0.1)
        # stop servos at center position
        self.robot.servos.stop_all()
        print('Setup Complete')
        print('Radius, Radius error, speed value, direction, error, direction value')

        # main loop
        for frame in camera_stream.start_stream(camera):
            (x, y), radius = self.process_frame(frame)

            # check for control messages from web app and for objects big enough to look for
            self.process_control()
            if self.running and radius > 20:
                # robot should be moving
                # run pid loops
                radius_error = self.correct_radius - radius
                speed_value = speed_pid.get_value(radius_error)
                # use center coordinate and current object, x to get direction error
                direction_error = self.center - x
                direction_value = direction_pid.get_value(direction_error)
                print(f"""{radius}, {radius_error}, {speed_value:.2f}, {direction_error},
                      {direction_error}, {direction_value:.2f}""")
                # produce motor speeds
                self.robot.set_left(speed_value - direction_value)
                self.robot.set_right(speed_value + direction_value)
            else:
                # if no object worth examining or stop is sent from web app
                self.robot.stop_motors()
                if not self.running:
                    speed_pid.reset()
                    direction_pid.reset()

print('Setting up')
behavior = ColorTrackingBehavior(Robot())
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()
