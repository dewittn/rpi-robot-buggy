# A refactored version of controller_test.py
# May not work with robot buggy
from gpiozero import Button, LED
btn1 = Button(17)
btn2 = Button(22)
btn3 = Button(13)
btn4 = Button(21)
led = LED(18)

def move(direction = ""):
    print('Moving ' + direction)
    led.on()

def stp():
    print('Stop!')
    led.off()

btn1.when_pressed = lambda: move("backward")
btn2.when_pressed = lambda: move("forward")
btn3.when_pressed = lambda: move("right")
btn4.when_pressed = lambda: move("left")

btn1.when_released = stp
btn2.when_released = stp
btn3.when_released = stp
btn4.when_released = stp