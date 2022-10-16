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
