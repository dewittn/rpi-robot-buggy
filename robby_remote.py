# Code to run the buggy from a remote Pi using a home-brew game controller.
# https://projects.raspberrypi.org/en/projects/remote-control-buggy/4
from gpiozero import Robot, Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import time

# There is a bug in GPIOZero 1.5.1 that prevents pin_factory from working with Robot and Motor
# This code does not work!
# factory = PiGPIOFactory(host='192.168.1.17')
# robot = Robot(left=(4, 14), right=(17, 18), pin_factory=factory)  # remote pins

# To address this bug we set the global pin factory to the remote host
# and connect to the breadboard controller through a localhost pin_factory.
import gpiozero
gpiozero.Device.pin_factory = PiGPIOFactory(host='192.168.7.96')

robot = Robot(left=(7,8), right=(9,10))
robot.stop()

local_pins = PiGPIOFactory(host="localhost")
btn1 = Button(17, pin_factory=local_pins)
btn2 = Button(22, pin_factory=local_pins)
btn3 = Button(13, pin_factory=local_pins)
btn4 = Button(21, pin_factory=local_pins)
led = LED(18, pin_factory=local_pins)


def fwd():
    print('Go Forward')
    robot.forward()
    led.on()

def bck():
    print('Go Backward')
    robot.backward()
    led.on()
    
def lft():
    print('Turn left')
    robot.left()
    led.on()

def rgt():
    print('Turn right')
    robot.right()
    led.on()

def stp():
    print('Stop!')
    robot.stop()
    led.off()

btn1.when_pressed = bck
btn2.when_pressed = fwd
btn3.when_pressed = lft
btn4.when_pressed = rgt

btn1.when_released = stp
btn2.when_released = stp
btn3.when_released = stp
btn4.when_released = stp

pause()
