#You can write, load, or paste Micropython programs here
#Tap "send program" to send it to the device

#This program puts the system in an low power "idle" mode, after running this program you will need to use the board's reset button to reboot it
import machine
p14=machine.Pin(14)
p14.init(p14.IN,p14.PULL_DOWN)
machine.deepsleep(90000000)