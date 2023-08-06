import time
from robot import Robot
from image_app_core import start_server_process, get_control_instruction, put_output_image
import camera_stream


# safety timeout for safety action if no user input is detected in this time
TIMEOUT_IN_SECONDS=1

class ManualDriveBehavior(object):
    def __init__(self, robot):
        self.robot = robot
        self.last_time = time.time()

    # control function, resets the last time for every instruction
    def process_control(self):
        instruction = get_control_instruction()
        while instruction:
            self.last_time = time.time()
            self.handle_instruction(instruction)
            instruction = get_control_instruction()

    def handle_instruction(self, instruction):
        # instruction is a dictionary with name as key and params as values
        command = instruction['command']
        if command == 'set_left':
            self.robot.set_left(int(instruction['speed']))
        elif command == 'set_right':
            self.robot.set_right(int(instruction['speed']))
        elif command == 'exit':
            print("stopping")
            exit()
        # handle unknown commands
        else:
            raise ValueError(f"Unknown instruction: {instruction}")
        
    def make_display(self, frame):
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)

    def run(self):
        # initial robot warm up
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        camera = camera_stream.setup_camera()
        time.sleep(0.1)
        self.robot.servos.stop_all()
        print("Setup Complete")

        # main run loop
        for frame in camera_stream.start_stream(camera):
            self.make_display(frame)
            self.process_control()

            # safety autostop based on timeout set
            if time.time() > self.last_time + TIMEOUT_IN_SECONDS:
                self.robot.stop_motors()

# create robot class behavior and start components
print("Setting up")
behavior = ManualDriveBehavior(Robot())
process = start_server_process('manual_drive.html')

# if we exit or hit a run time error, exit process
try:
    behavior.run()
except:
    process.terminate()