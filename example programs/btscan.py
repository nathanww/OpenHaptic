# This program converts Bluetooth beacons into tactile sequences
#Code based on the tutorial at https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_simple_central.py
# NOTICE: You will need to press the reset button on the board to switch from this to a different program

import bluetooth
import random
import struct
import time
import micropython
import random
import machine

from micropython import const
_IRQ_SCAN_RESULT = const(5)

fired=False
wdt=machine.WDT(timeout=10000)
def seqFromAddr(addr, rssi):
    seq=[]
    random.seed(addr)
    global fired
   
    for i in range(0,5):
        motorVal=random.choice([12,14,33]) #specifies what motor this is attached to
        self._ble.gap_scan(90000000, 30000, 3000)



def runscan():
    time.sleep(5)
    print("running")
    global fired
    while True:
        ble = bluetooth.BLE()
        central = BLESimpleCentral(ble)
        central.scan(callback=None)
        print("scan")
        while (not fired):
          time.sleep(0.1)
          wdt.feed()
        fired=False
        p14 = machine.Pin(14)
        p14.init(p14.IN,p14.PULL_DOWN)
        machine.lightsleep(2000)

     

   


if __name__ == "__main__":
  stopVibe=machine.Pin(14)
  pwmOut=machine.PWM(stopVibe)
  pwmOut.duty(0)
  runscan()