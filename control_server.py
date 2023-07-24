from flask import Flask, render_template
from robot_modes import RobotModes


# build flask app
app = Flask(__name__)
mode_manager = RobotModes()


# route for template
@app.route('/')
def index():
    # this passes the mode manager menu config to the menu.html template
    return render_template('menu.html', menu=mode_manager.menu_config)

# set up routes/api endpoints
@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # function that runs when there is a post request to /run/<mode_name> path/url
    mode_manager.run(mode_name)
    return f"{mode_name} running"

@app.route("/stop", methods=['POST'])
def stop():
    mode_manager.stop()
    return "stopped"

@app.after_request
def add_header(response):
    # we are actively changing the style sheet, so we need to stop devices holding a stale, cached copy of the sheet
    # this is achieved by adding a header to all responses.
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response


# start up the flask server
app.run(host="0.0.0.0", debug=True)