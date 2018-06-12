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
import pigpio

pi = pigpio.pi

if not pi.connected:
    exit()



def on(pin_BCM_number):
    pi.write(pin_BCM_number, 1)


def off(pin_BCM_number):
    pi.write(pin_BCM_number, 0)


def pwm(pin_BCM_number, percent_duty):
    pi.set_PWM_dutycycle(pin_BCM_number, percent_duty)


class Motor:
    def __init__(self, pi, forward, reverse, enable):
        self.pi = pi
        self.forward = forward
        self.reverse = reverse
        self.enable = enable
        self.pi.set_mode(forward, pigpio.OUTPUT)
        self.pi.set_mode(reverse, pigpio.OUTPUT)
        self.pi.set_mode(enable, pigpio.OUTPUT)
        pi.set_PWM_frequency(self.enable, 320)
        pi.set_PWM_range(self.enable, 100)

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

# right_in_place(.3)
# left_in_place(.1)
# forward(.5)
car.reverse()
time.sleep(2)
car.disable()
car.stop()

pi.stop()