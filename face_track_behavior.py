import time
from image_app_core import start_server_process, get_control_instruction, put_output_image
import cv2
import os
import camera_stream
from pid_controller import PIController
from robot import Robot


class FaceTrackBehavior:
    def __init__(self, robot):
        self.robot = robot
        cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
        cascade_path = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
        assert os.path.exists(cascade_path), f"File {cascade_path} not found"
        self.cascade = cv2.CascadeClassifier(cascade_path)

        self.center_x = 160
        self.center_y = 120
        self.min_size = 20
        self.pan_pid = PIController(proportional_constant=0.1, integral_constant=0.03)
        self.tilt_pid = PIController(proportional_constant=-0.1, integral_constant=-0.03)

        self.running = False

    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == "start":
                self.running = True
            elif command == "stop":
                self.running = False
                self.pan_pid.reset()
                self.tilt_pid.reset()
                self.robot.servos.stop_all()
            elif command == "exit":
                print("Stopping")
                exit()

    def find_object(self, original_frame):
        # make image grayscale for faster processing
        gray_img = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)

        # run cascade detectMultiScale for a list of pattern matches
        # returns objects as rectangles with x,y,width,height values
        objects = self.cascade.detectMultiScale(gray_img)

        # now loop through object and find the largest rectangle
        largest = 0, (0, 0, 0, 0)
        for (x, y, w, h) in objects:
            item_area = w * h 
            if item_area > largest[0]:
                largest = item_area, (x, y, w, h)
        
        return largest[1]
    
    def make_display(self, display_frame):
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes=encoded_bytes)

    def process_frame(self, frame):
        # find object and draw largest rectangle on frame for output
        (x, y, w, h) = self.find_object(frame)
        cv2.rectangle(frame, (x, y), (x + w, y + h), [255, 0, 0])
        self.make_display(frame)

        return x, y, w, h
    
    def run(self):
        # start with camera setup and warm up time
        camera = camera_stream.setup_camera()
        time.sleep(0.1)
        print("Setup Complete")

        # start main loop by processing the frame and checking for control instructions
        for frame in camera_stream.start_stream(camera):
            (x, y, w, h) = self.process_frame(frame)
            self.process_control()

            # only want to move if a large enough object as been detected, 
            # use height of face for min object size as faces are usually taller than wider
            if self.running and h > self.min_size:
                # once robot is running, feed the PIDs and send outputs to pan and tilt servos
                pan_error = self.center_x - (x + (w/2))
                pan_value = self.pan_pid.get_value(pan_error)
                self.robot.set_pan(int(pan_value))

                tilt_error = self.center_y - (y + (h/2))
                tilt_value = self.tilt_pid.get_value(tilt_error)
                self.robot.set_tilt(int(tilt_value))

                print(f"x: {x}, y: {y}, pan_error: {pan_error}, tilt_error: {tilt_error}, pan_value: {pan_value:.2f}, tilt_value: {tilt_value:.2f}")

# set up and run face tracking behavior
print("Setting Up")
behavior = FaceTrackBehavior(Robot())
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()