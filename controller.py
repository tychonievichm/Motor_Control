import time
import Adafruit_ADS1x15
import pwm_motor
from gpiozero.pins.pigpio import PiGPIOFactory


car_factory = PiGPIOFactory(host=robot_ip)
adc = Adafruit_ADS1x15.ADS1015()
left = pwm_motor.PWM_Motor(23, 24, 18, pin_factory=car_factory)
right = pwm_motor.PWM_Motor(5, 6, 13, pin_factory=car_factory)


def mainloop():
    gain = 2/3
    normalization = 882
    pot_values = [0]*2
    iteration = 0
    while True:
        for i in range(2):
            pot_values[i] = float(
                adc.read_adc(i, gain=gain)/normalization
                ) - 1
            if pot_values[i] < -1:
                pot_values[i] = -1
            elif pot_values[i] > 1:
                pot_values[i] = 1
            elif pot_values[i] > -0.3 and pot_values[i] < 0.3:
                pot_values[i] = 0
        left.value = pot_values[0]
        right.value = pot_values[1]
        if iteration == 5:
            print(values)
            iteration = 0
        else:
            iteration += 1
        time.sleep(0.15)

# todo: make a way to exit gracefully

mainloop()