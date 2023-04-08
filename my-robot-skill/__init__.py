from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import requests


# this is setting intents
# mycroft uses settingsmeta.json file for config settings
# mycroft uses requirements.txt for installing required packages
# for instance here, we need settings to pull in base_url
# and we use requests package so that needs to be in requirements.txt file
# vocabulary filses go in vocab/<IETF language and locale>
#   they contain phrases that can be used to trigger certain vocab words and thus intents
#   in this instance we need a vocab file for robot synonyms and testrainbow synonyms
#   put in vocab folder
#   mycroft matches phrases there to the the word robot in intent etc.
# dialog files work similarly but they define what the robot says in repsonse back to you
# upload the whole skills folder to /opt/mycroft/skills folder on the agent rpi.
class MyRobot(MycroftSkill):
    def __init__(self):
        super().__init__()
        self.base_url = self.settings.get("base_url", "http://myrobot.local:5000")

    # intent handler takes require to set up vocabulary words, vocabulary set up in separate file
    @intent_handler(IntentBuilder("").require("Robot").require("TestRainbow"))
    def handle_test_rainbow(self, message):
        self.handle_control('/run/test_rainbow', 'TestRainbow')

    # build stop intent
    @intent_handler(IntentBuilder("").require("Robot").require("stop"))
    def handle_stop(self, message):
        self.handle_control('/stop', 'stopping')

    def handle_control(self, end_point, dialog_verb):
        try:
            requests.post(self.base_url + end_point)
            self.speak_dialog('Robot')
            self.speak_dialog(dialog_verb)
        except:
            self.speak_dialog('UnableToReach')
            LOG.exception('Unable to reach the robot')

# mycroft expects this method in all skill files
def create_skill():
    return MyRobot()