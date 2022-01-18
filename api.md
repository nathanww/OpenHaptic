# OpenHaptic API
There are a few functions included with OpenHaptic to simplify building applications. Using the API is not required; you can also write Micropython code that accsesses all the ardware directly.

# Vibration functions

**vibePattern(intensity, timing, loop=0,pwmFreq=1000)**

Executes a vibration pattern on the three vibration motors

Vibration pattern are defined by two lists, one listig the vibration intensity(0-100 and the other vibration duration(in seconds). Each pattern can consist of multiple segments with different intensities. For example, the pattern
intensity=[0,100,0,100]
timing=[0.5,0.5,0.5,0.5] pulses the motor on once a second

*Arguments*

intensity--a list of three lists, each of which contains the intensity sequence for one motor

timing--a list containing the duration of each segment. The same timing is used for all motors.

loop--the number of times to loop the sequence

pwmFreq--frequency of the PWM drivers. The default (1000) is almost always good, but can be adjusted


**[intensity,timing]=waveSynth(freq,power,duration=1,waveform="sine",lowcut=0,highcut=100,stepSize=0.01,phaseOffset=[0,0,0])**

Generates intensity and timing lists to produce a specified waveform. This function generates three waves at once (one for each motor)

*Arguments*

freq--List of 3 frequencies in Hertz, corresponding to motors 1-3

power--List of three peak intensities, from 0 to 100, corresponding to motors 1-3

duration--duration in seconds

waveform--either "sine" or "square"

lowcut--minimum intensity for any point

highcut--maximum intensity for any point

stepSize--how long does each time point last in seconds. This can be adjusted to trade off resolution and memory use

phaseOffset--Lets you shift the phase of the wave. By default, waves are generated as wave=sine(x) from x=0 to x=6.28. However, you can override this by setting this variable for each motor--for instance if a motor's phase offset is set to 1, the wave will be generated from points 1 to 7.28.


*Outputs*

intensity--intensity list for in the format used by vibePattern. This is alist of three lists, each one of which contains the sequence for a particular motor.

timing--timing list in the format used by vibepattern

**wave=combineWaves(wave1,wave2,weight=1.0)**

Creates a composite wave by blending two seperate waveforms. This function deals with intensity lists in vibePattern format

*Arguments*

wave1--intensity list of all the segments for the first wave

wave2--intensity list of all the segments for the second

weight--relative weights of the first and second wave. Values greater than 1 weight the second wave more highly, values less than 1 weight the first wave more highly.


*Outputs*

wave--the intensity list for the combined wave.

**wave=modulate(wave1,wave2)**

Uses wave 2 to scale wave 1. the resulting wave at time x is wave1[x]\*(wave2[x]/100)

*Arguments*

wave1--intensity list of all the segments for the first wave

wave2--intensity list of all the segments for the second

*Outputs*

wave--the intensity list for the resulting wave.


# Communication protocol
OpenHaptic uses the Nordic UART BLE service for loading programs.  The OpenHaptic Programmer app also uses this service to create an interactive shell for users to interact with the devide. Alterantively, the connection can be used to send data between a app running on OpenHaptic and a companion device. Programs can also accsess the Bluetooth/wifi hardware directly for other types of connections.

*Using the OpenHaptic shell (easiest method)*

First, check that a connection exists by checking that **ble.isConnected** is true.

If it is, you can send data to be displayed to the user by calling

**ble.send(data)**

Where data is an UTF-8 string to be displayed in the OpenHaptic Programmer application

Data received from the shell is stored as a string in the **lastData** variable. Another variable, **lastDataTime**, keeps the time.time() timestamp of when the last data transmission ended.


*Connecting your own apps*
If you want to send data without using the shell, your app must first make a BLE GATT connection to the OpenHaptic device

Device name: OpenHaptic

Service UUID: '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'

OpenHaptic's "receive" GATT attribute: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E

OpenHaptic's "transmit" attribute: 6E400003-B5A3-F393-E0A9-E50E24DCCA9E



*Message formats*
To send a message to the device, write it to the GATT receive attribute. The message should be an UTF-8 string ending in "ENDMSG"

Messages sent by OpenHaptic are also strings terminated with "ENDMSG". 

The Openhaptic device attempts to send status messages when connected: These are prefaced by "ST:" and consist of the current battery voltage, a comma, and the current program status (0=not running program, 1=running program)

Messages prefaced with "PROG:" are commands to overwrite the current program with the data that comes afterwards.


