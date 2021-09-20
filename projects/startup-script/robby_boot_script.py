#! /usr/bin/env python3
# Code to run the buggy from a remote Pi using a home-brew game controller.
# https://projects.raspberrypi.org/en/projects/remote-control-buggy/4
from gpiozero import Robot, Button, LED, Device
from evdev import InputDevice, categorize, ecodes 
from signal import pause
import RPi.GPIO as GPIO
import time

## Robot Variables
front_wheels = Robot(left=(9,10), right=(7,8))
back_wheels = Robot(left=(21,20), right=(13,6))
front_wheels.stop()
back_wheels.stop()

## Testing Variables
testing_speed = 1
testing_time = 2

def fwd(speed = 1):
  print('Go Forward')
  front_wheels.forward(speed)
  back_wheels.forward(speed)
  #led.on()

def bck(speed = 1):
  print('Go Backward')
  front_wheels.backward(speed)
  back_wheels.backward(speed)
  
def lft(speed = 1):
  print('Turn left')
  front_wheels.right()
  back_wheels.left()

def rgt(speed = 1):
  print('Turn right')
  front_wheels.left()
  back_wheels.right()

def stp():
  print('Stop!')
  front_wheels.stop()
  back_wheels.stop()

## Functions to test wheels on boot
def test_forward():
    print("Test Forward!")
    fwd(testing_speed)
    time.sleep(testing_time)
    stp()
    
def test_backward():
    print("Test Backward!")
    bck(testing_speed)
    time.sleep(testing_time)
    stp()

def test_right():
    print("Test Right!")
    rgt(testing_speed)
    time.sleep(testing_time)
    stp()
    
def test_left():
    print("Test Left!")
    lft(testing_speed)
    time.sleep(testing_time)
    stp()

## Call Testing Functions
test_forward()
test_backward()
test_right()
test_left()


  
## Setup GamePad
for i in range(5):
  if InputDevice('/dev/input/event' + i).name = "Logitech Gamepad F310":
    gamepad = InputDevice('/dev/input/event'+ i)
i = 0
while i < 6
  gamepad = InputDevice('/dev/input/event'+ i)
  if gamepad.name = "Logitech Gamepad F310":
    break
else:
  print("ERROR: Game pad cannot be found!")
  quit()

button_commands = {
  304 : bck, # btn_a
  305 : rgt, # btn_b
  308 : fwd, # btn_y
  307 : lft, # btn_x
  #17 : fwd, # pad_up
  #17 : bck, # pad_down
  #16 : rgt, # pad_right
  #17 : lft, # pad_left
  310 : lft, # btn_tl
  311 : rgt, # btn_tr
  5   : fwd, # abs_rz
  2   : bck, # abs_z
}

print('Robot Ready!')
print('Using: ' + gamepad.name)

try:
    for event in gamepad.read_loop():
        print(event)
        if event.type == ecodes.EV_KEY: 
            if event.value == 1: 
              button_commands.get(event.code)()
            else: 
              stp()
        if event.type == ecodes.EV_ABS: 
            if event.value >= 1:
              speed = event.value/255
              command = button_commands.get(event.code)
              if command:
                command(speed)
            else:
              stp()

except KeyboardInterrupt:
    print("Stopping Robot...")

except:
    print("Oh no, something went wrong!\nStopping Robot...")
    
finally:
    print("Goodbye!")
    GPIO.cleanup()