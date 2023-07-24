import subprocess
import time


class RobotModes(object):
    mode_config = {
        "avoid_behavior": "avoid_with_rainbows.py",
        "circle_head": "circle_pan_tilt_behavior.py",
        "test_rainbow": "test_rainbow.py",
        "test_leds": "leds_test.py",
        "line_following": "line_follow_behavior.py",
        "drive_north": "drive_north_behavior.py"
    }

    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Avoid Behavior"},
        {"mode_name": "circle_head", "text": "Circle Head"},
        {"mode_name": "test_leds", "text": "Test LEDs"},
        {"mode_name": "test_rainbow", "text": "LED Rainbow"},
        {"mode_name": "line_following", "text": "Line Following"},
        {"mode_name": "behavior_line", "text": "Drive In A Line"},
        {"mode_name": "drive_north", "text": "Drive North"}
    ]

    def __init__(self) -> None:
        # need to ensure that only one process is running at one time
        self.current_process = None

    def is_running(self):
        # checks if a process is running
        # python subprocess lets us run other processes and has return code on status
        # None if still running
        return self.current_process and self.current_process.returncode is None
    
    def run(self, mode_name):
        while self.is_running():
            self.stop()
        script = self.mode_config[mode_name]
        self.current_process = subprocess.Popen(["python3", script])
        
    def stop(self):
        # used to stop running process
        if self.is_running():
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process.wait()
            self.current_process = None

        