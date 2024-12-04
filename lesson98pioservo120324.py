##############################################################
# SG90 servo PIO State machine lesson98pioservo120324.py     #
# state machine frequency = 2_000_000 hz = 0.5µs/instruction #   
# servo period = 50hz = 20_000 µs                            #
# servo control pin = Pin(0)                                 #
# X register: servo_pulse_width counter                      #
# Y register: servo period counter                           #
# import user defined servo state machine class library      #
#                                                            #
# ->|                               |<-  period = 20_000 µs  #
#                                                            #
#___|****|__________________________|***|________            #
#                                                            #
# ->|    |<- pulse width = 700->2_500 µs = 0->180 degrees    #
##############################################################

from machine import Pin 
from rp2 import asm_pio, PIO, StateMachine
from time import sleep
from sg_90_servo_PIO import ServoSM                                  # servo state machine lib

servo_signal_pin = Pin(0, Pin.OUT)                                   # first servo signal gpio pin
sm0 = ServoSM(2_000_000, 700, 2_500, servo_signal_pin, 20_000)       # SM for first servo
servo_signal_pin = Pin(1, Pin.OUT)                                   # second servo signal gpio pin
sm1 = ServoSM(2_000_000, 700, 2_500, servo_signal_pin, 20_000)       # SM for second servo
sm0.servo_angle(45)                                                  # first servo 45°
sm1.servo_angle(135)                                                 # second servo 135°
sleep(2)
for i in range(0, 180, 5):                                           # run 2 servos in 2 state machines
    sm0.servo_angle(i)
    sm1.servo_angle(180 - i)
    sleep(0.2)
for i in reversed(range(0, 180, 5)):
    sm0.servo_angle(i)
    sm1.servo_angle(180 - i)
    sleep(0.2)
sm0.servo_angle(90)                                                  # set servos back to 90°
sm1.servo_angle(90)
