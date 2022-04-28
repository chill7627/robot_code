from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM
import atexit

# setting address of the pwm device (servo) same as other I2C devices (motors)
pwm = PWM(0x60)

# this sets the timebase for it all in Hz
pwm_frequency = 100
pwm.setPWMFreq(pwm_frequency)

# positions in servos are set by pulse length
# Mid-point of the servo pulse length in milliseconds
servo_mid_point_ms = 1.5

# What a deflection of 90 degrees is in pulse length in milliseconds
deflect_90_in_ms = 0.95

# length of pulse in chip depends on the frequency pulse (number of steps per cycle)
# 4,096 steps (12 bits) higher frequency needs more steps in the pulse to maintain pulse length, because
# higher frequency = shorter step size
# Frequency is 1 divided by period, but working ms, we can use 1000
period_in_ms = 1000 / pwm_frequency
# The chip has 4096 steps in each period
pulse_steps = 4096
# Steps for every millisecond
steps_per_ms = pulse_steps / period_in_ms
# Steps for a degree
steps_per_degree = (deflect_90_in_ms * steps_per_ms) / 90
# Mid-point of the servo in steps
servo_mid_point_steps = servo_mid_point_ms * steps_per_ms

def convert_degrees_to_steps(position):
    return int(servo_mid_point_steps + (position * steps_per_degree))

atexit.register(pwm.setPWM, 0, 0, 4096)

while True:
    position = int(input("Type your position in degrees (90 to -90, 0 is middle):"))
    end_step = convert_degrees_to_steps(position)
    pwm.setPWM(0, 0, end_step)
