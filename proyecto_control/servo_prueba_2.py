from gpiozero import AngularServo
import time
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()

servo1 = AngularServo(18, pin_factory=factory,min_angle=-90,max_angle=90, min_pulse_width=0.0005,max_pulse_width=0.0025)

while True:
    servo1.angle=60
    time.sleep(0.2)
    servo1.angle=-60
    time.sleep(0.2)
    

   


