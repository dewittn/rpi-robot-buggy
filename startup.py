from gpiozero import Robot
import time

robby = Robot(left=(8,7), right=(9,10))
run_time = 0.4
sleep_time = 1


def test_forward():
    robby.forward(run_time)
    time.sleep(sleep_time)
    robby.stop()

def test_backward():
    robby.backward(run_time)
    time.sleep(sleep_time)
    robby.stop()

def test_right():
    robby.right(run_time)
    time.sleep(sleep_time)
    robby.stop()
    
def test_left():
    robby.left(run_time)
    time.sleep(sleep_time)
    robby.stop()
    
test_forward
test_backward
test_right
test_left