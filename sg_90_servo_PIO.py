#############################################################################################################################
#  SG_90 servo State Machine class library                                                                                  #
#  sg_90_servo_PIO.py    12/04/24  Lesson 98                                                                                #                                                                                         #
#  class ServoSM  instantiates an sg-90 servo as a state machine                                                            #
#############################################################################################################################

from machine import Pin 
from rp2 import asm_pio, PIO, StateMachine


@asm_pio(sideset_init = PIO.OUT_LOW)
def servo_pio():
    pull(noblock)                  # servo pulse width (µs), use X if no new pulse width to pull()
    mov(x,osr)                     # servo pulse width (µs) in X
    mov(y, isr)  .side(0)          # servo period (µs) already preloaded in isr -> Y; start with signal pin low
    label('loop')                  # count down from period (µs) in Y register
    jmp(x_not_y, 'nxt')            # check if servo pulse width counter needs starting
    nop() .side(1)                 # start servo pulse
    label('nxt')
    jmp(y_dec, 'loop')             # decrement period  until servo period complete; 2 instructions per loop = 1_µs/loop

class ServoSM:
    ''' smID: class variable, incremented in __init__() without user input for each state machine instantiation
        up to 4 state machine on each of the two different PIO blocks
    '''
    smID = -1                      # class variable; state machine ID automatically incremented in __init__()
    def __init__(self, sm_freq, servo_pulse_width_min_µs, servo_pulse_width_max_µs, servo_signal_pin, servo_period_µs):
        ServoSM.smID += 1          # keep track of state machine ID  without user input.  (0->3 : sm0, sm1, sm2, sm3 possible)
        self.servo_period_µs = servo_period_µs
        self.servo_pulse_width_min_µs = servo_pulse_width_min_µs
        self.servo_pulse_width_max_µs = servo_pulse_width_max_µs
        self._sm = StateMachine(ServoSM.smID, servo_pio, sm_freq, sideset_base = servo_signal_pin)
        self._sm.put(self.servo_period_µs)    # preload servo period (µs) into isr
        self._sm.exec("pull()")
        self._sm.exec("mov(isr,osr)")
        self._sm.active(1)
        
    def servo_angle(self, angle):
        '''
            y = m * x  + b;   use two points for a line  to calc µs for a given servo angle in degrees
            P1 = (x1,y1) = (0 deg, servo_pulse_width_min_µs);  P2 = (x2, y2) = (180 deg, servo_pulse_width_max_µs)
        '''
        m = (self.servo_pulse_width_max_µs - self.servo_pulse_width_min_µs) / 180  # m = (2_500-700)/180 = 10
        y = m * angle + self.servo_pulse_width_min_µs                              # µs needed for given servo angle degree
        self._sm.put( int( y) )
        
def main():                                                             # test ServoSM functionality
    servo_signal_pin = Pin(0, Pin.OUT)                                  # gpio signal pin for servo
    sm = ServoSM(2_000_000, 700, 2_500, servo_signal_pin, 20_000)       # SM for servo
    sm.servo_angle(45)                                                  # move servo to 45°
    
if __name__ == '__main__':                                              # run if stand alone code
    main()
