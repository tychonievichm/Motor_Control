#!/usr/bin/env python.
# -*- coding: utf-8 -*-

#########################################################################
#                                                                       #
# This will eventually be the tkinter gui for a robot car controller.   #
#                                                                       #
#########################################################################
#                                                                       #
#      Michael Tychonievich, Ph.D.                    June, 2018        #
#                                                                       #
#########################################################################

# import motor
import fake_motor as motor
import Tkinter as tk

import time

'''
Commands for changing the state of the car's motors:
enable(right_duty=None, left_duty=None)
set_speed(right_duty=None, left_duty=None)
disable()

stop()
stall()

forward(right_duty=None, left_duty=None)
reverse(right_duty=None, left_duty=None)
spin_right(right_duty=None, left_duty=None)
spin_left(right_duty=None, left_duty=None)
'''


class CarGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.car = motor.Car(motor.Motor(5, 6, 13), motor.Motor(23, 24, 18))
        self.pack(side=tk.LEFT)
        self.pin_frame_left = PinFrame(self, self.car.left)
        self.slider_frame_left = SliderFrame(self, self.car.left)
        self.buffer_frame = BufferFrame(self, 1, 100, tk.LEFT)
        self.slider_frame_right = SliderFrame(self, self.car.right)
        self.pin_frame_right = PinFrame(self, self.car.right)


class BufferFrame(tk.Frame):
    """Empty frame for spacing purposes."""
    def __init__(self, parent, ht, wd, sd):
        tk.Frame.__init__(self, parent, height=ht, width=wd)
        self.pack(side=sd, expand=False)


class PinFrame(tk.Frame):
    def __init__(self, parent, motor):
        tk.Frame.__init__(self, parent)
        self.motor = motor
        self.pack(side=tk.LEFT)
        self.forward_signal = tk.Frame(self, parent, height=100,
                                       width=100, relief=tk.RAISED)
        self.forward_signal.pack(side=tk.TOP)
        self.buffer_frame = BufferFrame(self, 100, 100, tk.TOP)
        self.backward_signal = tk.Frame(self, parent, height=100,
                                        width=100, relief=tk.RAISED)
        self.backward_signal.pack(side=tk.TOP)


    def update(self):
        pass


class SliderFrame(tk.Frame):
    def __init__(self, parent, motor):
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, expand=False)
        self.slider = tk.Scale(self, from_=100, to=-100, orient=tk.VERTICAL,
                               length=300)
        self.slider.pack(side=tk.LEFT)







root = tk.Tk()
root.title("Car Simulator")
app = CarGUI(root)
root.mainloop()
