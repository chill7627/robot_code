import subprocess
import time


class RobotModes(object):
    mode_config = {
        "avoid_behavior": "avoid_with_rainbows.py",
        "circle_head": "circle_pand_tilt.py",
        "test_rainbow": "test_rainbow.py"
    }

    def __init__(self) -> None:
        # need to ensure that only one process is running at one time
        self.current_process = None

    def is_running(self):
        # checks if a process is running
        # python subprocess lets us run other processes and has return code on status
        # None if still running
        return self.current_process and self.current_process.returncode is None
    
    def run(self, mode_name):
        if not self.is_running():
            script = self.mode_config[mode_name]
            self.current_process = subprocess.Popen(["python3", script])
            return True
        else:
            # if there is a process already running
            return False
        
    def stop(self):
        # used to stop running process
        if self.is_running():
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process.wait()
            self.current_process = None

        