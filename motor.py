#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# This will eventually be the backend for a robot car controller.       #
#                                                                       #
#########################################################################
#                                                                       #
#      Michael Tychonievich, Ph.D.                    June, 2018        #
#                                                                       #
#########################################################################

# import sys
import time
import RPi.GPIO as GPIO


# GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
sleeptime = 1


def on(pin_BCM_number):
    GPIO.output(pin_BCM_number, GPIO.HIGH)


def off(pin_BCM_number):
    GPIO.output(pin_BCM_number, GPIO.LOW)


class Motor:
    def __init__(self, forward, reverse, enable):
        self.forward = forward
        self.reverse = reverse
        self.enable = enable
        GPIO.setup(self.forward, GPIO.OUT, initial=0)
        GPIO.setup(self.reverse, GPIO.OUT, initial=0)
        GPIO.setup(self.enable, GPIO.OUT, initial=0)


class Car:
    def __init__(self, right_motor, left_motor):
        self.right = right_motor
        self.left = left_motor

    def enable(self):
        on(self.right.enable)
        on(self.left.enable)

    def duty_change(self, right_duty, left_duty):
        self.right_pulse = GPIO.PWM(self.right.enable, 100)
        self.left_pulse = GPIO.PWM(self.left.enable, 100)
        self.right_pulse.start(right_duty)
        self.left_pulse.start(left_duty)

    def disable(self):
        off(self.right.enable)
        off(self.left.enable)

    def stop(self):
        off(self.right.forward)
        off(self.left.forward)
        off(self.right.reverse)
        off(self.left.reverse)

    def forward(self):
        on(self.right.forward)
        on(self.left.forward)

    def reverse(self):
        on(self.right.reverse)
        on(self.left.reverse)

    def right_in_place(self):
        on(self.right.forward)
        on(self.left.reverse)

    def left_in_place(self):
        on(self.right.reverse)
        on(self.left.forward)


right_motor = Motor(5, 6, 13)
left_motor = Motor(23, 24, 18)
car = Car(right_motor, left_motor)

car.enable()
car.forward()
time.sleep(2)
car.duty_change(5, 5)
time.sleep(2)
car.disable()
car.stop()
GPIO.cleanup()
