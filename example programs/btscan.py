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

def seqFromAddr(addr, rssi):
    seq=[]
    random.seed(addr)
    global fired
   
    for i in range(0,5):
        motorVal=random.choice([12,14,32]) #specifies what motor this is attached to
        delay=random.uniform(0.1,0.3)
       
        thePin=machine.Pin(motorVal)
        pwmOut=machine.PWM(thePin)
        pwmOut.freq(100)
   
        power=(100-abs(rssi))*30
        if (power < 0):
          power=0
        pwmOut.duty(power)
        time.sleep(0.3)
        pwmOut.duty(0)
        time.sleep(delay)
    #the end, now say that we're done firing so the system goes to sleep
    fired=True
   
                   
       
   
class BLESimpleCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

        self._reset()

    def _reset(self):
        # Cached name and address from a successful scan.
        self._name = None
        self._addr_type = None
        self._addr = None

        # Callbacks for completion of various operations.
        # These reset back to None after being invoked.
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None

        # Persistent callback for when new data is notified from the device.
        self._notify_callback = None

        # Connected device.
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._tx_handle = None
        self._rx_handle = None

    def _irq(self, event, data):
     
        global fired
       
        if event == _IRQ_SCAN_RESULT:
            if (fired == False):
                addr_type, addr, adv_type, rssi, adv_data = data
                seqFromAddr(int.from_bytes(bytes(addr),"little"),rssi)


    # find devices
    def scan(self, callback=None):
        self._addr_type = None
        self._addr = None
        self._scan_callback = callback
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
        fired=False
        p14 = machine.Pin(14)
        p14.init(p14.IN,p14.PULL_DOWN)
        machine.lightsleep(2000)

     

   


if __name__ == "__main__":
  stopVibe=machine.Pin(14)
  pwmOut=machine.PWM(stopVibe)
  pwmOut.duty(0)
  runscan()
	
