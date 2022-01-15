import machine from machine import Pin, Timer,ADC,PWMimport sysfrom time import sleep_msimport ubluetoothfrom esp32 import raw_temperatureimport _threadimport timeimport mathrunSavedCode=True #can be set to false to prevent saved code from interrupting the loading of a new programrunProgram=True #keep the program running in a loopprogramStatus=0lastData=""lastDataTime=-1import mathdef waveSynth(freq,power,duration=1,waveform="sine",lowcut=0,highcut=100, phaseOffset=[0,0,0],stepSize=0.1):    if (len(power) != 3 or len(freq) != 3) or len(phaseOffset) != 3:        return -1 #arrays are not the right size    else:        motors=[]         #we use 628 points per second, so the duration value can scale this        totalPoints=(duration*6.28)/stepSize        timing=[]        for motor in range(0,3):            #generate a sine wave            temp=[]            #generate one cycle of a sine wave            x=0            while (round(x,2) < (duration*(6.28))):                tempVal=((math.sin((x*(freq[motor]/2)))+1)*power[motor]/2) #scale in the x domain (to control frequency) and in the y domain to control how the power is mpped to motor power                if waveform == "square": #if user asked for a square wave then threshold the sine wave                    if (tempVal > 50):                        tempVal=100                    else:                        tempVal=0                if tempVal < lowcut:                    tempVal=lowcut                if tempVal > highcut:                    tempVal=highcut                temp.append(int(tempVal))                x=x+stepSize            motors.append(temp)        for i in range(0,round(totalPoints)): #generate the timing array            timing.append(1/totalPoints)        return [motors,timing]def combineWaves(wave1,wave2,weight=1.0):        """combines two waveforms (with equal duration) toghether.        Arguments:    wave1 -- list containing points in the first waveform    wave2 -- list contianing points in the second waveform    weight -- how much to weight the second waveform relative to the first. 1.0 is equal weight    """    newWave=[]    if len(wave1) != len(wave2):        print("Error, the two waves are not equal length")        return -1    else:        for i in range(0,len(wave1)):            #We combine add the two waves but scale the second by weight. Then we scale them so that the overall sum is the same as the original waveform            temp=((wave1[i]/2)+((wave2[i]/2)*weight))            #find the amplitude of the new point compared to the old point, and use this to rescale the wave so that the amplitude doesn't change            scale=(1+weight)/2             newWave.append(int(temp/scale))                return newWavedef heatMotors(duration): #experimental, tries to create heat but not motion on the vibration motors    print("initial temp:"+str(raw_temperature()))     pin1=PWM(Pin(12,Pin.OUT),freq=10000000,duty=700)     pin2=PWM(Pin(14,Pin.OUT),freq=10000000,duty=700)    pin3=PWM(Pin(33,Pin.OUT),freq=10000000,duty=700)    time.sleep(duration)     pin1.deinit()    pin2.deinit()    pin3.deinit()    print("final temp:"+str(raw_temperature()))def vibePattern(motorPower,timing, loop=0): #execute a custom vibration pattern   #the current PWM system has some weird behavior (I think a bug) so we are doing this custom bitbang pwm for now    if len(motorPower) == 3:         powerCheck=[len(motorPower[0]), len(motorPower[1]),len(motorPower[2]),len(timing)]        if max(powerCheck) == min(powerCheck): #check to make sure the lists are all the right length            numSegments=len(motorPower[0])            totalLoops=loop            while totalLoops >= 0:                totalLoops=totalLoops-1                pin1=Pin(12,Pin.OUT);                pin2=Pin(14,Pin.OUT);                pin3=Pin(33,Pin.OUT);                for segment in range(0,numSegments):                    stopTime=time.ticks_ms()+(timing[segment]*1000)                    while(time.ticks_ms() < stopTime):                          for i in range(0,100):                             if (i < motorPower[0][segment]):                                pin1.value(1)                            else:                                pin1.value(0)                            if (i < motorPower[1][segment]):                                pin2.value(1)                            else:                                pin2.value(0)                            if (i < motorPower[2][segment]):                                pin3.value(1)                            else:                                pin3.value(0)                                   return True         else:            print("Motor sequences don't agree")            return -1    else:        print("Wrong number of motor sequences")        return -2        def runProgramFromStorage():    global programStatus    print("Attempting to run program")    #sait 30 seconds to allow for a new program to be sent (or other debugging)    time.sleep(30)    if runSavedCode:         progFile=open("program.py")        program=progFile.read()         progFile.flush()        progFile.close()        print(program)                while runProgram:            try:                exec(program,globals(),locals())            except Exception:                ble.send(traceback.format_exc())        programStatus=2        def handleMessage(message):    global lastData    global lastDataTime     if "PROG:" in message:        print("Loading new program...")        program=message.replace("ENDMSG","").replace("PROG:","")        print("Program")        print(program)        progFile=open("program.py",'w')        progFile.write(program)        progFile.flush()        progFile.close()        machine.reset()     else:        lastData=message        lastDataTime=time.time()        class BLE():         def __init__(self, name):        self.isConnected=False        self.name = name        self.ble = ubluetooth.BLE()        self.ble.active(True)                self.disconnected()        self.ble.irq(self.ble_irq)        self.register()        self.advertiser()        self.messageBuffer=""        def connected(self):        self.isConnected=True            def disconnected(self):        self.isConnected=False                def ble_irq(self, event, data):        global messageBuffer        if event == 1:            '''Central connected'''            self.connected()            elif event == 2:            '''Central disconnected'''            self.register()            self.advertiser()            self.disconnected()                elif event == 3:            '''New message received'''            global runSavedCode                     runSavedCode=False            buffer = self.ble.gatts_read(self.rx)            message = buffer.decode('UTF-8')[:-1]            self.messageBuffer=self.messageBuffer+message            print(str(len(self.messageBuffer)))            if ("ENDMSG") in self.messageBuffer:                print(self.messageBuffer)                handleMessage(self.messageBuffer)                self.messageBuffer=""                                def register(self):                # Nordic UART Service (NUS)        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'                    BLE_NUS = ubluetooth.UUID(NUS_UUID)        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)                    BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))        SERVICES = (BLE_UART, )        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)    def send(self,data): #format the data for transmission to the companion app        MTU=5         temp=""        data=data+"ENDMSG"        for char in data:            if len(temp) <= MTU:                temp=temp+char            else:                self.sendll(temp)                temp=char        self.sendll(temp)     def sendll(self, data): #low level send, doesn't check the data size etc        self.ble.gatts_notify(0, self.tx, data)    def advertiser(self):        name = bytes(self.name, 'UTF-8')        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)        # testp12=Pin(12,Pin.OUT);p12.value(False)p14=Pin(14,Pin.OUT);p14.value(False)p33=Pin(33,Pin.OUT);p33.value(False)ble = BLE("OpenHaptic")batteryVoltage=ADC(Pin(35)) batteryVoltage.atten(ADC.ATTN_11DB) #full range_thread.start_new_thread(runProgramFromStorage, ()) #run the stored program while True:     if ble.isConnected: #if we have a connection, send a status message every couple of seconds         try:            print("sending status")               ble.send("ST:"+str(round((batteryVoltage.read()/4095)*6.6,2))+":"+str(programStatus))        except Exception: #this can break due to interference by a program            pass        time.sleep(2)        