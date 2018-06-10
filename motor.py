import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()
print("current GPIO mode: " + str(mode))

GPIO.cleanup()

class motor:
    def __init__(self, forward, backward):
        self.forward = forward
        self.backward = backward
    
right_motor = motor(5,6)
left_motor = motor(13,19)

sleeptime = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(right_motor.forward, GPIO.OUT, initial=0)
GPIO.setup(right_motor.backward, GPIO.OUT, initial=0)
GPIO.setup(left_motor.forward, GPIO.OUT, initial=0)
GPIO.setup(left_motor.backward, GPIO.OUT, initial=0)



def forward(x):
    GPIO.output(right_motor.forward, GPIO.HIGH)
    GPIO.output(left_motor.forward, GPIO.HIGH)
    print("Moving forward")
    time.sleep(x)
    GPIO.output(right_motor.forward, GPIO.LOW)
    GPIO.output(left_motor.forward, GPIO.LOW)
          
def reverse(x):
    GPIO.output(right_motor.backward, GPIO.HIGH)
    GPIO.output(left_motor.backward, GPIO.HIGH)
    print("Moving forward")
    time.sleep(x)
    GPIO.output(right_motor.backward, GPIO.LOW)
    GPIO.output(left_motor.backward, GPIO.LOW)
    
def right_in_place(x):
    GPIO.output(right_motor.forward, GPIO.HIGH)
    GPIO.output(left_motor.backward, GPIO.HIGH)
    print("Moving forward")
    time.sleep(x)
    GPIO.output(right_motor.forward, GPIO.LOW)
    GPIO.output(left_motor.backward, GPIO.LOW)

def left_in_place(x):
    GPIO.output(right_motor.backward, GPIO.HIGH)
    GPIO.output(left_motor.forward, GPIO.HIGH)
    print("Moving forward")
    time.sleep(x)
    GPIO.output(right_motor.backward, GPIO.LOW)
    GPIO.output(left_motor.forward, GPIO.LOW)

#right_in_place(.3)
#left_in_place(.1)
#forward(.5)
reverse(2)
GPIO.cleanup()