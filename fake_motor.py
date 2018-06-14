#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# This is a simulator for the motor.py module for coding while away     #
# from the robot.                                                       #
#                                                                       #
#########################################################################
#                                                                       #
#      Michael Tychonievich, Ph.D.                    June, 2018        #
#                                                                       #
#########################################################################

# import sys
import time

sleeptime = 1

# This block of code sets up an API for GPIO pins, to isolate calls to
# RPi.GPIO in case I need to change from RPi.GPIO to a different GPIO
# package.  This might be needed if the streaming video causes the
# software pwm to lag.

class Pin:
    def __init__(self, pin_BCM_number):
        self.number = pin_BCM_number
        self.is_out = None
        self.state = "off"

    def on(self):
        self.state = "on"

    def off(self):
         self.state = "off"

    def out(self):
        self.is_out = True


class PWM(Pin):
    def __init__(self, pin_BCM_number, duty=None):
        Pin.__init__(self, pin_BCM_number)
        if duty != None:
            self.duty = duty
        else:
            self.duty = 25
        self.duty = duty
        self.state = "on"

    def stop(self):
        self.state = "off"
        self.duty = 0

    def start(self, duty=None):
        if duty != None:
            self.duty = duty
        self.state = "on"
        self.duty = duty

    def change_duty(self, duty=None):
        if duty != None:
            self.duty = duty
        self.duty = duty


class Motor:
    """This is the class to handle the motors of the car.  The motor 
    controller I use forces me to group motors together, and I did
    so by the side of the car they were on, like tank treads.
    """
    def __init__(self, forward_pin, reverse_pin, enable_pin):
        """Establish control over the named GPIO pins.  The enable pin
        is set as a pwm to allow for speed control.
        """
        self.forward_pin = Pin(forward_pin)
        self.reverse_pin = Pin(reverse_pin)
        self.pwm = PWM(enable_pin)
        self.forward_pin.out()
        self.reverse_pin.out()
        self.pwm.out()
        self.speed = self.pwm.duty

    def enable(self, duty=None):
        """This only starts up the enable pin for the motor.  The motor
        will not turn until told to go either forward or backward.
        """
        if duty != None:
            self.speed = duty
        self.pwm.start(self.speed)

    def set_speed(self, duty=None):
        """This changes the duty cycle of the pwm without stopping it."""
        if duty != None:
            self.speed = duty
        self.pwm.change_duty(self.speed)

    def disable(self):
        """Turns off the enable pin entirely.  This should cause the
        motor to stop turning, but to not resist being turned."""
        self.pwm.stop()

    def stop(self):
        """Causes the motor to stop turning, and causes it to resist
        being turned if the pwm is on.  The level of resistance should
        correlate to the duty of the pwm, so faster motors will brake
        harder.
        """
        self.forward_pin.off()
        self.reverse_pin.off()

    def stall(self):
        """Causes the motor to stop turning without resisting being
        turned.
        """
        self.forward_pin.on()
        self.reverse_pin.on()

    def forward(self, duty=None):
        """Causes the motor to spin in a way that makes its wheels move
        the car forward.
        """
        self.forward_pin.on()
        self.reverse_pin.off()
        if duty != None:
            self.speed = duty
        self.set_speed(self.speed)

    def reverse(self, duty=None):
        """Causes the motor to spin in a way that makes its wheels move
        the car backward.
        """
        self.reverse_pin.on()
        self.forward_pin.off()
        if duty != None:
            self.speed = duty
        self.set_speed(self.speed)


class Car:
    """This class groups together two motors to allow more intuitive
    simultaneous control.  Its methods consist of a command to the right
    side of the car and a command to the left side of the car.  This will 
    be the class which the interface programs use to control the car.
    """
    def __init__(self, right_motor, left_motor):
        self.right = right_motor
        self.left = left_motor

    def enable(self, right_duty=None, left_duty=None):
        self.right.enable(right_duty)
        self.left.enable(left_duty)

    def set_speed(self, right_duty=None, left_duty=None):
        self.right.change_speed(right_duty)
        self.left.change_speed(left_duty)

    def disable(self):
        self.right.disable()
        self.left.disable()

    def stop(self):
        self.right.stop()
        self.left.stop()

    def stall(self):
        self.right.stall()
        self.left.stall()

    def forward(self, right_duty=None, left_duty=None):
        self.right.forward(right_duty)
        self.left.forward(left_duty)

    def reverse(self, right_duty=None, left_duty=None):
        self.right.reverse(right_duty)
        self.left.reverse(left_duty)

    def spin_right(self, right_duty=None, left_duty=None):
        self.right.reverse(right_duty)
        self.left.forward(left_duty)

    def spin_left(self, right_duty=None, left_duty=None):
        self.right.forward(right_duty)
        self.left.reverse(left_duty)


# right_motor = Motor(5, 6, 13)
# left_motor = Motor(23, 24, 18)

# Here is a test script to make sure that the programming works as
# expected.  I will move this to another file later.

car = Car(Motor(5, 6, 13), Motor(23, 24, 18))

car.enable(100, 100)
car.forward(25, 25)
time.sleep(2)
car.set_speed(100, 50)
time.sleep(2)
car.disable()
car.stop()
