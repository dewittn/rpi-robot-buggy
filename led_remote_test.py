from gpiozero import Robot, Button, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from signal import pause
import time

piozero.Device.pin_factory = PiGPIOFactory(host='192.168.7.96')

factory = PiGPIOFactory(host='192.168.7.59')
led = LED(18, pin_factory=factory)
led.on()
time.sleep(1)
led.off()

factory2 = PiGPIOFactory(host='192.168.7.96')
robby = Robot(left=(7,8), right=(9,10), pin_factory=factory2)
robby.forward()
time.sleep(0.5)
robby.stop()

pause()