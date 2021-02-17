from gpiozero import Robot, Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory

#robot_pins = PiGPIOFactory(host="192.168.1.79")
#robot = Robot(left=(7,8), right=(9,10), pin_factory=robot_pins)

btn1 = Button(17)
btn2 = Button(22)
btn3 = Button(13)
btn4 = Button(21)
led = LED(18)

def fwd():
    print('Go Forward')
    led.on()

def bck():
    print('Go Backward')
    led.on()
    
def lft():
    print('Turn left')
    led.on()

def rgt():
    print('Turn right')
    led.on()

def stp():
    print('Stop!')
    led.off()

btn1.when_pressed = bck
btn2.when_pressed = fwd
btn3.when_pressed = rgt
btn4.when_pressed = lft

btn1.when_released = stp
btn2.when_released = stp
btn3.when_released = stp
btn4.when_released = stp
