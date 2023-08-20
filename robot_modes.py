import subprocess
import time


class RobotModes(object):
    mode_config = {
        "avoid_behavior": {"script": "avoid_with_rainbows.py"},
        "circle_head": {"script": "circle_pan_tilt_behavior.py"},
        "test_rainbow": {"script": "test_rainbow.py"},
        "test_leds": {"script": "leds_test.py"},
        "line_following": {"script", "line_follow_behavior.py"},
        "drive_north": {"script": "drive_north_behavior.py"},
        "color_track": {"script": "color_track_behavior.py", "server": True},
        "face_track": {"script": "face_track_behavior.py", "server": True},
        "manual_drive": {"script": "manual_drive.py", "server": True}
    }

    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Avoid Behavior"},
        {"mode_name": "circle_head", "text": "Circle Head"},
        {"mode_name": "test_leds", "text": "Test LEDs"},
        {"mode_name": "test_rainbow", "text": "LED Rainbow"},
        {"mode_name": "line_following", "text": "Line Following"},
        {"mode_name": "behavior_line", "text": "Drive In A Line"},
        {"mode_name": "drive_north", "text": "Drive North"},
        {"mode_name": "color_track", "text": "Color Track"},
        {"mode_name": "face_track", "text": "Face Track"},
        {"mode_name": "manual_drive", "text": "Manual Drive"}
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
        script = self.mode_config[mode_name]['script']
        self.current_process = subprocess.Popen(["python3", script])

    def should_redirect(self, mode_name):
        return self.mode_config[mode_name].get('server') is True and self.is_running()
        
    def stop(self):
        # used to stop running process
        if self.is_running():
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process.wait()
            self.current_process = None

        