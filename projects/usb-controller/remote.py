# Code to run the buggy from a remote Pi using a home-brew game controller.
# https://projects.raspberrypi.org/en/projects/remote-control-buggy/4
# https://core-electronics.com.au/tutorials/using-usb-and-bluetooth-controllers-with-python.html
from gpiozero import Robot, Button, LED, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO 
from signal import pause
import time

# There is a bug in GPIOZero 1.5.1 that prevents pin_factory from working with Robot and Motor
# For example, this code does not work!
#factory = PiGPIOFactory(host='192.168.1.17')
#robot = Robot(left=(4, 14), right=(17, 18), pin_factory=factory)  # remote pins
#robot.stop()

# To address this bug we set the global pin factory to the remote host
# and connect to the breadboard controller through a localhost pin_factory.
#Device.pin_factory = PiGPIOFactory(host='localhost')
front_wheels = Robot(left=(9,10), right=(7,8))
back_wheels = Robot(left=(21,20), right=(13,6))
front_wheels.stop()
back_wheels.stop()

## Breadboard Controller
#local_pins = PiGPIOFactory(host="localhost")
#led = LED(18, pin_factory=local_pins)

def fwd(speed = 1):
  print('Go Forward')
  front_wheels.forward(speed)
  back_wheels.forward(speed)
  #led.on()

def bck(speed = 1):
  print('Go Backward')
  front_wheels.backward(speed)
  back_wheels.backward(speed)
  #led.on()
  
def lft(speed = 1):
  print('Turn left')
  front_wheels.right()
  back_wheels.left()
  #led.on()

def rgt(speed = 1):
  print('Turn right')
  front_wheels.left()
  back_wheels.right()
  #led.on()

def stp():
  print('Stop!')
  front_wheels.stop()
  back_wheels.stop()
  #led.off()

gamepad = InputDevice('/dev/input/event0')

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
              button_commands.get(event.code)(speed)
            else: 
              stp()

except KeyboardInterrupt:
    print("Stopping Robot...")

except:
    print("Oh no, something went wrong!\nStopping Robot...")
    
finally:
    print("Goodbye!")
    GPIO.cleanup()