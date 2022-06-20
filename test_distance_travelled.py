from robot import Robot
import time
import math
import logging

logger = logging.getLogger("test_distance_travelled")

# need to come back and set these with measured values
wheel_diameter_mm = 66.0
tick_per_revolution = 40.0

ticks_to_mm_const = (math.pi/tick_per_revolution) * wheel_diameter_mm

def ticks_to_mm(ticks):
    return int(ticks_to_mm_const * ticks)

bot = Robot()
stop_at_time = time.time() + 1
logging.basicConfig(level=logging.INFO) 
bot.set_left(90)
bot.set_right(90)

while time.time() < stop_at_time:
    logger.info("Left: {}, Right {}".format(ticks_to_mm(bot.left_encoder.pulse_count),
                                            ticks_to_mm(bot.right_encoder.pulse_count)))
    time.sleep(0.05)