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

import motor
#import fake_motor as motor
import tkinter as tk


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
        self.car.enable(0, 0)

    def update(self):
        self.pin_frame_left.update()
        self.pin_frame_right.update()


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
        self.forward_signal = tk.Frame(self, parent, height=50,
                                       width=50, relief=tk.RAISED)
        self.forward_signal.pack(side=tk.TOP)
        self.buffer_frame = BufferFrame(self, 100, 100, tk.TOP)
        self.reverse_signal = tk.Frame(self, parent, height=50,
                                       width=50, relief=tk.RAISED)
        self.reverse_signal.pack(side=tk.TOP)
        self.update()

    def update(self):
        if self.motor.forward_pin.state == "on":
            self.forward_signal.config(background="green")
        elif self.motor.forward_pin.state == "off":
            self.forward_signal.config(background="red")
        else:
            self.forward_signal.config(background="white")
        if self.motor.reverse_pin.state == "on":
            self.reverse_signal.config(background="green")
        elif self.motor.reverse_pin.state == "off":
            self.reverse_signal.config(background="red")
        else:
            self.reverse_signal.config(background="white")


class SliderFrame(tk.Frame):
    def __init__(self, parent, motor):
        self.motor = motor
        tk.Frame.__init__(self, parent)
        self.pack(side=tk.LEFT, expand=False)
        self.slider = tk.Scale(self, from_=100, to=-100, orient=tk.VERTICAL,
                               length=300, resolution=5,
                               command=lambda value:
                                   self.scale_move(float(value)))
        self.slider.pack(side=tk.LEFT)

    def scale_move(self, x):
        if x > 15:
            self.motor.forward(x)
        elif x < -15:
            self.motor.reverse(-x)
        elif abs(x) < 5:
            self.motor.stop()
        else:
            self.motor.stall()
        app.update()


root = tk.Tk()
root.title("Car Simulator")
app = CarGUI(root)
root.mainloop()
