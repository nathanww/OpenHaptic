from machine import Pin, Timer,ADC,PWMfrom time import sleep_msimport ubluetoothfrom esp32 import raw_temperatureimport _threadimport timeimport mathrunSavedCode=True #can be set to false to prevent saved code from interrupting the loading of a new programrunProgram=True #keep the program running in a loopprogramStatus=0import math  def waveSynth(freq,power,duration=1,waveform="sine",lowcut=0,highcut=100, stepSize=0.01):    if (len(power) != 3 or len(freq) != 3):        return -1 #arrays are not the right size    else:        motors=[]         #we use 628 points per second, so the duration value can scale this        totalPoints=(duration*6.28)/stepSize        timing=[]        for motor in range(0,3):            #generate a sine wave            temp=[]            #generate one cycle of a sine wave            x=0                       while (round(x,2) < (duration*6.28)):                tempVal=((math.sin((x*freq[motor]))+1)*power[motor]/2) #scale in the x domain (to control frequency) and in the y domain to control how the power is mpped to motor power                if waveform == "square": #if user asked for a square wave then threshold the sine wave                    if (tempVal > 50):                        tempVal=100                    else:                        tempVal=0                if tempVal < lowcut:                    tempVal=lowcut                if tempVal > highcut:                    tempVal=highcut                temp.append(int(tempVal))                x=x+stepSize            motors.append(temp)        for i in range(0,round(totalPoints)): #generate the timing array            timing.append(1/totalPoints)        return [motors,timing]def vibePattern(motorPower,timing, loop=0): #execute a custom vibration pattern   #the current PWM system has some weird behavior (I think a bug) so we are doing this custom bitbang pwm for now    if len(motorPower) == 3:         powerCheck=[len(motorPower[0]), len(motorPower[1]),len(motorPower[2]),len(timing)]        if max(powerCheck) == min(powerCheck): #check to make sure the lists are all the right length            numSegments=len(motorPower[0])            totalLoops=loop            while totalLoops >= 0:                totalLoops=totalLoops-1                pin1=Pin(12,Pin.OUT);                pin2=Pin(14,Pin.OUT);                pin3=Pin(32,Pin.OUT);                for segment in range(0,numSegments):                    stopTime=time.ticks_ms()+(timing[segment]*1000)                    while(time.ticks_ms() < stopTime):                          for i in range(0,100):                             if (i < motorPower[0][segment]):                                pin1.value(1)                            else:                                pin1.value(0)                            if (i < motorPower[1][segment]):                                pin2.value(1)                            else:                                pin2.value(0)                            if (i < motorPower[2][segment]):                                pin3.value(1)                            else:                                pin3.value(0)                                   return True         else:            print("Motor sequences don't agree")            return -1    else:        print("Wrong number of motor sequences")        return -2                    def runProgram(program):    global programStatus    global runSavedCode    runSavedCode=True    programStatus=1    program=program.replace("ENDMSG","")    print("Program")    print(program)    progFile=open("program.py",'w')    progFile.write(program)    progFile.flush()    progFile.close()    while runProgram:        try:            exec(program,globals(),locals())        except Exception:            print(traceback.format_exc())    programStatus=2    def runProgramFromStorage():    global programStatus    print("Attempting to run program")    time.sleep(30)    if runSavedCode:        progFile=open("program.py")        program=progFile.read()        progFile.flush()        progFile.close()        print(program)        progFile=open("program.py",'w')        progFile.write(program)        progFile.flush()        progFile.close()        while runProgram:            try:                exec(program,globals(),locals())            except ArithmeticError:                print(traceback.format_exc())        programStatus=2        def handleMessage(message):    if "PROG:" in message:        print("Loading new program...")        _thread.start_new_thread(runProgram, (message.split("PROG:")[1],))        class BLE():        def __init__(self, name):        self.isConnected=False        self.name = name        self.ble = ubluetooth.BLE()        self.ble.active(True)                self.disconnected()        self.ble.irq(self.ble_irq)        self.register()        self.advertiser()        self.messageBuffer=""        def connected(self):        self.isConnected=True            def disconnected(self):        self.isConnected=False                def ble_irq(self, event, data):        global messageBuffer        if event == 1:            '''Central connected'''            self.connected()            elif event == 2:            '''Central disconnected'''            self.register()            self.advertiser()            self.disconnected()                elif event == 3:            '''New message received'''            global runSavedCode            runSavedCode=False            buffer = self.ble.gatts_read(self.rx)            message = buffer.decode('UTF-8')[:-1]            self.messageBuffer=self.messageBuffer+message            print(str(len(self.messageBuffer)))            if ("ENDMSG") in self.messageBuffer:                print(self.messageBuffer)                handleMessage(self.messageBuffer)                self.messageBuffer=""                                def register(self):                # Nordic UART Service (NUS)        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'                    BLE_NUS = ubluetooth.UUID(NUS_UUID)        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)                    BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))        SERVICES = (BLE_UART, )        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)    def send(self,data): #format the data for transmission to the companion app        MTU=5         temp=""        data=data+"ENDMSG"        for char in data:            if len(temp) <= MTU:                temp=temp+char            else:                self.sendll(temp)                temp=char        self.sendll(temp)     def sendll(self, data): #low level send, doesn't check the data size etc        self.ble.gatts_notify(0, self.tx, data)    def advertiser(self):        name = bytes(self.name, 'UTF-8')        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)        # testblue_led = Pin(2, Pin.OUT)p14=Pin(14,Pin.OUT);ble = BLE("ESP32") batteryVoltage=ADC(Pin(35)) batteryVoltage.atten(ADC.ATTN_11DB) #full range_thread.start_new_thread(runProgramFromStorage, ()) #run the stored program#[motor,timing]=waveSynth([30,30.5,30],[100,100,100],duration=2,waveform="sine",stepSize=0.1) #vibePattern(motor,timing,loop=10)  while True:    if ble.isConnected: #if we have a connection, send a status message every couple of seconds        try:            print("sending status")               ble.send("ST:"+str(round((batteryVoltage.read()/4095)*6.6,2))+":"+str(programStatus))        except Exception: #this can break due to interference by a program            pass        time.sleep(2)        