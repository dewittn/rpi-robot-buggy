# A simple script that can be run at startup to test the basic functions of the buggy
# It's useful to make sure all the wires are connected properly
from gpiozero import Robot
from gpiozero.pins.pigpio import PiGPIOFactory
import time

robby = Robot(left=(7,8), right=(9,10))
speed = 0.75
sleep_time = 0.5

def test_forward():
    robby.forward(speed)
    time.sleep(sleep_time)
    robby.stop()

def test_backward():
    robby.backward(speed)
    time.sleep(sleep_time)
    robby.stop()

def test_right():
    robby.right(speed)
    time.sleep(sleep_time)
    robby.stop()
    
def test_left():
    robby.left(speed)
    time.sleep(sleep_time)
    robby.stop()
    
test_forward()
test_backward()
test_right()
test_left()