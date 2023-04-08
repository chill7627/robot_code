from flask import Flask
from robot_modes import RobotModes


# build flask app
app = Flask(__name__)
mode_manager = RobotModes()


# set up routes/api endpoints
@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # function that runs when there is a post request to /run/<mode_name> path/url
    mode_manager.run(mode_name)
    return "%s running"

@app.route("/stop", methods=['POST'])
def stop():
    mode_manager.stop()
    return "stopped"


# start up the flask server
app.run(host="0.0.0.0", debug=True)