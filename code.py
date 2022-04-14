# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Circuit Playground HID Keyboard

import time

import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from digitalio import DigitalInOut, Direction, Pull

import neopixel

# A simple neat keyboard demo in CircuitPython

# The button pins we'll use, each will have an internal pulldown
buttonpins = [board.BUTTON_A, board.BUTTON_B]
# our array of button objects
buttons = []
# The keycode sent for each button, will be paired with a control key
#buttonkeys = [Keycode.J, "Hello World!\n"]
controlkey = Keycode.SHIFT

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

# the keyboard object!
# sleep for a bit to avoid a race condition on some systems
time.sleep(1)
kbd = Keyboard(usb_hid.devices)
# we're americans :)
layout = KeyboardLayoutUS(kbd)

# make all pin objects, make them inputs with pulldowns
for pin in buttonpins:
    button = DigitalInOut(pin)
    button.direction = Direction.INPUT
    button.pull = Pull.DOWN
    buttons.append(button)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

#Neo pixel colors
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)


print("Waiting for button presses")

while True:
    # check each button
    # when pressed, the LED will light up,
    # when released, the keycode or string will be sent
    # this prevents rapid-fire repeats!
    for button in buttons:
        if button.value:  # pressed?
            i = buttons.index(button)
            print("Button #%d Pressed" % i)

            # turn on the LED
            led.value = True

            # turn neopixel on for test
            pixels[2] = OFF
            pixels[7] = OFF
            pixels.show()

        while button.value:
            pass  # wait for it to be released!

            # type the keycode or string
            #k = buttonkeys[i]  # get the corresponding keycode or string
            if i == 0:
                pixels[2] = RED
                pixels.show()
                kbd.press(Keycode.CONTROL, Keycode.COMMAND, Keycode.Q)
                time.sleep(3)
                pixels[2] = OFF
                pixels.show()
                kbd.release_all()

            elif i == 1:
                pixels[7] = GREEN
                pixels.show()
                kbd.release_all()
                print("Released Keys - Nothing to see here")
                time.sleep(1)
                pixels[2] = OFF
                pixels[7] = OFF
                pixels.show()
            #if isinstance(k, str):
            #    layout.write(k)
            else:
                kbd.release_all()  # release!


            # turn off the LED
            led.value = False

    time.sleep(0.01)
