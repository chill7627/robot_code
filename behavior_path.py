import robot
from time import sleep

def straight(bot, seconds):
    bot.set_left(80)
    bot.set_right(80)
    sleep(seconds)


def turn_left(bot, seconds):
    bot.set_left(30)
    bot.set_right(75)
    sleep(seconds)


def turn_right(bot, seconds):
    bot.set_left(75)
    bot.set_right(30)
    sleep(seconds)


def spin_left(bot, seconds):
    bot.set_left(-80)
    bot.set_right(80)
    sleep(seconds)


bot = robot.Robot()
# go straight for one second
straight(bot, 1)
# turn right for one second
turn_right(bot, 1)
# go straight for one second
straight(bot, 1)
# turn left for one second
turn_left(bot, 1)
# go straight for one second
straight(bot, 1)
# turn left for one second
turn_left(bot, 1)
# go straight for one second
straight(bot, 1)
# spin_left for one second
spin_left(bot, 1)
