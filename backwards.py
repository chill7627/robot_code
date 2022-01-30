import robot
from time import sleep

bot = robot.Robot()

def backwards(bot, seconds):
    bot.set_left(-80)
    bot.set_right(-80)
    sleep(seconds)

backwards(bot, 1)
