# OpenHaptic
 Welcome! OpenHaptic is a system for interfacing with the sense of touch in rich ways.
Some things you can do with OpenHaptic:
* Build [Sensory augmentation](https://en.wikipedia.org/wiki/Sensory_substitution) systems that let you sense radar signals, infrared, ultrasound, etc
* Use vibratory stimuli to [control the autonomic nervous system](https://www.healio.com/news/rheumatology/20190417/vibration-stimulation-of-external-ear-alleviates-inflammation-in-ra)
* Build an unintrusive notification systems
* Provide biofeedback/neurofeedback
* Make haptic interfaces for AR, VR, and video games

# Hardware build
The OpenHaptic hardware consists of a [ESP32 Feather](https://www.adafruit.com/product/3405) connected to 3 vibration motors and a battery. The parts used in my build were:

The specific part numbers we used were:
* [1 ESP32 Feather](https://www.adafruit.com/product/3405)
* [3 DZS electric vibration motors](https://www.amazon.com/gp/product/B07PHRX7QH)
* [3 Fairchild 2N7000 MOSFETS](https://www.amazon.com/gp/product/B07PHRX7QH)
* [1 Adafruit 400mAh lipo battery](https://www.adafruit.com/product/3898) *

Assembly is fairly simple; each MOSFET is used to drive a motor (make sure that the MOSFET is placed in the low side of the motor, the current path should be battery -> motor -> MOSFET source -> MOSFET drain -> ground). The battery is plugged into the Feather's battery terminals; an onboard circuit will automatically control charging and discharging

*400 mAh is probably a good minimum, this battery is also sold in larger sizes and if you anticipate using it heavily (3+ hours of continuous vibration or wireless communication between charges) a larger battery may be useful.

![Circuit schematic](https://raw.githubusercontent.com/nathanww/OpenHaptic/main/schematic.png)
# Software installation

1. Install MicroPython on your ESP32 feather, as shown [here](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)
2. Download the main.py file and use [Thonny](https://thonny.org/) to save it on the Feather board.

All of the critical software is now installed, but your OpenHaptic won't do anything until you load an app on it. The easiest way to do that is using our [Android app](https://play.google.com/store/apps/details?id=appinventor.ai_nathanwhitmore2020.hapticProgrammer) which will let you load Python code on the board. A few demo programs are included with the Android app for you to load.

Once code is loaded, it will run immediately, and every time the board starts up it will wait 30 seconds and then run the last loaded program
# Use
The Openhaptic Programmer app will you you install and remove programs and communicate with the device.

You can also toggle programs on and off by pressing the reset button on the board itself. Each time you press it the board will switch between "program running" and "idle" states
# Programming
The OpenHaptic board will run any Micropython program you load on it; you can do anything one could do in micropython. There are also some convenience functions that simplify building apps, see [here](https://github.com/nathanww/OpenHaptic/blob/main/api.md) for details

# Communicating with other devices
The ESP32 device has a Bluetooth/Wifi radio, and OpenHaptic [includes some APIs](https://github.com/nathanww/OpenHaptic/blob/main/api.md) for communicating with another device over Bluetooth. 
It is also entirely possible to ignore the API and just use custom Micropython code for communication.



