# -*- coding: utf-8 -*-

"""This is code modified from the gpiozero source to work better with the particular
H-bridge I used in my car.

Copyright 2015- Raspberry Pi Foundation

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""

import gpiozero as gz

class PWM_Motor(gz.SourceMixin, gz.CompositeDevice):
    '''A new gpiozero-style motor object.'''
    def __init__(self, forward=None, backward=None, enable=None, pin_factory=None):
        if not all(p is not None for p in [forward, backward, enable]):
            raise gz.GPIOPinMissing(
                'forward and backward pins must be provided.'
                )
        super(PWM_Motor, self).__init__(
                forward_device=gz.OutputDevice(forward, pin_factory=pin_factory),
                backward_device=gz.OutputDevice(backward, pin_factory=pin_factory),
                enable_device=gz.PWMOutputDevice(enable, pin_factory=pin_factory),
                _order=('forward_device', 'backward_device', 'enable_device'),
                pin_factory=pin_factory
                )

    @property
    def value(self):
        '''Represents the speed of the motor as a floating point value between -1
        (full speed backward) and 1 (full speed forward), with 0 representing
        stopped.
        '''
        speed = self.enable_device.value
        if self.forward_device.value == self.backward_device.value:
            return 0
        elif self.forward_device.value is True:
            return self.enable_device.value
        elif self.backward_device.value is True:
            return -self.enable_device.value

    @value.setter
    def value(self, value):
        '''Ensures that changing the motor value field also changes the rate of
        the pwm.'''
        if not -1 <= value <= 1:
            raise gz.OutputDeviceBadValue("Motor value must be between -1 and 1.")
        if -1 <= value <= 1:
            try:
                if value > 0:
                    self.forward(value)
                elif value < 0:
                    self.backward(-value)
                elif value == 0:
                    self.stop()
            except ValueError as e:
                raise gz.OutputDeviceBadValue(e)
        else:
            self.stop()

    @property
    def is_active(self):
        '''Not used, but kept for adherence to gpiozer format.'''
        return self.value != 0

    def forward(self, speed=1):
        '''Instruct the motor to turn "forward".'''
        if not 0 <= speed <= 1:
            raise ValueError('Forward speed must be between 0 and 1')
        self.backward_device.off()
        self.forward_device.on()
        self.enable_device.value = speed

    def backward(self, speed=1):
        '''Instruct the motor to turn "backward".'''
        if not 0 <= speed <= 1:
            raise ValueError('Backward speed must be between 0 and 1')
        self.forward_device.off()
        self.backward_device.on()
        self.enable_device.value = speed

    def stop(self):
        '''Motor stops, resisting movement.'''
        self.forward_device.off()
        self.backward_device.off()
