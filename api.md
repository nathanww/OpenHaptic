# OpenHaptic API
There are a few functions included with OpenHaptic to simplify building applications. Using the API is not required; you can also write Micropython code that accsesses all the ardware directly.

# Vibration functions

**vibePattern(intensity, timing, loop=0)**
Executes a vibration pattern on the three vibration motors

Vibration pattern are defined by two lists, one listig the vibration intensity(0-100 and the other vibration duration(in seconds). Each pattern can consist of multiple segments with different intensities. For example, the pattern
intensity=[0,100,0,100]
timing=[0.5,0.5,0.5,0.5]
Pulses the motor on once a second

This function 
