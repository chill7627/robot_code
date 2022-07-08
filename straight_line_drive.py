from robot import Robot
from pid_controller import PIController
import time
import logging

# set up logging
logger = logging.getLogger('straight_line')
logging.basicConfig(level=logging.INFO)
logging.getLogger('pid_controller').setLevel(logging.DEBUG)

# set up robot speed and runtime
bot=Robot()
stop_at_time = time.time() + 15
speed = 80
bot.set_left(speed)
bot.set_right(speed)

# set up pid controller, constants may need to be tuned
pid = PIController(proportional_constant=5, integral_constant=0.3)

# main loop
while time.time() < stop_at_time:
    # good idea to have some sleep so encoders can get a measurement and 
    # give other things a chance to run and get measurements
    time.sleep(0.01)

    #Calculate the error
    left = bot.left_encoder.pulse_count
    right = bot.right_encoder.pulse_count
    error = left-right

    # get the speed
    adjustment = pid.get_value(error)
    right_speed = int(speed + adjustment)
    left_speed = int(speed - adjustment)

    # logging information
    logger.debug(f"error: {error}, adjustment: {adjustment:.2f}")
    logger.info(f"left: {left}, right: {right}, left_speed: {left_speed}, right_speed: {right_speed}")

    # set motor speeds to adjusted values
    bot.set_left(left_speed)
    bot.set_right(right_speed)     
