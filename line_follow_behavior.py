import time
from image_app_core import start_server_process, get_control_instruction, put_output_image
import cv2
import numpy as np
import camera_stream
from pid_controller import PIController
from robot import Robot
import os


class LineFollowingBehavior:
    def __init__(self, robot, log_file=None) -> None:
        self.robot = robot
        self.check_row = 180
        self.diff_threshold = 10
        self.center = 160
        self.running = False
        self.speed = 45
        self.crosshair_color = [0, 255, 0]
        self.line_middle_color = [128, 128, 255]
        self.graph_color = [255, 128, 128]
        self.log_file = log_file

    def process_control(self):
        """Processes control commands from the http request queue.
           Checks current state of robot and the request from the queue, then takes 
           appropriate action."""
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == 'start':
                self.running = True
            elif command == 'stop':
                self.running = False
            elif command == 'exit':
                print('Stopping')
                exit()

    def run(self):
        """Runs main pid lopp and drives the robot.  Set the pan and tilt to 0 and 90.
           Looking straight down."""
        self.robot.set_pan(0)
        self.robot.set_tilt(90)
        camera = camera_stream.setup_camera()

        # set up pid
        direction_pid = PIController(proportional_constant=0.25, integral_constant=0.01, 
                                     windup_limit=400)
        time.sleep(1)
        # stop the servos after initial positioning so they don't drain power.
        self.robot.servos.stop_all()
        print('Setup Complete')

        # keep track of time
        last_time = time.time()

        # start processing camera frames
        for frame in camera_stream.start_stream(camera):
            x, magnitude = self.process_frame(frame)
            self.process_control()

            # now move the robot, keep track of time since last movement, calculate error and feed dt and 
            # x pos error into the pid controller, reset last_time to new_time
            if self.running and magnitude > self.diff_threshold:
                direction_error = self.center - x
                new_time = time.time()
                dt = new_time - last_time
                direction_value = direction_pid.get_value(direction_error, delta_time=dt)
                last_time = new_time

                # now set motor speeds based off of pid return, log error to file
                print(f"Error:{direction_error}, Value:{direction_value:2f}, t:{new_time}")
                if os.path.exists(self.log_file):
                    with open(self.log_file, 'a') as f:
                        f.write(f"{direction_error},{direction_value:2f},{new_time}\n")
                else:
                    with open(self.log_file, 'w+') as f:
                        f.write("direction_error,direction_value,new_time\n")
                        f.write(f"{direction_error},{direction_value:2f},{new_time}\n") 
                self.robot.set_left(self.speed - direction_value)
                self.robot.set_right(self.speed + direction_value)

            # now stop motors and reset pids in case line is lost
            else:
                self.robot.stop_motors()
                self.running = False
                direction_pid.reset()
                # still keep track of last_time to not confuse pid controller
                last_time = time.time()

    def process_frame(self, frame):
        """Process the image frame and find line and its mid point"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.blur(gray, (5, 5))
        row = blur[self.check_row].astype(np.int32)
        diff = np.diff(row)
        max_d = np.amax(diff, 0)
        min_d = np.amin(diff, 0)

        # check to see if it is actually a line
        if max_d < 0 or min_d > 0:
            return 0, 0
        
        # continue processing and find min max positions and the mid point between them
        highest = np.where(diff == max_d)[0][0]
        lowest = np.where(diff == min_d)[0][0]
        middle = (highest + lowest) // 2
        # make sure that it picked up the line and not some line like artifact, by checking mag of min max change
        mag = max_d - min_d

        # make display
        self.make_display(frame, middle, lowest, highest, diff)

        return middle, mag
    
    def make_display(self, frame, middle, lowest, highest, diff):
        # make crosshair about center and chosen image row
        cv2.line(frame, (self.center - 4, self.check_row), (self.center + 4, self.check_row), self.crosshair_color)
        cv2.line(frame, (self.center, self.check_row - 4), (self.center, self.check_row + 4), self.crosshair_color)

        # show were found line middle is
        cv2.line(frame, (middle, self.check_row - 8), (middle, self.check_row + 8), self.line_middle_color)
        # plot bars for found edges with min and max contrast delta method
        cv2.line(frame, (lowest, self.check_row - 4), (lowest, self.check_row + 4), self.line_middle_color)
        cv2.line(frame, (highest, self.check_row - 4), (highest, self.check_row + 4), self.line_middle_color)

        # graph diff across empty frame
        graph_frame = np.zeros((camera_stream.size[1], camera_stream.size[0], 3), np.uint8)
        self.make_cv2_simple_graph(graph_frame, diff)

        # concatenate frames
        display_frame = np.concatenate((frame, graph_frame), axis=1)

        # encode bytes and put on image queue
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

    def make_cv2_simple_graph(self, frame, data):
        """This is because pyplot is too slow, have to do graphics render tricks"""
        last = data[0]
        graph_middle = 100

        # enumerate data to plot each item
        for x, item in enumerate(data):
            cv2.line(frame, (x, last + graph_middle), (x + 1, item + graph_middle), self.graph_color)
            last = item

# now intialize robot and run class behavior
print('Setting up')
behavior = LineFollowingBehavior(Robot(), log_file='pid_log.csv')
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()
