from flask import Flask, render_template, jsonify
from robot_modes import RobotModes
from leds_led_shim import Leds


# build flask app
app = Flask(__name__)
mode_manager = RobotModes()
leds = Leds()
leds.set_one(1, [0, 255, 0])
leds.show()

# route for template
@app.route('/')
def index():
    # this passes the mode manager menu config to the menu.html template
    return render_template('menu.html', menu=mode_manager.menu_config)

# set up routes/api endpoints
@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # check if leds are on and clear if so, leds just used to show that robot is ready
    global leds
    if leds:
        leds.clear()
        leds.show()
        leds = None
    # function that runs when there is a post request to /run/<mode_name> path/url
    mode_manager.run(mode_name)
    response = {"message": f'{mode_name} running'}
    # check to see if the response should be redirected
    if mode_manager.should_redirect(mode_name):
        response['redirect'] = True
    return jsonify(response)

@app.route("/stop", methods=['POST'])
def stop():
    mode_manager.stop()
    return jsonify({'message': 'Stopped'})

@app.after_request
def add_header(response):
    # we are actively changing the style sheet, so we need to stop devices holding a stale, cached copy of the sheet
    # this is achieved by adding a header to all responses.
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response


# start up the flask server, debug should only be used in testing and never in production
app.run(host="0.0.0.0", debug=False)