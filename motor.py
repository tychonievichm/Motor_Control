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


GPIO.cleanup()
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

    def disable(self):
        off(self.right.enable)
        off(self.left.enable)

    def forward(self, do_time):
        on(self.right.forward)
        on(self.left.forward)
        print("Moving forward.")
        time.sleep(do_time)
        off(self.right.forward)
        off(self.left.forward)

    def reverse(self, do_time):
        on(self.right.reverse)
        on(self.left.reverse)
        print("Reversing.")
        time.sleep(do_time)
        off(self.right.reverse)
        off(self.left.reverse)

    def right_in_place(self, do_time):
        on(self.right.forward)
        on(self.left.reverse)
        print("Spinning clockwise.")
        time.sleep(do_time)
        off(self.right.forward)
        off(self.left.reverse)

    def left_in_place(self, do_time):
        on(self.right.reverse)
        on(self.left.forward)
        print("Spinning counter-clockwise.")
        time.sleep(do_time)
        off(self.right.reverse)
        off(self.left.forward)


right_motor = Motor(5, 6, 13)
left_motor = Motor(18, 23, 24)
car = Car(right_motor, left_motor)
car.enable()

# right_in_place(.3)
# left_in_place(.1)
# forward(.5)
car.reverse(2)
car.disable()
GPIO.cleanup()
